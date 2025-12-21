# # Streamlit UI
# # import sys
# # import os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# import streamlit as st
# from utils.pdf_loader import extract_text_from_pdf
# from app.ingestion import ingest
# from app.retrieval import answer_question

# def load_page():
#     st.set_page_config(page_title="Notes Helper", layout="wide")

#     st.title("Get exact answer from your Notes !!!")
#     st.write("Upload your PDF notes and ask questions")

#     uploaded_files = st.file_uploader(
#         "Upload PDF files",
#         type=["pdf"],
#         accept_multiple_files=True
#     )

#     if uploaded_files:
#         for pdf in uploaded_files:
#             text = extract_text_from_pdf(pdf)
#             # st.subheader(f"Extracted text from {pdf.name}")
#             # st.text_area("Preview",text,height=200)
#             # chunk = chunker.chunk_text(text)
#             # st.write("Chunks Length : ",len(chunk))
#             # st.text_area("Chunks : ", chunk[0], height=200)
#             # embedding = gemini_embed.embed_chunks(chunk[0])
#             # st.write("Embedding Length : ",len(embedding))
#             # st.text_area("Embedding : ", embedding[0], height=200)
#             with st.spinner("Processing pdf..."):
#                 ingest(text)

#         st.write("Ask questions")
#         question = st.text_input(label="Enter Question", max_chars=200, on_change=None, placeholder="My doubt is", disabled=False, label_visibility="visible")
#         if question:
#             with st.spinner("Searching for answers..."):
#                 answer = answer_question(question)
#                 st.write(answer)

# load_page()


import streamlit as st
from utils.pdf_loader import extract_text_from_pdf
from app.ingestion import ingest
from app.retrieval import answer_question
from streamlit.runtime.scriptrunner import get_script_run_ctx
from db.pinecodeIndex import get_index

def get_streamlit_session_id():
    """
    Returns the unique session ID for the current user's connection.
    Note: This uses an internal Streamlit API .
    """
    try:
        # Get the current script run context
        ctx = get_script_run_ctx()
        if ctx is None:
            return None
        return ctx.session_id
    except ImportError:
        # Handle cases where the internal module path might change
        st.error("Could not import necessary Streamlit runtime module.")
        return None

def delete_current_session_data():
    if "session_id" in st.session_state:
        try:
            # This wipes everything in that specific namespace
            index = get_index()
            index.delete(delete_all=True, namespace=st.session_state.session_id)
            st.success("All session data has been deleted.")
        except Exception as e:
            # If the namespace is already empty, Pinecone might throw an error
            st.info("No data found to delete or session already cleared.")

def load_page():
    st.set_page_config(page_title="Notes Helper", layout="wide")
    st.title("Get exact answer from your Notes !!!")

    # TO stop same file from processing multiple times
    # set is made
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()
    if "session_id" not in st.session_state:
        st.session_state.session_id = get_streamlit_session_id()

    if st.session_state.session_id :
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True
        )

        # ingest each pdf only once
        if uploaded_files :
            for pdf in uploaded_files:
                if pdf.name not in st.session_state.processed_files:
                    with st.spinner(f"Processing {pdf.name}"):
                        text = extract_text_from_pdf(pdf)
                        ingest(text,st.session_state.session_id)
                        st.session_state.processed_files.add(pdf.name)
                    

        # Question input
        if st.session_state.processed_files:

            if st.button("Delete all pdf"):
                delete_current_session_data()

            question = st.text_input(
                "Enter Question",
                max_chars=200,
                placeholder="My doubt is"
            )

            if question:
                with st.spinner("Searching for answers..."):
                    answer = answer_question(question,st.session_state.session_id)
                    st.write(answer)

load_page()
