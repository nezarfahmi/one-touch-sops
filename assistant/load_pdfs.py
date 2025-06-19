import os
import fitz # PyMuPDF

def extract_text_from_pdf(pdf_dir):
    docs = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_dir, filename)
            with fitz.open(path) as doc:
                text =""
                for page in doc:
                    text += page.get_text()
                docs.append({
                    "filename" : filename,
                    "text" : text
                })
    return docs