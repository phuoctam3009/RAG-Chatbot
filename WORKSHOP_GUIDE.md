# WORKSHOP 4: Building Chatbot RAG Systems
## IT Support Chatbot with Vector Store, LangChain & Function Calling

---

## Workshop Overview

### Objectives
By the end of this workshop, participants will:
1. Understand RAG (Retrieval-Augmented Generation) architecture
2. Build and query vector stores using FAISS
3. Implement LangChain for prompt and chain management
4. Use Azure OpenAI function calling to extend chatbot capabilities
5. Deploy a production-ready chatbot with UI

### Duration
4 hours (including breaks)

### Prerequisites
- Python programming experience (intermediate level)
- Basic understanding of machine learning concepts
- Azure OpenAI account (or OpenAI API key)
- Laptop with Python 3.8+

---

## Part 1: Introduction to RAG Systems (30 minutes)

### What is RAG?

**Retrieval-Augmented Generation** combines:
- **Retrieval**: Finding relevant documents from a knowledge base
- **Generation**: Using LLM to generate contextual responses

### Why RAG?

**Problems with vanilla LLMs:**
- Limited to training data (knowledge cutoff)
- Cannot access proprietary/recent information
- May hallucinate facts
- Cannot cite sources

**RAG Benefits:**
- Up-to-date information from documents
- Reduces hallucinations
- Provides source attribution
- Cost-effective (less fine-tuning needed)

### RAG Architecture

```
User Query → Vector Search → Retrieve Relevant Docs → 
Augment Prompt → LLM Generation → Response with Sources
```

### Real-World Applications
- Customer support chatbots
- Internal knowledge bases
- Document Q&A systems
- Technical support automation
- Legal document analysis

---

## Part 2: Understanding Vector Stores (45 minutes)

### What are Vector Embeddings?

Text converted to numerical vectors that capture semantic meaning:
- Similar meanings = Similar vectors
- Enable semantic search (not just keyword matching)

Example:
```
"password reset" ≈ "forgot my password" ≈ "can't login"
```

### Vector Store Options

| Store | Type | Best For |
|-------|------|----------|
| FAISS | In-memory | Fast, local development |
| Pinecone | Cloud | Production, scalability |
| Weaviate | Open-source | Self-hosted production |
| Chroma | In-memory/persistent | Lightweight projects |
| Milvus | Distributed | Large-scale applications |

### Hands-On: Building Vector Store

**Step 1: Create Knowledge Base**
```python
# See generate_mock_data.py
# 15 IT support articles covering common issues
```

**Step 2: Generate Embeddings**
```python
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002"
)
```

**Step 3: Build FAISS Index**
```python
from langchain.vectorstores import FAISS

vector_store = FAISS.from_documents(
    documents=documents,
    embedding=embeddings
)
```

**Step 4: Query**
```python
results = vector_store.similarity_search(
    "How do I reset my password?", 
    k=3
)
```

### Exercise 1: Vector Store Experimentation
- Run `python build_vector_store.py`
- Test different queries
- Compare similarity scores
- Adjust k parameter

---

## Part 3: LangChain Integration (60 minutes)

### Why LangChain?

**LangChain simplifies:**
- Prompt template management
- Chain construction (retrieval + generation)
- Memory management (conversation history)
- Tool/function integration

### Key Components

**1. Prompt Templates**
```python
template = """You are an IT Support Assistant.
Use the following context: {context}
Question: {question}
Answer:"""
```

**2. Retrieval Chain**
```python
from langchain.chains import ConversationalRetrievalChain

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vector_store.as_retriever(),
    memory=memory
)
```

**3. Conversation Memory**
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
```

### Hands-On: Building the Chain

**Step 1: Initialize LLM**
```python
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    azure_deployment="gpt-4",
    temperature=0.3
)
```

**Step 2: Configure Retriever**
```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Top 3 results
)
```

**Step 3: Create Chain**
```python
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True
)
```

**Step 4: Query**
```python
result = chain({"question": "How do I reset my password?"})
print(result["answer"])
print(result["source_documents"])
```

### Exercise 2: Chain Testing
- Modify prompt template
- Test conversation memory
- Adjust retrieval parameters
- Compare response quality

---

## Part 4: Function Calling (60 minutes)

### What is Function Calling?

Allows LLMs to:
- Execute external functions
- Access real-time data
- Perform actions (create tickets, check status)
- Integrate with APIs

### Function Definition Format

```python
{
    "name": "create_support_ticket",
    "description": "Create a new IT support ticket",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Brief issue title"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "critical"]
            }
        },
        "required": ["title"]
    }
}
```

### Implementing Functions

**1. Define Function**
```python
def create_support_ticket(title: str, description: str, 
                         category: str, priority: str) -> Dict:
    ticket = {
        "ticket_id": f"INC{counter}",
        "title": title,
        "status": "open",
        "created_at": datetime.now()
    }
    return ticket
