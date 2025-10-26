# IT Support Chatbot

A RAG-based IT support chatbot using FAISS vector store, LangChain, and OpenAI/Azure OpenAI.

## Features

- **Semantic Search**: Finds relevant IT articles using vector similarity
- **Similarity Filtering**: Only uses documents that match well with queries
- **Conversation Memory**: Maintains context across chat exchanges
- **Dual API Support**: Works with both OpenAI API and Azure OpenAI
- **Web Interface**: Clean Streamlit UI with knowledge base explorer
- **Smart Responses**: Honest answers when information isn't available

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Configuration

Create `.env` file:

**For OpenAI API:**

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

**For Azure OpenAI:**

```env
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your-embedding-deployment
```

### 3. Build Vector Store

```bash
python generate_mock_data.py
python build_vector_store.py
```

### 4. Run Application

```bash
streamlit run app.py
```

Visit `http://localhost:8501`

## Usage

### Basic Query

```python
from chatbot import ITSupportChatbot

chatbot = ITSupportChatbot()
response, sources, _ = chatbot.process_message("How do I reset my password?")

print(response)
for source in sources:
    print(f"- {source['title']}")
```

### Custom Threshold

```python
# Stricter filtering
chatbot = ITSupportChatbot(similarity_threshold=0.8)

# More lenient
chatbot = ITSupportChatbot(similarity_threshold=0.6)
```

### Conversation Management

```python
# Chat
response1, _, _ = chatbot.process_message("How do I reset password?")
response2, _, _ = chatbot.process_message("What if email doesn't arrive?")

# Clear history
chatbot.reset_conversation()
```

## System Requirements

- Python 3.8+
- 512MB+ RAM
- Internet connection for LLM API
- OpenAI API key or Azure OpenAI access

## File Structure

```
├── app.py                      # Streamlit UI
├── chatbot.py                  # Core chatbot logic
├── build_vector_store.py       # Vector store builder
├── generate_mock_data.py       # Data generator
├── requirements.txt            # Dependencies
├── .env                        # Configuration (create this)
├── it_knowledge_base.json      # Knowledge base (generated)
└── faiss_index/               # Vector store (generated)
```

## Configuration

### Similarity Threshold

Controls document relevance filtering:

| Value | Behavior                                |
| ----- | --------------------------------------- |
| 0.9   | Very strict - only near-perfect matches |
| 0.8   | Strict - recommended for production     |
| 0.7   | Balanced - default                      |
| 0.6   | Lenient - exploratory queries           |
| 0.5   | Very lenient - broad search             |

### LLM Settings

In `.env`:

- `OPENAI_MODEL`: Model name (gpt-4, gpt-4o-mini)
- `temperature`: Set in code (default: 0.3)

## Knowledge Base

The system includes 15 IT support articles covering:

- Password Reset & Account Issues
- VPN Connection Setup
- Software Installation
- Email Configuration
- Hardware Troubleshooting
- Network Connectivity
- Security & Phishing
- Mobile Device Setup
- Performance Optimization
- Multi-Factor Authentication

## API Methods

### ITSupportChatbot

**`__init__(vector_store_path="faiss_index", similarity_threshold=0.7)`**

- Initialize chatbot with vector store and threshold

**`process_message(user_message: str)`**

- Process query and return (response, sources, function_result)

**`get_relevant_articles(query: str, k=5)`**

- Retrieve relevant KB articles

**`reset_conversation()`**

- Clear conversation history

**`set_similarity_threshold(threshold: float)`**

- Update relevance threshold

## Troubleshooting

**Error: "Vector store not found"**

```bash
python build_vector_store.py
```

**Error: "API key not found"**

- Check `.env` file exists
- Verify API key is correct

**Poor responses:**

- Adjust similarity threshold
- Check knowledge base content
- Try different LLM model

**High API costs:**

- Use gpt-4o-mini instead of gpt-4
- Increase similarity threshold
- Implement caching

## Performance

- Response time: 1-4 seconds
- Memory usage: ~500MB
- Concurrent users: 10-50
- Knowledge base: 15-1000+ articles

## Security

- API keys in `.env` (not in code)
- `.env` excluded from git
- No persistent user data storage
- Safe FAISS deserialization

## Documentation

- **DOCUMENTATION.md**: Complete system documentation
- **TECHNICAL_REFERENCE.md**: Technical implementation details
- Code comments in source files

## License

Educational/Workshop purposes

## Version

2.1 - Production ready with similarity threshold filtering
