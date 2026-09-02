from langchain_text_splitters import RecursiveCharacterTextSplitter

from documentloader import load_documents


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=300
)


def chunk_documents():

    documents = load_documents()

    all_chunks = []

    for document in documents:

        chunks = text_splitter.split_documents(
            [document]
        )

        all_chunks.extend(chunks)

        print(
            f"Page {document.metadata['page']} "
            f"→ {len(chunks)} chunks"
        )

    print(
        f"Total chunks created: "
        f"{len(all_chunks)}"
    )

    return all_chunks


if __name__ == "__main__":

    chunks = chunk_documents()

    print("Chunking completed!")