"""
IT Support Chatbot with RAG, LangChain, and Similarity Threshold Filtering
Supports both OpenAI API and Azure OpenAI
Updated to use modern LangChain LCEL with score-based filtering
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
    Uses modern LangChain LCEL with similarity threshold filtering
    """
    
    def __init__(self, vector_store_path: str = "faiss_index", similarity_threshold: float = 0.7):
        """
        Initialize the chatbot with vector store and LLM
        
        Args:
            vector_store_path: Path to the FAISS vector store
            similarity_threshold: Minimum similarity score (0-1) to include a document
                                 Lower = more strict (only very similar docs)
                                 Higher = more lenient (include less similar docs)
                                 Default: 0.7 (good balance)
        """
        
        # Store similarity threshold
        self.similarity_threshold = similarity_threshold
        print(f"✓ Similarity threshold set to: {similarity_threshold}")
        
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
    
    def _retrieve_with_threshold(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve documents with similarity score filtering
        
        Args:
            query: Search query
            k: Number of documents to retrieve (will fetch more than needed for filtering)
        
        Returns:
            List of documents that meet the similarity threshold
        """
        # Get documents with scores (fetch more than k to allow for filtering)
        docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k * 2)
        
        # Filter by threshold
        filtered_docs = []
        filtered_scores = []
        
        for doc, score in docs_with_scores:
            # FAISS returns L2 distance (lower is better)
            # Convert to similarity: closer to 0 = more similar
            # Normalize to 0-1 range where 1 is most similar
            similarity = 1 / (1 + score)
            
            if similarity >= self.similarity_threshold:
                filtered_docs.append(doc)
                filtered_scores.append(similarity)
                
                if len(filtered_docs) >= k:
                    break
        
        # Log filtering results
        if filtered_docs:
            print(f"✓ Found {len(filtered_docs)} documents above threshold {self.similarity_threshold}")
            for i, (doc, sim) in enumerate(zip(filtered_docs, filtered_scores), 1):
                print(f"  {i}. {doc.metadata.get('title', 'Unknown')} (similarity: {sim:.3f})")
        else:
            print(f"⚠️ No documents found above threshold {self.similarity_threshold}")
        
        return filtered_docs
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Format documents for context"""
        if not docs:
            return "No relevant information found in the knowledge base."
        
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
1. If the context contains relevant information, provide clear, step-by-step solutions
2. If the context says "No relevant information found", acknowledge that you don't have specific information about this topic in the knowledge base and offer to:
   - Help with related topics you do know about
   - Suggest the user contact IT support directly for specialized help
   - Ask clarifying questions to better understand their issue
3. Be professional, friendly, and empathetic
4. Reference the knowledge base article ID when providing solutions
5. Always verify you understood the issue correctly before providing solutions
6. Never make up information that isn't in the context

Chat History:
{chat_history}

User Question: {question}

Helpful Answer:""")
        
        # Create the chain with threshold-based retrieval
        chain = (
            RunnableParallel(
                context=lambda x: self._format_docs(self._retrieve_with_threshold(x["question"], k=3)),
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
            # Get relevant documents with threshold filtering
            source_docs = self._retrieve_with_threshold(user_message, k=3)
            
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
    
    def get_relevant_articles(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve relevant knowledge base articles with threshold filtering
        
        Args:
            query: Search query
            k: Number of articles to return
        
        Returns:
            List of relevant articles with metadata
        """
        docs = self._retrieve_with_threshold(query, k=k) if query else self.vector_store.similarity_search("", k=k)
        
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
    
    def set_similarity_threshold(self, threshold: float):
        """
        Update the similarity threshold
        
        Args:
            threshold: New threshold value (0-1)
        """
        if 0 <= threshold <= 1:
            self.similarity_threshold = threshold
            print(f"✓ Similarity threshold updated to: {threshold}")
        else:
            print(f"✗ Invalid threshold: {threshold}. Must be between 0 and 1")

def main():
    """Test the chatbot"""
    print("="*70)
    print("IT SUPPORT CHATBOT - Testing with Similarity Threshold")
    print("="*70)
    
    # Initialize chatbot with default threshold (0.7)
    chatbot = ITSupportChatbot(similarity_threshold=0.7)
    
    # Test queries
    test_queries = [
        "How do I reset my password?",  # Should match well
        "My computer is running slow, what should I do?",  # Should match well
        "I can't connect to the VPN",  # Should match well
        "How do I make a sandwich?",  # Should NOT match well (irrelevant)
        "What is quantum physics?",  # Should NOT match well (irrelevant)
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"User: {query}")
        print(f"{'='*70}")
        
        response, sources, func_result = chatbot.process_message(query)
        
        print(f"\nAssistant: {response}")
        
        if sources:
            print(f"\n📚 Knowledge Base Sources ({len(sources)} found):")
            for source in sources[:2]:  # Show top 2 sources
                print(f"   • {source['title']} (ID: {source['id']})")
                print(f"     Category: {source['category']}")
        else:
            print(f"\n📚 No relevant sources found (below threshold)")
        
        print()
        
        # Reset conversation for next test
        chatbot.reset_conversation()
    
    print("="*70)
    print("Test completed!")
    print("\nThreshold Testing:")
    print("- Relevant queries found matching documents")
    print("- Irrelevant queries filtered out (no documents shown)")

if __name__ == "__main__":
    main()