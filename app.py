import os
import streamlit as st
from dotenv import load_dotenv

from document_loader import load_pdf_documents
from rag_engine import answer_question, build_vector_store

load_dotenv()

st.set_page_config(
    page_title="Domain-Specific RAG Chatbot",
    page_icon="📚",
    layout="wide",
)

st.title("Domain-Specific RAG Chatbot")
st.write(
    "Upload PDF documents and ask questions. Answers are generated from the "
    "uploaded documents, with source file and page references."
)

with st.sidebar:
    st.header("Setup")
    st.write("This app uses Groq for language generation and FAISS for document retrieval.")
    api_key_present = bool(os.getenv("GROQ_API_KEY"))
    if api_key_present:
        st.success("Groq API key found.")
    else:
        st.warning("Groq API key not found. Add GROQ_API_KEY to your .env file.")
    st.caption("Do not upload your real .env file or API key to GitHub or shared folders.")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    help="Only PDF files are accepted. Use documents you are allowed to share.",
)

col1, col2 = st.columns([1, 3])
with col1:
    build_clicked = st.button("Process PDFs", type="primary", use_container_width=True)
with col2:
    st.caption("The first run may take longer while the sentence-transformer model downloads.")

if build_clicked:
    if not uploaded_files:
        st.error("Please upload at least one PDF file first.")
    elif not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is missing. Create a .env file using .env.example and add your key.")
    else:
        try:
            with st.spinner("Reading PDFs and building the searchable index..."):
                documents = load_pdf_documents(uploaded_files)
                if not documents:
                    st.error("No readable text was found. Check that the PDFs contain selectable text.")
                else:
                    st.session_state.vector_store = build_vector_store(documents)
                    st.session_state.indexed_files = [file.name for file in uploaded_files]
                    st.session_state.chat_history = []
                    st.success(
                        f"Processed {len(uploaded_files)} PDF file(s) and indexed "
                        f"{len(documents)} page(s)."
                    )
        except Exception as exc:
            st.error("The PDFs could not be processed.")
            st.exception(exc)

if st.session_state.indexed_files:
    st.info("Indexed files: " + ", ".join(st.session_state.indexed_files))

st.divider()
st.subheader("Ask a question")

question = st.text_input(
    "Your question",
    placeholder="Example: What are the main objectives described in the document?",
)

if st.button("Get Answer", use_container_width=False):
    if not question.strip():
        st.warning("Enter a question first.")
    elif st.session_state.vector_store is None:
        st.warning("Upload your PDFs and click Process PDFs first.")
    elif not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is missing. Add it to your local .env file.")
    else:
        try:
            with st.spinner("Searching the documents and preparing an answer..."):
                result = answer_question(st.session_state.vector_store, question.strip())
            st.session_state.chat_history.append(
                {"question": question.strip(), "answer": result["answer"], "sources": result["sources"]}
            )
        except Exception as exc:
            st.error("I couldn't generate an answer. Check your API key, internet connection, and package setup.")
            st.exception(exc)

for index, item in enumerate(reversed(st.session_state.chat_history), start=1):
    st.markdown(f"### Answer {len(st.session_state.chat_history) - index + 1}")
    st.markdown(f"**Question:** {item['question']}")
    st.write(item["answer"])
    if item["sources"]:
        with st.expander("View source documents and pages"):
            for source in item["sources"]:
                st.write(f"- **{source['source']}** — page {source['page']}")
    else:
        st.caption("No source passages were returned for this answer.")

st.caption(
    "Reminder: AI-generated answers can be incorrect. Check important information against the original PDF."
)
