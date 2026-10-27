# Domain-Specific RAG Chatbot for PDF Question Answering

A Streamlit application that lets a user upload PDF documents and ask questions about their contents. It extracts page text, splits it into chunks, creates embeddings with Sentence Transformers, stores them in FAISS, retrieves relevant chunks, and uses Groq to generate a grounded answer with source-page references.

## Features

- Upload one or more PDF files through a Streamlit interface.
- Extract text page by page with `pypdf`.
- Split text into overlapping chunks.
- Create embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
- Search relevant chunks using FAISS.
- Generate answers using Groq and LangChain.
- Show source PDF filenames and page numbers.
- Instruct the model to say when the answer is not present in the retrieved context.
- Keep the API key in a local `.env` file.

## Requirements

- Windows, macOS, or Linux
- Python 3.11 or 3.12 recommended
- Internet connection for package installation, model download, and Groq API calls
- A Groq API key

## Setup on Windows

Open PowerShell in this project folder and run these commands one at a time.

### 1. Create a virtual environment

```powershell
py -3.11 -m venv .venv
```

If Python 3.11 is not installed, install Python 3.11 or 3.12, then reopen PowerShell.

### 2. Activate it

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead, or run the following only for the current PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install packages

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The first installation can take several minutes because the embedding and machine-learning packages are large.

### 4. Create your local `.env` file

Copy `.env.example` to a new file named `.env` in the same folder. Open `.env` and replace the placeholder with your own Groq API key:

```text
GROQ_API_KEY=your_real_groq_api_key
```

Do not include quotes unless your provider specifically instructs you to. Do not share or upload the real `.env` file. Obtain a key from the Groq developer console.

### 5. Start the app

```powershell
streamlit run app.py
```

Streamlit should open the app in your browser. If it does not, open the local URL printed in the terminal, usually `http://localhost:8501`.

## How to use it

1. Upload one or more text-based PDF files.
2. Click **Process PDFs** and wait for indexing to finish.
3. Enter a question about the uploaded documents.
4. Click **Get Answer**.
5. Expand **View source documents and pages** to inspect the retrieved source references.

## Project files

- `app.py` — Streamlit interface.
- `document_loader.py` — PDF text extraction and page metadata.
- `vector_store.py` — chunking, embeddings, and FAISS index creation.
- `prompt.py` — grounded-answer instructions.
- `rag_engine.py` — retrieval and Groq answer generation.
- `requirements.txt` — Python dependencies.
- `.env.example` — safe example of required environment configuration.
- `.gitignore` — excludes secrets and generated files.

## Notes and limitations

- This starter version creates the FAISS index in memory when you click **Process PDFs**. The index is not saved between app restarts.
- Scanned PDFs containing only images may produce no text. OCR is not included in this version.
- The application displays source documents/pages retrieved for the answer. A source being retrieved does not guarantee that every sentence in the answer is correct; verify important details in the original PDF.
- Groq model availability can change. If the configured model is unavailable for your account, update `DEFAULT_MODEL` in `rag_engine.py` to a currently supported chat model in your Groq account.
- Avoid uploading confidential or sensitive documents unless you have permission and understand the services used.

## Troubleshooting

**`GROQ_API_KEY is missing`**  
Confirm the file is named `.env` (not `.env.txt`), is in the same folder as `app.py`, and contains `GROQ_API_KEY=...`.

**PowerShell cannot activate the virtual environment**  
Use Command Prompt and run `.venv\\Scripts\\activate.bat`, or follow the temporary PowerShell execution-policy command above.

**FAISS or sentence-transformers installation fails**  
Use Python 3.11 or 3.12 in a fresh virtual environment, then repeat the installation.

**No text is extracted from a PDF**  
Try a PDF where you can select and copy text. OCR for scanned documents is not included.

## Responsible use

The chatbot can make mistakes. Check important answers against the source documents. Do not expose API keys. Treat instructions embedded in uploaded documents as document content, not as trusted commands.
