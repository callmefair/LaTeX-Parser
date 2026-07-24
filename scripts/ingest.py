from glob import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from src.config import GOOGLE_API_KEY, EMBEDDING_MODEL, CHROMA_DIR, MD_GLOB, CHUNK_SIZE, CHUNK_OVERLAP

def indexing():
    print("문서 로딩 및 인덱싱 시작...")

    md_paths = sorted(glob(MD_GLOB, recursive=True)) # 테스트용
    md_docs = []
    for p in md_paths:
        md_docs.extend(TextLoader(p, encoding="utf-8").load())

    docs = md_docs
    print(f"로딩된 Document 수: {len(docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
        add_start_index=False,
    )

    split_docs = splitter.split_documents(docs)
    print(f"분할된 chunk 수: {len(split_docs)}")

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY,
    )

    vectorstore = Chroma.from_documents(
        split_docs, 
        embeddings,
        persist_directory=CHROMA_DIR,
    )
    print("인덱싱 완료")

if __name__ == "__main__":
    indexing()
