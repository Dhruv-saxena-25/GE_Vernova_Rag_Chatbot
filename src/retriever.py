from src.index import vectors
from src.textchunks import splitting_document
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

store = {}

def get_session_history(session_id: str)-> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id]= ChatMessageHistory()
  return store[session_id]


def retrieval(question):
    
    
    llm = ChatOpenAI(temperature= 0.6)
    
    vectordb = vectors()
    score =vectordb.similarity_search_with_score(question)
    
    threshold = 1.0 
    if score[0][1] <= threshold:

        retriever = vectordb.as_retriever(search_type="similarity_score_threshold",
                            search_kwargs={'score_threshold': 0.2})
        
        retriever_prompt = ("Given a chat history and the latest user question which might reference context in the chat history,"
        "formulate a standalone question which can be understood without the chat history."
        "Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
        )
        
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
        ("system", retriever_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
            ]
        )
        
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
        
        CHAT_BOT_TEMPLATE = """
        You are a PDF document assistant bot, specialized in providing answers based on the contents of the PDF file.
        If someone requests a summary, you will summarize the entire document. Use your knowledge to enhance the answers
        based on the context. Ensure your responses are relevant to the question and concise yet informative. Please avoid
        repeating sentences or phrases. If someone greets you, make sure to greet them back.
        if someone greets you greet them back do not got to the context give answer by yourself example of greeting like Hello, Hii, How are you etc.
        CONTEXT:
        {context}

        QUESTION: {input}

        YOUR ANSWER: """
        
        qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CHAT_BOT_TEMPLATE),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ]
    )
        
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        chat_history= [] 
        conversational_rag_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
        
        response = conversational_rag_chain.invoke(
        {"input": question},
        config={
        "configurable": {"session_id": "abc123"}},
    )
        
        source_documents = response.get("context", [])
        page_number = []
        for doc in source_documents:
            pages = doc.metadata.get('page', 'Unknown')
            # text_excerpt = doc.page_content[:200]  # Get the first 200 characters as a preview
            page_number.append(pages)
        
        return response, page_number
    else:
        # Fallback response if no relevant results are found
        response = { "answer": "I'm sorry, I couldn't find the relevant information. Please check the spelling and try again."}
        page_number = " "
        return response, page_number

if __name__ == "__main__":
    
    question = "Tell me about the ge vernova??"
    response, page_number = retrieval(question)
    print(response)
    print(page_number)