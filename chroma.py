import os
import shutil

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from chunker import chunk_documents


CHROMA_PATH = "chroma"
COLLECTION_NAME = "utem_documents"

print("Creating document chunks...")
chunks = chunk_documents()
print(f"Total chunks: {len(chunks)}")


print("Loading embedding model...")
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
print("Embedding model loaded!")

if os.path.exists(CHROMA_PATH):
    print("Removing existing ChromaDB...")
    shutil.rmtree(CHROMA_PATH)

print("Creating ChromaDB...")

db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory=CHROMA_PATH,
    collection_name=COLLECTION_NAME
)

print()
print("========================================")
print("ChromaDB created successfully!")
print("========================================")
print(f"Collection: {COLLECTION_NAME}")
print(f"Chunks stored: {len(chunks)}")
print(f"Database location: {CHROMA_PATH}")