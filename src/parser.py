# parser.py
import fitz
import os

def chunk_text(text, chunk_size=500, overlap=50):
    words=text.split()
    chunks=[]
    i=0
    while i<len(words):
        chunk=words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i=i+chunk_size-overlap
    return chunks
def parse_pdf(file_path):
    doc=fitz.open(file_path)
    full_text=""
    for page in doc:
        full_text +=page.get_text("text")+" "
    full_text=" ".join(full_text.split())
    return chunk_text(full_text)
if __name__ == "__main__":
    chunks=parse_pdf("data_ingest/Sample Data 1.pdf")
    for chunk in chunks[:3]:
        print(chunk)
        print("---")