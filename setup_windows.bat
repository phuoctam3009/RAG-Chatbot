@echo off
REM Windows Setup Script for IT Support Chatbot
REM Double-click this file to run automatic setup

echo ========================================
echo IT Support Chatbot - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/6] Python found!
python --version

echo.
echo [2/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Trying alternative method...
    pip install virtualenv
    virtualenv venv
)

echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [5/6] Installing required packages...
echo This may take a few minutes...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo WARNING: Some packages failed to install
    echo Trying to install packages individually...
    
    pip install python-dotenv
    pip install openai
    pip install langchain
    pip install langchain-openai
    pip install faiss-cpu
    pip install numpy
    pip install pandas
    pip install streamlit
    pip install tiktoken
)

echo.
echo [6/6] Checking installation...
python -c "import faiss, langchain, openai, streamlit; print('All packages installed successfully!')"

if errorlevel 1 (
    echo.
    echo WARNING: Installation verification failed
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete! 
echo ========================================
echo.
echo Virtual environment created: venv\
echo All packages installed successfully!
echo.
echo NEXT STEPS:
echo.
echo 1. Create .env file with your API credentials:
echo    - Copy .env.example to .env
echo    - Edit .env with your OpenAI or Azure OpenAI credentials
echo.
echo 2. Generate mock data:
echo    python generate_mock_data.py
echo.
echo 3. Build vector store:
echo    python build_vector_store.py
echo.
echo 4. Launch chatbot:
echo    streamlit run app.py
echo.
echo TIP: Always activate virtual environment first:
echo      venv\Scripts\activate
echo.
echo Read WINDOWS_INSTALLATION_FIX.md for detailed help
echo.
pause
