# Streamlit UI

import streamlit as st
from pdf_loader import extract_text_from_pdf

st.set_page_config(page_title="Notes Helper", layout="wide")

st.title("Get exact answer from your Notes !!!")
st.write("Upload your PDF notes and ask questions")

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for pdf in uploaded_files:
        text = extract_text_from_pdf(pdf)
        st.subheader(f"Extracted text from {pdf.name}")
        st.text_area("Preview", text[:2000], height=200)
