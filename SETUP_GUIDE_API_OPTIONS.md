# Setup Guide: OpenAI API vs Azure OpenAI

## 🔑 Understanding the Two Options

### Option 1: Regular OpenAI API (Simpler Setup)
✅ **You have:** API key, model name  
✅ **Best for:** Quick testing, personal projects, simpler setup  
✅ **Cost:** Pay-as-you-go based on usage  

### Option 2: Azure OpenAI (Enterprise Setup)
✅ **You have:** API key, endpoint, deployment names  
✅ **Best for:** Enterprise, production, Azure ecosystem integration  
✅ **Cost:** Azure subscription-based pricing  

---

## 🚀 Quick Setup - Choose Your Option

### OPTION 1: Using Regular OpenAI API (RECOMMENDED IF YOU JUST HAVE API KEY)

#### Step 1: Create .env file
```bash
# Create .env file
cat > .env << 'EOF'
# Regular OpenAI API
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
EOF
```

**Where to get your API key:**
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and paste above

#### Step 2: Use the flexible files
```bash
# Replace the original files with flexible versions
mv chatbot_flexible.py chatbot.py
mv build_vector_store_flexible.py build_vector_store.py

# Install dependencies
pip install -r requirements.txt

# Generate data and build vector store
python generate_mock_data.py
python build_vector_store.py

# Launch chatbot
streamlit run app.py
```

---

### OPTION 2: Using Azure OpenAI (If You Have Azure Deployment)

#### What are "Deployments" in Azure OpenAI?

In Azure, you don't use model names directly. Instead, you create **deployments**:

1. **Deployment** = A specific instance of a model in your Azure resource
2. You give each deployment a custom name (e.g., "my-gpt4", "my-embeddings")
3. You need TWO deployments:
   - One for chat (GPT-4 or GPT-3.5)
   - One for embeddings (text-embedding-ada-002)

#### How to Create Deployments (If You Don't Have Them)

**Step 1: Go to Azure OpenAI Studio**
- Visit: https://oai.azure.com
- Select your resource

**Step 2: Create Chat Deployment**
1. Click "Deployments" → "Create new deployment"
2. Select model: `gpt-4` or `gpt-35-turbo`
3. Give it a name: e.g., `gpt4-deployment`
4. Click "Create"
5. **Copy this deployment name** ← This is your `AZURE_OPENAI_DEPLOYMENT_NAME`

**Step 3: Create Embedding Deployment**
1. Click "Deployments" → "Create new deployment"
2. Select model: `text-embedding-ada-002`
3. Give it a name: e.g., `embeddings-deployment`
4. Click "Create"
5. **Copy this deployment name** ← This is your `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`

**Step 4: Get Your Credentials**
1. Go to "Keys and Endpoint" in Azure Portal
2. Copy:
   - API Key
   - Endpoint (looks like: https://your-resource.openai.azure.com/)

#### Step 5: Create .env file
```bash
# Create .env file
cat > .env << 'EOF'
# Azure OpenAI
AZURE_OPENAI_API_KEY=your-api-key-from-azure-portal
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt4-deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=embeddings-deployment
EOF
```

#### Step 6: Use the flexible files
```bash
# Replace the original files with flexible versions
mv chatbot_flexible.py chatbot.py
mv build_vector_store_flexible.py build_vector_store.py

# Install dependencies
pip install -r requirements.txt

# Generate data and build vector store
python generate_mock_data.py
python build_vector_store.py

# Launch chatbot
streamlit run app.py
```

---

## 📊 Comparison Table

| Feature | OpenAI API | Azure OpenAI |
|---------|-----------|--------------|
| **Setup Complexity** | ⭐ Simple | ⭐⭐⭐ Complex |
| **What You Need** | Just API key | API key + Endpoint + Deployments |
| **Configuration** | 3 variables | 5 variables |
| **Best For** | Testing, demos | Enterprise, production |
| **Pricing** | Pay per token | Azure subscription |
| **Enterprise Features** | Limited | Full (RBAC, VNet, etc.) |
| **Model Access** | Immediate | Request required |

---

## 🔧 Example .env Files

### ✅ Example 1: OpenAI API (Simpler)
```env
OPENAI_API_KEY=sk-proj-abc123xyz...
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
```

### ✅ Example 2: Azure OpenAI (Enterprise)
```env
AZURE_OPENAI_API_KEY=abc123def456...
AZURE_OPENAI_ENDPOINT=https://mycompany-openai.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt4-chat
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embeddings
```

---

## 🐛 Troubleshooting

### Error: "Please set either OPENAI_API_KEY or AZURE_OPENAI_API_KEY"
**Solution:** Create .env file with your credentials (see examples above)

### Error: "Deployment not found" (Azure)
**Solution:** 
1. Check deployment name is correct (case-sensitive)
2. Verify deployment exists in Azure Portal
3. Make sure you created BOTH deployments (chat + embeddings)

### Error: "Invalid API key"
**Solution:**
1. Verify API key is correct (no extra spaces)
2. For Azure: Check you're using the key from correct resource
3. For OpenAI: Generate new key from https://platform.openai.com/api-keys

### Error: "Model not found" (OpenAI)
**Solution:** 
1. Check you have access to the model (gpt-4 requires approval)
2. Try using `gpt-3.5-turbo` instead
3. Update .env: `OPENAI_MODEL=gpt-3.5-turbo`

---

## 💡 Which Should You Use?

### Use **OpenAI API** if:
- ✅ You just have an API key (starts with `sk-`)
- ✅ You want quick setup
- ✅ You're testing/learning
- ✅ You don't have Azure account

### Use **Azure OpenAI** if:
- ✅ Your company uses Azure
- ✅ You need enterprise features (RBAC, compliance, VNet)
- ✅ You already have Azure OpenAI resource
- ✅ You have deployments created

---

## 📝 Step-by-Step for Complete Beginners

### If you're using OpenAI API:

```bash
# 1. Get API key from https://platform.openai.com/api-keys

# 2. Create .env file
echo 'OPENAI_API_KEY=sk-your-key-here' > .env
echo 'OPENAI_MODEL=gpt-3.5-turbo' >> .env
echo 'OPENAI_EMBEDDING_MODEL=text-embedding-ada-002' >> .env

# 3. Replace files
cp chatbot_flexible.py chatbot.py
cp build_vector_store_flexible.py build_vector_store.py

# 4. Install and run
pip install -r requirements.txt
python generate_mock_data.py
python build_vector_store.py
streamlit run app.py
```

---

## 🎯 Summary

**The KEY difference:**
- **OpenAI API:** Direct model names (gpt-4, text-embedding-ada-002)
- **Azure OpenAI:** Custom deployment names (you create these in Azure Portal)

**If you only have:**
- API key + model name → Use **OpenAI API** (Option 1)
- API key + endpoint + deployment names → Use **Azure OpenAI** (Option 2)

**The flexible files (`chatbot_flexible.py` and `build_vector_store_flexible.py`) automatically detect which one you're using based on your .env file!**

---

## 📞 Still Need Help?

1. Check which variables you have
2. Look at the example .env files above
3. Choose the matching option
4. Copy the exact format
5. Replace only the values with your actual credentials

**Common mistake:** Mixing OpenAI and Azure variables in the same .env file. Use ONLY one set!

---

## ✅ Quick Test

After setup, test your configuration:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'); print('Azure Key:', 'SET' if os.getenv('AZURE_OPENAI_API_KEY') else 'NOT SET')"
```

This will show which API you're configured for.

---

**Need the flexible files?** They're included in the updated zip file below!
