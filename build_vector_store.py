import os
import json
from typing import List, Dict
from dotenv import load_dotenv

# Updated imports for newer LangChain versions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Load environment variables
load_dotenv()

# Determine which API to use
USE_AZURE = os.getenv("AZURE_OPENAI_API_KEY") is not None
USE_OPENAI = os.getenv("OPENAI_API_KEY") is not None

if USE_AZURE:
    from langchain_openai import AzureOpenAIEmbeddings
    print("✓ Using Azure OpenAI")
elif USE_OPENAI:
    from langchain_openai import OpenAIEmbeddings
    print("✓ Using OpenAI API")
else:
    raise ValueError("Please set either OPENAI_API_KEY or AZURE_OPENAI_API_KEY in .env file")

class VectorStoreBuilder:
    """Build and manage FAISS vector store for IT knowledge base"""
    
    def __init__(self):
        # Initialize embeddings based on available credentials
        if USE_AZURE:
            self.embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
            )
        else:  # Use regular OpenAI
            # Use separate key for embeddings if available
            embedding_key = os.getenv("OPENAI_EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY")
            embedding_base_url = os.getenv("OPENAI_EMBEDDING_BASE_URL") or os.getenv("OPENAI_BASE_URL")
            
            embedding_kwargs = {
                "api_key": embedding_key,
                "model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            }
            
            # Add base_url if provided
            if embedding_base_url:
                embedding_kwargs["base_url"] = embedding_base_url
            
            self.embeddings = OpenAIEmbeddings(**embedding_kwargs)
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def load_knowledge_base(self, file_path: str = "it_knowledge_base.json") -> List[Dict]:
        """Load IT knowledge base from JSON"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def prepare_documents(self, knowledge_base: List[Dict]) -> List[Document]:
        """Convert knowledge base to LangChain documents"""
        documents = []
        
        for article in knowledge_base:
            # Create comprehensive text for embedding
            text = f"""
Title: {article['title']}
Category: {article['category']}
ID: {article['id']}

{article['content']}

Tags: {', '.join(article['tags'])}
"""
            
            # Create metadata
            metadata = {
                'id': article['id'],
                'category': article['category'],
                'title': article['title'],
                'tags': article['tags'],
                'related_issues': article.get('related_issues', [])
            }
            
            # Split long documents
            chunks = self.text_splitter.split_text(text)
            
            for i, chunk in enumerate(chunks):
                chunk_metadata = metadata.copy()
                chunk_metadata['chunk'] = i
                documents.append(Document(page_content=chunk, metadata=chunk_metadata))
        
        return documents
    
    def build_vector_store(self, documents: List[Document]) -> FAISS:
        """Build FAISS vector store from documents"""
        print("Building FAISS vector store...")
        print(f"Total document chunks: {len(documents)}")
        
        vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        print("Vector store built successfully!")
        return vector_store
    
    def save_vector_store(self, vector_store: FAISS, path: str = "faiss_index"):
        """Save FAISS index to disk"""
        vector_store.save_local(path)
        print(f"Vector store saved to {path}/")
    
    def load_vector_store(self, path: str = "faiss_index") -> FAISS:
        """Load FAISS index from disk"""
        vector_store = FAISS.load_local(
            path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"Vector store loaded from {path}/")
        return vector_store

def main():
    """Build and save the vector store"""
    builder = VectorStoreBuilder()
    
    # Load knowledge base
    print("Loading knowledge base...")
    kb = builder.load_knowledge_base()
    print(f"Loaded {len(kb)} articles")
    
    # Prepare documents
    print("\nPreparing documents...")
    documents = builder.prepare_documents(kb)
    print(f"Created {len(documents)} document chunks")
    
    # Build vector store
    print("\nBuilding vector store...")
    vector_store = builder.build_vector_store(documents)
    
    # Save vector store
    print("\nSaving vector store...")
    builder.save_vector_store(vector_store)
    
    # Test retrieval
    print("\n" + "="*50)
    print("Testing retrieval...")
    test_query = "How do I reset my password?"
    results = vector_store.similarity_search(test_query, k=3)
    
    print(f"\nQuery: {test_query}")
    print(f"Found {len(results)} relevant documents:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.metadata['title']} (ID: {doc.metadata['id']})")
        print(f"   Category: {doc.metadata['category']}")
        print(f"   Content preview: {doc.page_content[:150]}...")
    
    print("\n" + "="*50)
    print("Vector store creation complete!")

if __name__ == "__main__":
    main()