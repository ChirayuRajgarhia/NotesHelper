# Streamlit UI
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import streamlit as st
from utils.pdf_loader import extract_text_from_pdf
import utils.chunker as chunker
import embedding.gemini_embed as gemini_embed
from app.ingestion import ingest
from app.retrieval import answer_question

def load_page():
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
            # st.subheader(f"Extracted text from {pdf.name}")
            # st.text_area("Preview",text,height=200)
            # chunk = chunker.chunk_text(text)
            # st.write("Chunks Length : ",len(chunk))
            # st.text_area("Chunks : ", chunk[0], height=200)
            # embedding = gemini_embed.embed_chunks(chunk[0])
            # st.write("Embedding Length : ",len(embedding))
            # st.text_area("Embedding : ", embedding[0], height=200)
            with st.spinner("Processing pdf..."):
                ingest(text)

        st.write("Ask questions")
        question = st.text_input(label="Enter Question", max_chars=200, on_change=None, placeholder="My doubt is", disabled=False, label_visibility="visible")
        if question:
            with st.spinner("Searching for answers..."):
                answer = answer_question(question)
                st.write(answer)

load_page()
