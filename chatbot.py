"""
IT Support Chatbot with RAG, LangChain, and Function Calling
Supports both OpenAI API and Azure OpenAI
Updated to use modern LangChain LCEL
"""

import os
import json
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.documents import Document
from function_calling import FUNCTION_DEFINITIONS, execute_function

# Load environment variables
load_dotenv()

# Determine which API to use
USE_AZURE = os.getenv("AZURE_OPENAI_API_KEY") is not None
USE_OPENAI = os.getenv("OPENAI_API_KEY") is not None

if USE_AZURE:
    print("✓ Using Azure OpenAI")
elif USE_OPENAI:
    print("✓ Using OpenAI API")
else:
    raise ValueError("Please set either OPENAI_API_KEY or AZURE_OPENAI_API_KEY in .env file")

class ITSupportChatbot:
    """
    RAG-based IT Support Chatbot with function calling capabilities
    Supports both OpenAI API and Azure OpenAI
    Uses modern LangChain LCEL
    """
    
    def __init__(self, vector_store_path: str = "faiss_index"):
        """Initialize the chatbot with vector store and LLM"""
        
        # Initialize LLM based on available credentials
        if USE_AZURE:
            self.llm = AzureChatOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                temperature=0.3
            )
            
            self.embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
            )
        else:  # Use regular OpenAI
            # Chat LLM setup
            chat_base_url = os.getenv("OPENAI_BASE_URL")
            chat_kwargs = {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                "temperature": 0.3
            }
            if chat_base_url:
                chat_kwargs["base_url"] = chat_base_url
            
            self.llm = ChatOpenAI(**chat_kwargs)
            
            # Embeddings setup
            embedding_key = os.getenv("OPENAI_EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY")
            embedding_base_url = os.getenv("OPENAI_EMBEDDING_BASE_URL") or os.getenv("OPENAI_BASE_URL")
            
            embedding_kwargs = {
                "api_key": embedding_key,
                "model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            }
            if embedding_base_url:
                embedding_kwargs["base_url"] = embedding_base_url
            
            self.embeddings = OpenAIEmbeddings(**embedding_kwargs)
        
        # Load vector store
        self.vector_store = self._load_vector_store(vector_store_path)
        
        # Initialize retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # Initialize chat history
        self.chat_history = []
        
        # Create the RAG chain
        self.chain = self._create_chain()
        
        print("✓ IT Support Chatbot initialized successfully!")
    
    def _load_vector_store(self, path: str) -> FAISS:
        """Load FAISS vector store"""
        try:
            vector_store = FAISS.load_local(
                path,
                embeddings=self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"✓ Vector store loaded from {path}/")
            return vector_store
        except Exception as e:
            print(f"✗ Error loading vector store: {e}")
            print("Please run build_vector_store.py first")
            raise
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Format documents for context"""
        formatted = []
        for i, doc in enumerate(docs, 1):
            article_id = doc.metadata.get("id", "N/A")
            title = doc.metadata.get("title", "N/A")
            category = doc.metadata.get("category", "N/A")
            content = doc.page_content
            
            formatted.append(
                f"Article {i} (ID: {article_id}):\n"
                f"Title: {title}\n"
                f"Category: {category}\n"
                f"Content: {content}\n"
            )
        return "\n---\n".join(formatted)
    
    def _format_chat_history(self) -> str:
        """Format chat history for prompt"""
        if not self.chat_history:
            return "No previous conversation."
        
        formatted = []
        for msg in self.chat_history[-6:]:  # Last 3 exchanges
            if isinstance(msg, HumanMessage):
                formatted.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                formatted.append(f"Assistant: {msg.content}")
        return "\n".join(formatted)
    
    def _create_chain(self):
        """Create the RAG chain using LCEL"""
        
        prompt = ChatPromptTemplate.from_template("""You are an IT Support Assistant for a company. Your role is to help employees with technical issues using the knowledge base provided.

Use the following context from the IT knowledge base to answer the question:

Context:
{context}

Instructions:
1. Provide clear, step-by-step solutions when available in the knowledge base
2. If the issue cannot be resolved with available information, offer to create a support ticket
3. Be professional, friendly, and empathetic
4. Reference the knowledge base article ID when providing solutions
5. If the user wants to check system status, create tickets, or search employee directory, use the appropriate functions
6. Always verify you understood the issue correctly before providing solutions

Chat History:
{chat_history}

User Question: {question}

Helpful Answer:""")
        
        # Create the chain
        chain = (
            RunnableParallel(
                context=lambda x: self._format_docs(self.retriever.invoke(x["question"])),
                chat_history=lambda x: self._format_chat_history(),
                question=lambda x: x["question"]
            )
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain
    
    def process_message(self, user_message: str) -> Tuple[str, List[Dict], Optional[Dict]]:
        """
        Process user message and return response
        
        Args:
            user_message: The user's question or message
        
        Returns:
            Tuple of (response_text, source_documents, function_call_result)
        """
        try:
            # Get relevant documents
            source_docs = self.retriever.invoke(user_message)
            
            # Get response from chain
            response_text = self.chain.invoke({"question": user_message})
            
            # Update chat history
            self.chat_history.append(HumanMessage(content=user_message))
            self.chat_history.append(AIMessage(content=response_text))
            
            # Keep only last 10 messages (5 exchanges)
            if len(self.chat_history) > 10:
                self.chat_history = self.chat_history[-10:]
            
            # Check if function calling is needed (simplified for this example)
            function_result = None
            
            # Format source documents
            formatted_sources = []
            for doc in source_docs:
                formatted_sources.append({
                    "id": doc.metadata.get("id", "N/A"),
                    "title": doc.metadata.get("title", "N/A"),
                    "category": doc.metadata.get("category", "N/A"),
                    "content_preview": doc.page_content[:200] + "..."
                })
            
            return response_text, formatted_sources, function_result
            
        except Exception as e:
            error_msg = f"I encountered an error processing your request: {str(e)}"
            return error_msg, [], None
    
    def call_function(self, function_name: str, arguments: Dict) -> Dict:
        """
        Execute a function call
        
        Args:
            function_name: Name of the function to call
            arguments: Function arguments
        
        Returns:
            Function execution result
        """
        result_json = execute_function(function_name, arguments)
        return json.loads(result_json)
    
    def get_relevant_articles(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve relevant knowledge base articles
        
        Args:
            query: Search query
            k: Number of articles to return
        
        Returns:
            List of relevant articles with metadata
        """
        docs = self.vector_store.similarity_search(query, k=k)
        
        articles = []
        seen_ids = set()
        
        for doc in docs:
            article_id = doc.metadata.get("id")
            if article_id not in seen_ids:
                articles.append({
                    "id": article_id,
                    "title": doc.metadata.get("title"),
                    "category": doc.metadata.get("category"),
                    "preview": doc.page_content[:300] + "..."
                })
                seen_ids.add(article_id)
        
        return articles
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.chat_history = []
        print("✓ Conversation history cleared")

def main():
    """Test the chatbot"""
    print("="*70)
    print("IT SUPPORT CHATBOT - Testing")
    print("="*70)
    
    # Initialize chatbot
    chatbot = ITSupportChatbot()
    
    # Test queries
    test_queries = [
        "How do I reset my password?",
        "My computer is running slow, what should I do?",
        "I can't connect to the VPN",
        "How do I setup email on my iPhone?",
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"User: {query}")
        print(f"{'='*70}")
        
        response, sources, func_result = chatbot.process_message(query)
        
        print(f"\nAssistant: {response}")
        
        if sources:
            print(f"\n📚 Knowledge Base Sources:")
            for source in sources[:2]:  # Show top 2 sources
                print(f"   • {source['title']} (ID: {source['id']})")
                print(f"     Category: {source['category']}")
        
        print()
    
    print("="*70)
    print("Test completed!")

if __name__ == "__main__":
    main()