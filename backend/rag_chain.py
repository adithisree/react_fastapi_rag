import os
from pathlib import Path


from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
BASE_DIR = Path(__file__).resolve().parent
VECTORSTORE_PATH = BASE_DIR / "vectorstore"
GROQ_MODEL = "llama-3.3-70b-versatile"

load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

PROMPT = ChatPromptTemplate.from_template(
    """
You are a helpful assistant.

Answer ONLY from the provided context.

If the answer is not present in the context, say:

"I couldn't find the answer in the provided documents."

Context:
{context}

Question:
{input}
"""
)


def _get_groq_api_key():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or api_key == "your_groq_api_key_here":
        raise RuntimeError("GROQ_API_KEY is missing.")

    return api_key


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    return FAISS.load_local(str(VECTORSTORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )
def get_llm():
    return ChatGroq(
        api_key=_get_groq_api_key(),
        model=GROQ_MODEL,
        temperature=0,
    )


def ask_question(question):
    llm = get_llm()
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(question, k=3)

    chain = PROMPT | llm
    response = chain.invoke(
        {
            "context": _format_docs(docs),
            "input": question,
        }
    )
  

    return response.content
