import os
from typing import Dict, List

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS

from prompt import RAG_PROMPT
from vector_store import create_vector_store

DEFAULT_MODEL = "llama-3.3-70b-versatile"
RETRIEVAL_K = 4


def build_vector_store(documents) -> FAISS:
    """Create and return a FAISS index for the uploaded PDF pages."""
    return create_vector_store(documents)


def _format_context(documents) -> str:
    """Format retrieved chunks with their source and page metadata."""
    sections = []
    for doc in documents:
        source = doc.metadata.get("source", "Unknown file")
        page = doc.metadata.get("page", "Unknown")
        sections.append(
            f"[Source: {source}, Page: {page}]\n{doc.page_content}"
        )
    return "\n\n---\n\n".join(sections)


def answer_question(vector_store: FAISS, question: str) -> Dict[str, object]:
    """Retrieve relevant text and ask Groq to answer from that context."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Add it to your local .env file.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": RETRIEVAL_K},
    )
    relevant_docs = retriever.invoke(question)

    if not relevant_docs:
        return {
            "answer": "I couldn't find that information in the uploaded documents.",
            "sources": [],
        }

    context = _format_context(relevant_docs)
    prompt_value = RAG_PROMPT.invoke({"context": context, "question": question})

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=api_key,
    )
    response = llm.invoke(prompt_value)
    answer = str(response.content).strip()

    # Return unique source/page pairs in the order retrieved.
    sources: List[Dict[str, object]] = []
    seen = set()
    for doc in relevant_docs:
        source = str(doc.metadata.get("source", "Unknown file"))
        page = doc.metadata.get("page", "Unknown")
        key = (source, page)
        if key not in seen:
            seen.add(key)
            sources.append({"source": source, "page": page})

    return {"answer": answer, "sources": sources}
