@echo off
echo Starting Domain-Specific RAG Chatbot...
if not exist .venv (
    echo Virtual environment not found. Please follow README.md setup steps first.
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat
streamlit run app.py
pause
