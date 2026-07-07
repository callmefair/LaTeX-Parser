import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = "models/gemini-embedding-001"

CHROMA_DIR = "./chroma_db"
MD_GLOB = "md/**/*.md"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
RETRIEVER_K = 3