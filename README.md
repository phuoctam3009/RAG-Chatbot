# IT Support Chatbot with RAG + LangChain + Function Calling

A production-ready IT support chatbot system using Retrieval-Augmented Generation (RAG), FAISS vector store, LangChain, and Azure OpenAI function calling to automate IT support and reduce operational costs.

## 🎯 Problem Statement

IT support teams are overwhelmed with repetitive questions about:
- Password resets
- Software installation
- VPN setup
- Email issues
- Hardware troubleshooting

**Solution:** An intelligent chatbot that provides instant answers using a knowledge base and can execute functions like creating tickets and checking system status.

## ✨ Features

### Core Capabilities
- **RAG System**: Retrieves relevant information from IT knowledge base
- **FAISS Vector Store**: Fast similarity search for document retrieval
- **LangChain Integration**: Manages prompts, chains, and conversation memory
- **Function Calling**: Extends chatbot with dynamic capabilities
- **Conversation Memory**: Maintains context across chat sessions

### Function Calling Capabilities
1. **Create Support Tickets**: Automatically create tickets for complex issues
2. **Check Ticket Status**: Query existing ticket information
3. **System Status Monitoring**: Check operational status of company systems
4. **Employee Directory**: Search for IT staff contact information

### Knowledge Base Coverage (15 Articles)
- Password Reset & Account Issues
- VPN Connection Setup
- Software Installation (Office 365, etc.)
- Email Configuration & Troubleshooting
- Hardware Issues (Printers, etc.)
- Network Connectivity
- Security & Phishing
- Mobile Device Setup
- Performance Optimization
- Multi-Factor Authentication

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Streamlit Web App)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   IT Support Chatbot                         │
│                    (chatbot.py)                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  LangChain ConversationalRetrievalChain             │   │
│  │  - Conversation Memory                               │   │
│  │  - Custom Prompt Template                            │   │
│  └─────────────────────────────────────────────────────┘   │
└───────┬───────────────────────────────────┬────────────────┘
        │                                   │
┌───────▼──────────┐              ┌─────────▼──────────────┐
│  Vector Store     │              │  Azure OpenAI GPT-4    │
│  (FAISS)          │              │  - Chat Completion     │
│                   │              │  - Function Calling    │
│  Embeddings:      │              │  - Embeddings          │
│  text-embedding-  │              └────────────────────────┘
│  ada-002          │
└───────────────────┘              ┌────────────────────────┐
                                   │  Function Calling       │
                                   │  (function_calling.py)  │
                                   │  - create_ticket()      │
                                   │  - check_status()       │
                                   │  - system_status()      │
                                   │  - search_directory()   │
                                   └────────────────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- Azure OpenAI account with:
  - GPT-4 or GPT-3.5 deployment
  - text-embedding-ada-002 deployment
- pip package manager

## 🚀 Quick Start

### 1. Clone/Download the Project

```bash
cd it-support-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Azure OpenAI

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI credentials:

```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
```

### 4. Generate Mock Data

```bash
python generate_mock_data.py
```

This creates:
- `it_knowledge_base.json` - 15 IT support articles
- `it_knowledge_base.csv` - Same data in CSV format

### 5. Build Vector Store

```bash
python build_vector_store.py
```

This creates the FAISS index in the `faiss_index/` directory.

Expected output:
```
Loading knowledge base...
Loaded 15 articles

Preparing documents...
Created 45 document chunks

Building FAISS vector store...
Total document chunks: 45
Vector store built successfully!

Saving vector store...
Vector store saved to faiss_index/

Testing retrieval...
Query: How do I reset my password?
Found 3 relevant documents...
```

### 6. Launch the Chatbot

```bash
streamlit run app.py
```

The web interface will open at `http://localhost:8501`

## 📁 Project Structure

```
it-support-chatbot/
│
├── app.py                      # Streamlit UI
├── chatbot.py                  # Main chatbot logic with RAG
├── function_calling.py         # Function definitions and implementations
├── build_vector_store.py       # FAISS vector store builder
├── generate_mock_data.py       # Mock data generator
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── faiss_index/               # FAISS vector store (created after build)
│   ├── index.faiss
│   └── index.pkl
│
├── it_knowledge_base.json     # Knowledge base data (created)
└── it_knowledge_base.csv      # Knowledge base data (created)
```

## 🎮 Usage Examples

### Example 1: Password Reset Question

**User:** "How do I reset my password?"

**Chatbot Response:**
```
To reset your company password:
1. Go to https://password.company.com
2. Click 'Forgot Password'
3. Enter your employee ID and registered email
...

📚 Knowledge Base Source: 
- How to Reset Your Password (ID: KB001)
```

### Example 2: Creating a Support Ticket

**User:** "I can't print and I've tried everything"

**Chatbot:** 
```
I understand you're having printing issues. Since you've already tried 
troubleshooting steps, let me create a support ticket for you.

Would you like me to create a ticket? I'll need:
- Brief description of the issue
- Which printer you're trying to use
- Priority level
```

### Example 3: Checking System Status

**User:** "Is the VPN working?"

**Chatbot:**
```
Let me check the VPN system status...

✅ VPN is operational
Uptime: 99.5%
Last incident: 5 days ago
```

## 🔧 Configuration

