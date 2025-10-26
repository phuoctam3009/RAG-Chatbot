# 🔧 Installation Fix Guide

## ✅ Fixed: FAISS Version Issue

The original `requirements.txt` had an outdated FAISS version. This has been fixed!

---

## 🚀 Installation Options

### Option 1: Install with Updated Requirements (Recommended)
```bash
pip install -r requirements.txt
```

This now uses flexible version ranges and will install:
- `faiss-cpu>=1.8.0` (any version 1.8.0 or higher)
- Latest compatible versions of all libraries

### Option 2: Install Specific Versions (If you have issues)
```bash
pip install openai==1.12.0
pip install langchain==0.1.6
pip install langchain-openai==0.0.5
pip install faiss-cpu==1.8.0
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install python-dotenv==1.0.0
pip install streamlit==1.31.0
pip install tiktoken==0.5.2
```

### Option 3: Install Latest Versions (Most Compatible)
```bash
pip install openai langchain langchain-openai faiss-cpu numpy pandas python-dotenv streamlit tiktoken
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: FAISS Installation Fails
**Error:** `ERROR: Could not find a version that satisfies the requirement faiss-cpu`

**Solution A:** Install latest version
```bash
pip install faiss-cpu
```

**Solution B:** Try specific available version
```bash
# Check available versions
pip index versions faiss-cpu

# Install a specific one (e.g., 1.8.0, 1.9.0, 1.10.0, 1.11.0, or 1.12.0)
pip install faiss-cpu==1.8.0
```

**Solution C:** If using M1/M2 Mac
```bash
# Use conda instead
conda install -c conda-forge faiss-cpu
```

---

### Issue 2: NumPy Version Conflict
**Error:** `ERROR: numpy 2.0.0 is not compatible`

**Solution:**
```bash
pip install "numpy>=1.24.0,<2.0.0"
```

---

### Issue 3: LangChain Compatibility
**Error:** `ImportError: cannot import name 'ChatOpenAI'`

**Solution:** Upgrade LangChain packages
```bash
pip install --upgrade langchain langchain-openai
```

---

### Issue 4: Pip Outdated Warning
**Warning:** `A new release of pip is available`

**Solution:** Update pip (optional but recommended)
```bash
python -m pip install --upgrade pip
```

---

## 🔍 Verify Installation

After installing, verify everything works:

```bash
python -c "import faiss; print('FAISS version:', faiss.__version__)"
python -c "import langchain; print('LangChain version:', langchain.__version__)"
python -c "import openai; print('OpenAI version:', openai.__version__)"
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
```

Expected output:
```
FAISS version: 1.8.0 (or higher)
LangChain version: 0.1.6 (or higher)
OpenAI version: 1.12.0 (or higher)
Streamlit version: 1.31.0 (or higher)
```

---

## 🐍 Python Version Requirements

**Minimum:** Python 3.8
**Recommended:** Python 3.9, 3.10, or 3.11
**Note:** Python 3.12+ might have compatibility issues with some libraries

Check your version:
```bash
python --version
```

If you need a different Python version:
- **Windows:** Download from https://www.python.org/downloads/
- **Mac:** Use `brew install python@3.11`
- **Linux:** Use `sudo apt install python3.11`

---

## 💡 Virtual Environment (Recommended)

To avoid conflicts with other projects:

### Create Virtual Environment
```bash
# Create
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

---

## ✅ Complete Fresh Installation

Start from scratch if you're having multiple issues:

```bash
# 1. Update pip
python -m pip install --upgrade pip

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# 3. Install packages one by one
pip install python-dotenv
pip install openai
pip install langchain
pip install langchain-openai
pip install faiss-cpu
pip install numpy
pip install pandas
pip install streamlit
pip install tiktoken

# 4. Verify
python -c "import faiss, langchain, openai, streamlit; print('All imports successful!')"
```

---

## 🔄 Already Installed? Update to Fixed Version

If you already downloaded and want the fix:

```bash
# Just update the problematic package
pip install --upgrade faiss-cpu

# Or reinstall all with updated versions
pip install --upgrade -r requirements.txt
```

---

## 📦 Alternative: Use Conda

If pip installation keeps failing, try conda:

```bash
# Install Anaconda or Miniconda first, then:
conda create -n it-support python=3.10
conda activate it-support

# Install packages
conda install -c conda-forge faiss-cpu
pip install openai langchain langchain-openai streamlit python-dotenv tiktoken pandas
```

---

## 🆘 Still Having Issues?

### Debug Information
Run this to get debug info:
```bash
python --version
pip --version
pip list | grep -E "faiss|langchain|openai|streamlit"
```

### Common Solutions by Error Type

**"No module named 'faiss'"**
→ Run: `pip install faiss-cpu`

**"No module named 'langchain_openai'"**
→ Run: `pip install langchain-openai`

**"cannot import name 'ChatOpenAI'"**
→ Run: `pip install --upgrade langchain-openai`

**"ImportError: DLL load failed"** (Windows)
→ Install Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe

**"Symbol not found"** (Mac M1/M2)
→ Use conda: `conda install -c conda-forge faiss-cpu`

---

## ✅ Updated requirements.txt

The fixed `requirements.txt` now contains:
```
openai>=1.12.0
langchain>=0.1.0
langchain-openai>=0.0.5
faiss-cpu>=1.8.0
numpy>=1.24.0,<2.0.0
pandas>=2.0.0
python-dotenv>=1.0.0
streamlit>=1.31.0
tiktoken>=0.5.0
```

This uses flexible version ranges (>=) so it will install the latest compatible versions.

---

## 🎉 After Successful Installation

Once everything is installed, proceed with:

```bash
python generate_mock_data.py
python build_vector_store.py
streamlit run app.py
```

---

**The issue has been fixed in the updated ZIP file!**
