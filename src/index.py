from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.textchunks import splitting_document 
from dotenv import load_dotenv
import os
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def vectors():
    
    text_chunks = splitting_document()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    if os.path.exists("faiss_index"):
        vectordb = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        print("Index Present")
    else:    
        vectordb = FAISS.from_documents(text_chunks, embeddings)
        vectordb.save_local("faiss_index")
        print("Index Created")
    return vectordb


if __name__ == "__main__":
    vector = vectors()
    print(vector)

    
    
    
    