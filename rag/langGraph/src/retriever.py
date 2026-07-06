from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from src.config import GOOGLE_API_KEY, EMBEDDING_MODEL, CHROMA_DIR, RETRIEVER_K

def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )

    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": RETRIEVER_K})