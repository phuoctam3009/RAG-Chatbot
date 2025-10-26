@echo off
REM Quick Start Script - Run after setup is complete

echo ========================================
echo IT Support Chatbot - Quick Start
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_windows.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo.
    echo Please create .env file with your API credentials:
    echo.
    echo For OpenAI API:
    echo   OPENAI_API_KEY=sk-your-key-here
    echo   OPENAI_MODEL=gpt-4
    echo   OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
    echo.
    echo For Azure OpenAI:
    echo   AZURE_OPENAI_API_KEY=your-key
    echo   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
    echo   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
    echo   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your-embedding-deployment
    echo   AZURE_OPENAI_API_VERSION=2024-02-15-preview
    echo.
    pause
    exit /b 1
)

REM Check if knowledge base exists
if not exist "it_knowledge_base.json" (
    echo [1/3] Generating knowledge base...
    python generate_mock_data.py
) else (
    echo [1/3] Knowledge base already exists
)

REM Check if vector store exists
if not exist "faiss_index\" (
    echo [2/3] Building vector store...
    python build_vector_store.py
) else (
    echo [2/3] Vector store already exists
)

echo [3/3] Launching chatbot...
echo.
echo ========================================
echo Starting Streamlit...
echo Press Ctrl+C to stop
echo ========================================
echo.

streamlit run app.py

pause
