# 🪟 Windows Installation Fix Guide

## ⚠️ Problem: Permission Error on Windows

**Error:**
```
ERROR: Could not install packages due to an OSError: [WinError 2] 
The system cannot find the file specified: 'C:\\Python312\\Scripts\\dotenv.exe'
```

**Cause:** Installing directly to system Python requires admin privileges or conflicts with existing packages.

---

## ✅ SOLUTION 1: Use Virtual Environment (BEST METHOD)

Virtual environments isolate your project dependencies and avoid permission issues.

### Step 1: Create Virtual Environment
```cmd
# Navigate to your project folder
cd path\to\it-support-chatbot

# Create virtual environment
python -m venv venv
```

### Step 2: Activate Virtual Environment
```cmd
# Activate it
venv\Scripts\activate

# You should see (venv) in your prompt:
# (venv) C:\path\to\it-support-chatbot>
```

### Step 3: Install Packages
```cmd
# Now install (no admin needed!)
pip install -r requirements.txt
```

### Step 4: Run the Chatbot
```cmd
# Generate data
python generate_mock_data.py

# Build vector store
python build_vector_store.py

# Launch chatbot
streamlit run app.py
```

### To Deactivate Later
```cmd
deactivate
```

---

## ✅ SOLUTION 2: Install with Admin Rights

### Option A: Run Command Prompt as Administrator
1. Press Windows key
2. Type "cmd"
3. Right-click "Command Prompt"
4. Select "Run as administrator"
5. Navigate to your folder:
   ```cmd
   cd C:\path\to\it-support-chatbot
   ```
6. Install:
   ```cmd
   pip install -r requirements.txt
   ```

### Option B: Run PowerShell as Administrator
1. Press Windows key
2. Type "powershell"
3. Right-click "Windows PowerShell"
4. Select "Run as administrator"
5. Navigate and install:
   ```powershell
   cd C:\path\to\it-support-chatbot
   pip install -r requirements.txt
   ```

---

## ✅ SOLUTION 3: Install to User Directory

Install packages for your user only (no admin needed):

```cmd
pip install --user -r requirements.txt
```

**Note:** Scripts will be installed to:
- `C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts`

---

## ✅ SOLUTION 4: Use Anaconda (Easiest for Windows)

If you keep having issues, Anaconda is easier on Windows:

### Step 1: Install Anaconda
Download from: https://www.anaconda.com/download

### Step 2: Create Conda Environment
```cmd
# Open Anaconda Prompt (comes with Anaconda)
conda create -n it-support python=3.11
conda activate it-support
```

### Step 3: Install Packages
```cmd
# Navigate to project
cd C:\path\to\it-support-chatbot

# Install most packages with conda
conda install -c conda-forge faiss-cpu numpy pandas

# Install remaining with pip
pip install openai langchain langchain-openai streamlit python-dotenv tiktoken
```

### Step 4: Run
```cmd
python generate_mock_data.py
python build_vector_store.py
streamlit run app.py
```

---

## 🎯 RECOMMENDED: Step-by-Step Virtual Environment Setup

Here's the complete process for Windows:

```cmd
# 1. Open Command Prompt (no admin needed)
# Press Windows + R, type: cmd, press Enter

# 2. Navigate to Downloads (or wherever you extracted the zip)
cd C:\Users\YourName\Downloads\it-support-chatbot

# 3. Create virtual environment
python -m venv venv

# 4. Activate it
venv\Scripts\activate

# 5. Upgrade pip (optional but recommended)
python -m pip install --upgrade pip

# 6. Install packages
pip install -r requirements.txt

# 7. Create .env file (use notepad)
notepad .env

# In notepad, add your credentials:
# OPENAI_API_KEY=sk-your-key-here
# OPENAI_MODEL=gpt-4
# OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
# Save and close

# 8. Generate data
python generate_mock_data.py

# 9. Build vector store
python build_vector_store.py

# 10. Launch chatbot
streamlit run app.py
```

---

## 🔍 Verify Virtual Environment

Check that you're in the virtual environment:

```cmd
# Should show path to venv folder
where python

# Expected output:
# C:\path\to\it-support-chatbot\venv\Scripts\python.exe
```

---

## 🆘 Still Having Issues?

### Issue: "python: command not found"
**Solution:** Python not in PATH. Reinstall Python and check "Add Python to PATH"

### Issue: "pip: command not found"
**Solution:** Use `python -m pip` instead of `pip`

### Issue: "'venv\Scripts\activate' is not recognized"
**Solution:** Make sure you're in the correct directory where venv folder exists

### Issue: "Access is denied"
**Solution:** 
1. Close any Python/Streamlit processes in Task Manager
2. Try Solution 1 (Virtual Environment) - it doesn't need admin rights

### Issue: "Cannot create virtual environment"
**Solution:** 
```cmd
# Install virtualenv
pip install virtualenv

# Use virtualenv instead
virtualenv venv
```

---

## 💡 Why Virtual Environment is Best

### Benefits:
✅ No admin rights needed  
✅ Isolated dependencies  
✅ No conflicts with other projects  
✅ Easy to delete and recreate  
✅ Industry standard practice  

### To Delete Virtual Environment:
```cmd
# Deactivate first
deactivate

# Just delete the folder
rmdir /s venv
```

---

## 📝 Quick Reference Card

**Create venv:**
```cmd
python -m venv venv
```

**Activate venv:**
```cmd
venv\Scripts\activate
```

**Install packages:**
```cmd
pip install -r requirements.txt
```

**Deactivate venv:**
```cmd
deactivate
```

**Delete venv:**
```cmd
rmdir /s venv
```

---

## 🎯 Summary

**Best Solution for Windows:**
1. ✅ Use virtual environment (`python -m venv venv`)
2. ✅ Activate it (`venv\Scripts\activate`)
3. ✅ Install packages (`pip install -r requirements.txt`)
4. ✅ Run the chatbot

**No admin rights needed! No permission errors! Clean installation!**

---

## 🚀 Full Windows Setup Script

Save this as `setup_windows.bat`:

```batch
@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing packages...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create .env file with your API key
echo 2. Run: python generate_mock_data.py
echo 3. Run: python build_vector_store.py  
echo 4. Run: streamlit run app.py
echo.
pause
```

Run it by double-clicking `setup_windows.bat`

---

**This will fix your Windows installation issues! Use virtual environment - it's the cleanest solution.** 🎉