### Adjusting Retrieval Settings

In `chatbot.py`, modify the retriever parameters:

```python
retriever=self.vector_store.as_retriever(
    search_type="similarity",  # or "mmr" for Maximum Marginal Relevance
    search_kwargs={"k": 3}     # Number of documents to retrieve
)
```

### Customizing the Prompt

Edit the prompt template in `chatbot.py`:

```python
def _create_prompt_template(self) -> PromptTemplate:
    template = """You are an IT Support Assistant...
    
    # Customize your prompt here
    """
```

### Adding New Functions

1. Define the function in `function_calling.py`:

```python
def new_function(param1: str, param2: int) -> Dict:
    """Function description"""
    # Implementation
    return result
```

2. Add function definition to `FUNCTION_DEFINITIONS`:

```python
{
    "name": "new_function",
    "description": "What this function does",
    "parameters": {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "..."},
            "param2": {"type": "integer", "description": "..."}
        },
        "required": ["param1"]
    }
}
```

3. Add to `AVAILABLE_FUNCTIONS` dictionary

## 📊 Performance Metrics

### Expected Performance
- **Query Response Time**: 1-3 seconds
- **Retrieval Accuracy**: 85-95% (based on test queries)
- **Concurrent Users**: 10-50 (depends on Azure OpenAI tier)
- **Knowledge Base Size**: 15 articles (expandable to 1000+)

### Cost Estimation (Azure OpenAI)
- Embedding generation: ~$0.0001 per 1K tokens
- Chat completion: ~$0.03 per 1K tokens (GPT-4)
- Average conversation: $0.05 - $0.15

**Monthly cost for 1000 queries**: ~$50-150

## 🧪 Testing

### Test the Chatbot

```bash
python chatbot.py
```

This runs test queries and displays results.

### Test Individual Components

```python
# Test vector store
from build_vector_store import VectorStoreBuilder

builder = VectorStoreBuilder()
vector_store = builder.load_vector_store()
results = vector_store.similarity_search("password reset", k=3)

# Test function calling
from function_calling import create_support_ticket

ticket = create_support_ticket(
    title="Cannot access email",
    description="Outlook shows offline",
    category="email",
    priority="high"
)
print(ticket)
```

## 🐛 Troubleshooting

### Error: "Vector store not found"
**Solution:** Run `python build_vector_store.py` first

### Error: "Azure OpenAI authentication failed"
**Solution:** Check your `.env` file credentials

### Error: "Module not found"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Chatbot gives irrelevant answers
**Solution:** 
1. Check if vector store is built correctly
2. Adjust retrieval parameters (increase `k`)
3. Improve knowledge base content

### Slow response time
**Solution:**
1. Use GPT-3.5-turbo instead of GPT-4
2. Reduce number of retrieved documents
3. Implement caching for common queries

## 🔒 Security Considerations

- Store API keys in `.env` file (never commit to git)
- Add `.env` to `.gitignore`
- Use Azure RBAC for access control
- Implement rate limiting in production
- Validate user inputs before function calls
- Log all ticket creation for audit trail

## 📈 Future Enhancements

1. **Analytics Dashboard**: Track common issues and chatbot performance
2. **Multi-language Support**: Translate knowledge base and responses
3. **Voice Input**: Add speech-to-text capability
4. **Integration with ServiceNow**: Real ticket system integration
5. **Feedback Loop**: Learn from user feedback to improve responses
6. **Slack/Teams Bot**: Deploy as messaging platform bot
7. **Advanced Search**: Implement hybrid search (keyword + semantic)
8. **User Authentication**: Add SSO/Azure AD integration

## 📚 Data Schema

### Knowledge Base Article Schema

```json
{
  "id": "KB001",
  "category": "Password Reset",
  "title": "How to Reset Your Password",
  "content": "Detailed step-by-step instructions...",
  "tags": ["password", "reset", "login", "access"],
  "related_issues": ["account_locked", "email_access"]
}
```

### Support Ticket Schema

```json
{
  "ticket_id": "INC1000",
  "title": "Brief issue title",
  "description": "Detailed description",
  "category": "password|hardware|software|network|access|other",
  "priority": "low|medium|high|critical",
  "status": "open|in_progress|resolved|closed",
  "created_at": "2025-01-15 10:30:00",
  "estimated_resolution": "1-2 business days",
  "assigned_to": "IT Support Team"
}
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional knowledge base articles
- New function implementations
- UI/UX enhancements
- Performance optimizations
- Documentation improvements

## 📄 License

This project is for educational and workshop purposes.

## 👥 Team

Workshop 4: RAG Chatbot Systems
- Instructor: [Your Name]
- Students: [Team Members]

## 🎓 Learning Outcomes

By completing this workshop, you will:
1. ✅ Understand RAG architecture and implementation
2. ✅ Build and query vector stores with FAISS
3. ✅ Use LangChain for prompt and chain management
4. ✅ Implement Azure OpenAI function calling
5. ✅ Create production-ready chatbot with UI
6. ✅ Deploy scalable AI applications

## 📞 Support

For questions or issues:
- Check troubleshooting section
- Review Azure OpenAI documentation
- Contact workshop instructor

---

**Built with ❤️ using RAG, LangChain, FAISS, and Azure OpenAI**
