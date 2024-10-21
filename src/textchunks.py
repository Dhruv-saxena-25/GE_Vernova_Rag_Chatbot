from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def splitting_document():
    file_path = "data\\GE_Vernova_Sustainability_Report_2023.pdf"
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,)
    text_chunks = text_splitter.split_documents(docs)
    return text_chunks


if __name__ == "__main__":
        chunks = splitting_document()
        print(chunks)
        
    