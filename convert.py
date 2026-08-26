import pymupdf4llm
from pathlib import Path

DATA_PATH = Path("Knowledge")

def convert_pdf():
    for pdf_file in DATA_PATH.glob("*.pdf"):
        print(f"Converting {pdf_file} to markdown...")

        markdown = pymupdf4llm.to_markdown(pdf_file)

        output_file = pdf_file.with_suffix(".md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"Saved markdown to {output_file.name}")

if __name__ == "__main__":
    convert_pdf()