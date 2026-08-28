from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


CHROMA_PATH = "chroma_db"

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding
)


def retrieve_documents(question, k=3):

    results = db.similarity_search(
        question,
        k=k
    )

    return results