```

**2. Register with LLM**
```python
llm = AzureChatOpenAI(
    model_kwargs={
        "functions": FUNCTION_DEFINITIONS,
        "function_call": "auto"
    }
)
```

**3. Handle Function Calls**
```python
if response.get("function_call"):
    function_name = response["function_call"]["name"]
    arguments = json.loads(response["function_call"]["arguments"])
    result = execute_function(function_name, arguments)
```

### Our Implemented Functions

1. **create_support_ticket**: Create tickets for unresolved issues
2. **check_ticket_status**: Query ticket information
3. **check_system_status**: Monitor system health
4. **search_employee_directory**: Find IT staff contacts

### Exercise 3: Function Implementation
- Add new function (e.g., schedule_maintenance)
- Test function execution
- Integrate with chatbot
- Handle errors gracefully

---

## Part 5: Building the Complete Chatbot (60 minutes)

### System Architecture Review

```
┌─────────────────┐
│   Streamlit UI  │
└────────┬────────┘
         │
┌────────▼──────────────────────┐
│   ITSupportChatbot Class      │
│  ┌──────────────────────────┐ │
│  │ ConversationalRetrieval  │ │
│  │        Chain             │ │
│  └──────────────────────────┘ │
└────┬──────────────────┬───────┘
     │                  │
┌────▼─────┐     ┌──────▼────────┐
│  FAISS   │     │ Azure OpenAI  │
│  Vector  │     │  + Functions  │
│  Store   │     └───────────────┘
└──────────┘
```

### Key Implementation Details

**1. Chatbot Class Structure**
```python
class ITSupportChatbot:
    def __init__(self):
        self.llm = ...
        self.vector_store = ...
        self.memory = ...
        self.chain = ...
    
    def process_message(self, user_message):
        # Main query processing
        pass
    
    def call_function(self, function_name, arguments):
        # Function execution
        pass
```

**2. Error Handling**
```python
try:
    result = self.chain({"question": user_message})
except Exception as e:
    return f"Error: {str(e)}", [], None
```

**3. Source Attribution**
```python
source_docs = result.get("source_documents", [])
for doc in source_docs:
    print(f"Source: {doc.metadata['title']}")
```

### Exercise 4: Full Integration
- Run complete chatbot: `python chatbot.py`
- Test various scenarios
- Monitor source retrieval
- Test function calling

---

## Part 6: UI Development with Streamlit (45 minutes)

### Why Streamlit?

- Rapid prototyping
- Python-native (no HTML/CSS/JS needed)
- Interactive widgets
- Easy deployment

### Key UI Components

**1. Chat Interface**
```python
user_input = st.chat_input("Type your question...")
if user_input:
    response = chatbot.process_message(user_input)
    st.write(response)
```

**2. Sidebar Tools**
```python
with st.sidebar:
    st.header("IT Support Tools")
    # Ticket creation
    # System status
    # Directory search
```

**3. Session State**
```python
if 'messages' not in st.session_state:
    st.session_state.messages = []
