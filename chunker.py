from langchain_text_splitters import RecursiveCharacterTextSplitter
from documentloader import load_documents


def chunk_documents():

    documents = load_documents()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")

    return chunks