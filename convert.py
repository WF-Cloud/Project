import pymupdf4llm
from pathlib import Path

PDF_FILE = Path("Knowledge/peraturan_akademik_010126.pdf")

def convert_pdf():
    print(f"Converting {PDF_FILE} to markdown...")

    markdown = pymupdf4llm.to_markdown(PDF_FILE)

    output_file = PDF_FILE.with_suffix(".md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Saved markdown to {output_file.name}")


if __name__ == "__main__":
    convert_pdf()