```

### Hands-On: Launch UI

```bash
streamlit run app.py
```

Features to explore:
- Chat with the bot
- Create support tickets
- Check system status
- Search employee directory
- View knowledge base sources

### Exercise 5: UI Customization
- Modify color scheme
- Add new sidebar widget
- Enhance message display
- Add analytics dashboard

---

## Part 7: Testing & Evaluation (30 minutes)

### Testing Strategy

**1. Unit Tests**
- Vector store retrieval accuracy
- Function execution correctness
- Prompt template validation

**2. Integration Tests**
- End-to-end chat flow
- Function calling chain
- Error handling

**3. User Acceptance Testing**
- Response quality
- Source relevance
- User experience

### Evaluation Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Retrieval Accuracy | >85% | Relevant docs in top 3 |
| Response Time | <3s | Average query time |
| Function Success Rate | >95% | Successful executions |
| User Satisfaction | >4/5 | Feedback scores |

### Using the Jupyter Notebook

```bash
jupyter notebook IT_Support_Chatbot_Demo.ipynb
```

Notebook includes:
- Vector store analysis
- Similarity scoring
- Batch testing
- Performance metrics

### Exercise 6: Testing
- Run batch tests
- Measure response times
- Evaluate retrieval accuracy
- Identify improvement areas

---

## Part 8: Production Deployment (30 minutes)

### Deployment Checklist

**1. Security**
- [ ] Environment variables (.env)
- [ ] API key rotation
- [ ] Rate limiting
- [ ] Input validation

**2. Scalability**
- [ ] Cloud vector store (Pinecone)
- [ ] Load balancing
- [ ] Caching strategy
- [ ] Database for tickets

**3. Monitoring**
- [ ] Logging
- [ ] Analytics
- [ ] Error tracking
- [ ] User feedback

### Deployment Options

**Option 1: Azure Web App**
```bash
az webapp up --name it-support-chatbot --resource-group myRG
```

**Option 2: Docker Container**
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

**Option 3: Streamlit Cloud**
- Push to GitHub
- Connect to Streamlit Cloud
- Add secrets (environment variables)
- Deploy

### Cost Optimization

**Estimated Monthly Costs (1000 queries):**
- Azure OpenAI (GPT-4): $50-150
- FAISS (self-hosted): $0
- Streamlit hosting: $0-20

**Optimization tips:**
- Use GPT-3.5-turbo for non-critical queries
- Cache frequent queries
- Batch embeddings generation
- Use smaller embedding models

---

## Part 9: Advanced Topics (30 minutes)

### 1. Hybrid Search

Combine semantic + keyword search:
```python
# BM25 for keywords + FAISS for semantic
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever],
    weights=[0.3, 0.7]
)
```

### 2. Re-ranking

Improve result quality:
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)
```

### 3. Multi-modal RAG

Handle images, PDFs, tables:
- Document parsing (PyPDF, docx)
- Image embeddings (CLIP)
- Table extraction

### 4. Evaluation Framework

```python
from langchain.evaluation import load_evaluator

evaluator = load_evaluator("qa")
result = evaluator.evaluate_strings(
    prediction=answer,
    input=question,
    reference=ground_truth
)
```

### 5. Fine-tuning Embeddings

- Train custom embedding model
- Domain-specific vectors
- Improve retrieval accuracy

---

## Part 10: Q&A and Project Showcase (30 minutes)

### Project Requirements Recap

**Deliverables:**
✅ Clearly defined problem statement
✅ Mock data schema and generation
✅ Vector store (FAISS) populated with embeddings
✅ LangChain configuration
✅ Azure OpenAI function call integration
✅ Functional chatbot prototype with UI

### Success Criteria

- [ ] Chatbot answers 80%+ of test queries correctly
- [ ] Sources are relevant and cited
- [ ] Functions execute successfully
- [ ] UI is intuitive and responsive
- [ ] Code is documented and maintainable

### Next Steps

**Immediate:**
1. Expand knowledge base (add more articles)
2. Implement additional functions
3. Enhance UI/UX
4. Add authentication

**Short-term:**
5. Deploy to staging environment
6. User testing and feedback
7. Performance optimization
8. Integration with ticketing system

**Long-term:**
9. Multi-language support
10. Voice interface
11. Mobile app
12. Analytics dashboard

---

## Resources

### Documentation
- LangChain: https://python.langchain.com/docs
- FAISS: https://github.com/facebookresearch/faiss
- Azure OpenAI: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- Streamlit: https://docs.streamlit.io

### Tutorials
- RAG from scratch: https://python.langchain.com/docs/use_cases/question_answering/
- Function calling: https://platform.openai.com/docs/guides/function-calling

### Community
- LangChain Discord
- Stack Overflow
- GitHub Issues

---

## Conclusion

You've learned to:
1. ✅ Build RAG systems with vector stores
2. ✅ Use LangChain for chain management
3. ✅ Implement function calling
4. ✅ Create production-ready chatbots
5. ✅ Deploy with modern UI

**Key Takeaways:**
- RAG solves LLM knowledge limitations
- Vector stores enable semantic search
- LangChain simplifies complex chains
- Function calling extends capabilities
- Testing and evaluation are critical

**Thank you for participating!**

---

## Contact & Support

**Instructor:** [Your Name]
**Email:** [Your Email]
**Workshop Materials:** [GitHub Repository]
**Support:** [Workshop Slack/Discord]

---

*Workshop materials © 2025 - For educational purposes*
