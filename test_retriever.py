from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PATH = "chroma"
COLLECTION_NAME = "utem_documents"

# Load the same embedding model used when creating ChromaDB
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Load ChromaDB
db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding,
    collection_name=COLLECTION_NAME
)

question = "What is the registration date for new students?"

results = db.similarity_search(question, k=5)

print("\n")
print("=" * 80)
print("RETRIEVAL TEST")
print("=" * 80)

print(f"\nQuestion: {question}")
print(f"Number of results: {len(results)}")

for i, document in enumerate(results):

    print("\n" + "-" * 80)
    print(f"RESULT {i + 1}")
    print("-" * 80)

    print("\nSOURCE:")
    print(document.metadata.get("source"))

    print("\nPAGE:")
    print(document.metadata.get("page"))

    print("\nCONTENT:")
    print(document.page_content[:1500])