from io import BytesIO
from typing import List

from langchain_core.documents import Document
from pypdf import PdfReader


def load_pdf_documents(uploaded_files) -> List[Document]:
    """
    Extract selectable text from each page of uploaded PDF files.

    Each returned Document represents one PDF page and includes source and
    page metadata. Page numbers are one-based for easier reading by users.
    """
    documents: List[Document] = []

    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.getvalue()
        reader = PdfReader(BytesIO(file_bytes))

        for page_index, page in enumerate(reader.pages):
            text = (page.extract_text() or "").strip()
            if not text:
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": uploaded_file.name,
                        "page": page_index + 1,
                    },
                )
            )

    return documents
