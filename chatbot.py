"""
IT Support Chatbot with RAG and Similarity Threshold Filtering
Supports both OpenAI API and Azure OpenAI
"""

import os
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.documents import Document

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
    RAG-based IT Support Chatbot with similarity threshold filtering
    """
    
    def __init__(self, vector_store_path: str = "faiss_index", similarity_threshold: float = 0.7):
        """
        Initialize the chatbot
        
        Args:
            vector_store_path: Path to FAISS vector store directory
            similarity_threshold: Minimum similarity score (0-1) for document relevance
        """
        self.similarity_threshold = similarity_threshold
        self._initialize_llm()
        self.vector_store = self._load_vector_store(vector_store_path)
        self.chat_history = []
        self.chain = self._create_chain()
        print("✓ IT Support Chatbot initialized successfully!")
    
    def _initialize_llm(self):
        """Initialize LLM and embeddings based on environment configuration"""
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
        else:
            chat_kwargs = {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                "temperature": 0.3
            }
            if os.getenv("OPENAI_BASE_URL"):
                chat_kwargs["base_url"] = os.getenv("OPENAI_BASE_URL")
            self.llm = ChatOpenAI(**chat_kwargs)
            
            embedding_kwargs = {
                "api_key": os.getenv("OPENAI_EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY"),
                "model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            }
            if os.getenv("OPENAI_EMBEDDING_BASE_URL") or os.getenv("OPENAI_BASE_URL"):
                embedding_kwargs["base_url"] = os.getenv("OPENAI_EMBEDDING_BASE_URL") or os.getenv("OPENAI_BASE_URL")
            self.embeddings = OpenAIEmbeddings(**embedding_kwargs)
    
    def _load_vector_store(self, path: str) -> FAISS:
        """Load FAISS vector store from disk"""
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
            raise
    
    def _retrieve_with_threshold(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve documents filtered by similarity threshold
        
        Args:
            query: Search query
            k: Maximum number of documents to return
        
        Returns:
            List of documents meeting similarity threshold
        """
        docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k * 2)
        
        filtered_docs = []
        for doc, score in docs_with_scores:
            similarity = 1 / (1 + score)
            if similarity >= self.similarity_threshold:
                filtered_docs.append(doc)
                if len(filtered_docs) >= k:
                    break
        
        return filtered_docs
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Format documents for LLM context"""
        if not docs:
            return "No relevant information found in the knowledge base."
        
        formatted = []
        for i, doc in enumerate(docs, 1):
            formatted.append(
                f"Article {i} (ID: {doc.metadata.get('id', 'N/A')}):\n"
                f"Title: {doc.metadata.get('title', 'N/A')}\n"
                f"Category: {doc.metadata.get('category', 'N/A')}\n"
                f"Content: {doc.page_content}\n"
            )
        return "\n---\n".join(formatted)
    
    def _format_chat_history(self) -> str:
        """Format recent chat history for context"""
        if not self.chat_history:
            return "No previous conversation."
        
        formatted = []
        for msg in self.chat_history[-6:]:
            if isinstance(msg, HumanMessage):
                formatted.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                formatted.append(f"Assistant: {msg.content}")
        return "\n".join(formatted)
    
    def _create_chain(self):
        """Create RAG chain using LangChain LCEL"""
        prompt = ChatPromptTemplate.from_template("""You are an IT Support Assistant. Use the knowledge base context to answer questions.

Context:
{context}

Instructions:
1. If context contains relevant information, provide clear step-by-step solutions
2. If context says "No relevant information found", acknowledge this and offer general help
3. Be professional, friendly, and empathetic
4. Reference knowledge base article IDs when providing solutions
5. Never make up information not in the context

Chat History:
{chat_history}

User Question: {question}

Answer:""")
        
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
        Process user message and generate response
        
        Args:
            user_message: User's question
        
        Returns:
            Tuple of (response_text, source_documents, function_result)
        """
        try:
            source_docs = self._retrieve_with_threshold(user_message, k=3)
            response_text = self.chain.invoke({"question": user_message})
            
            self.chat_history.append(HumanMessage(content=user_message))
            self.chat_history.append(AIMessage(content=response_text))
            
            if len(self.chat_history) > 10:
                self.chat_history = self.chat_history[-10:]
            
            formatted_sources = [
                {
                    "id": doc.metadata.get("id", "N/A"),
                    "title": doc.metadata.get("title", "N/A"),
                    "category": doc.metadata.get("category", "N/A"),
                    "content_preview": doc.page_content[:200] + "..."
                }
                for doc in source_docs
            ]
            
            return response_text, formatted_sources, None
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            return error_msg, [], None
    
    def get_relevant_articles(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve relevant knowledge base articles
        
        Args:
            query: Search query (empty string returns all articles)
            k: Number of articles to return
        
        Returns:
            List of article metadata dictionaries
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
    
    def set_similarity_threshold(self, threshold: float):
        """
        Update similarity threshold
        
        Args:
            threshold: New threshold value (0-1)
        """
        if 0 <= threshold <= 1:
            self.similarity_threshold = threshold
        else:
            raise ValueError(f"Threshold must be between 0 and 1, got {threshold}")


if __name__ == "__main__":
    # Test the chatbot
    chatbot = ITSupportChatbot()
    response, sources, _ = chatbot.process_message("How do I reset my password?")
    print(f"\nResponse: {response}")
    print(f"\nSources: {len(sources)} documents")