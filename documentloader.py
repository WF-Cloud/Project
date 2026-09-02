import pymupdf as fitz
from pathlib import Path

from langchain_core.documents import Document


DATA_PATH = Path("Knowledge")


def load_documents():

    documents = []

    for pdf_file in DATA_PATH.glob("*.pdf"):

        print(f"Loading {pdf_file.name}...")

        pdf = fitz.open(pdf_file)

        for page_number, page in enumerate(pdf):

            text = page.get_text()

            if text.strip():

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": pdf_file.name,
                            "page": page_number + 1
                        }
                    )
                )

        pdf.close()

    print(f"Loaded {len(documents)} pages.")

    return documents