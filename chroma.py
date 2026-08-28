import os
import shutil

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from chunker import chunk_documents

CHROMA_PATH = "chroma_db"

if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)

# load chunks from markdown files
chunks = chunk_documents()

print(f"Total Chunks: {len(chunks)}")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

db = Chroma.from_documents(chunks, embedding, persist_directory=CHROMA_PATH)

print(f"Saved {len(chunks)} chunks to Chroma database at {CHROMA_PATH}")