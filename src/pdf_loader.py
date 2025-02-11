import os
from PyPDF2 import PdfReader

def load_documents(doc_folder: str):
    '''
    Loads relevant documents for tokenization
    '''
    
    doc_texts = []
    for filename in os.listdir(doc_folder):
        if filename.endswith(".txt") or filename.endswith(".yaml"):
            with open(os.path.join(doc_folder, filename), "r", encoding="utf-8") as f:
                text = f.read()
                doc_texts.append(text)
        elif filename.endswith(".pdf"):
            text = ""
            with open(os.path.join(doc_folder, filename), "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
                doc_texts.append(text)
    
    return doc_texts

