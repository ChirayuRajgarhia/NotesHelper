# PDF text extraction logic

import pdfplumber
from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_file):
    text = ""

    try:
        # First try pdfplumber (best quality)
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except:
        # Fallback to PyPDF2
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""

    return text
