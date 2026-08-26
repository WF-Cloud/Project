from langchain_community.document_loaders import DirectoryLoader

DATA_PATH = "Knowledge/"

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents

