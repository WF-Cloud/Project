import pymupdf4llm

text = pymupdf4llm.to_text("Knowledge/BukuPanduan.pdf")
print(text)

with open("Knowledge/BukuPanduan.md", "w", encoding="utf-8") as f:
    f.write(text)