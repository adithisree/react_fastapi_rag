
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (DirectoryLoader,PyPDFLoader,)
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

DOCUMENTS_PATH = "documents"
VECTORSTORE_PATH = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def ingest_documents():
    
    loader = DirectoryLoader(
        DOCUMENTS_PATH,
        glob="*.pdf",
        loader_cls=PyPDFLoader,
    )

    documents = loader.load()

   
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    
    vectorstore = FAISS.from_documents(chunks,embeddings,) 
    
    vectorstore.save_local(str(VECTORSTORE_PATH))

    print("Done!")
    print(f"Loaded {len(documents)} pages")
    print(f"Created {len(chunks)} chunks")

if __name__ == "__main__":
    ingest_documents()

   