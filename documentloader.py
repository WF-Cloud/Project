from pathlib import Path
from langchain_community.document_loaders import TextLoader

DATA_PATH = Path("Knowledge/")


def load_documents():

    documents = []

    for md_file in DATA_PATH.glob("*.md"):

        loader = TextLoader(
            str(md_file),
            encoding="utf-8"
        )

        documents.extend(loader.load())

    return documents