from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150


def split_documents(documents: List[Document]) -> List[Document]:
    """Split page-level documents into smaller overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def create_vector_store(documents: List[Document]) -> FAISS:
    """Create embeddings for document chunks and store them in FAISS."""
    if not documents:
        raise ValueError("No readable PDF text was found.")

    chunks = split_documents(documents)
    if not chunks:
        raise ValueError("The PDF text could not be split into searchable chunks.")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    return FAISS.from_documents(chunks, embeddings)
