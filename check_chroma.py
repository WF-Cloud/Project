import chromadb


CHROMA_PATH = "chroma"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collections = client.list_collections()

print("Collections found:")

for collection in collections:
    print(
        f"- {collection.name}"
    )

    print(
        f"  Documents: {collection.count()}"
    )