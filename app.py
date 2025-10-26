"""
Streamlit UI for IT Support Chatbot
Enhanced version with creative knowledge base stats and fixed common questions
"""

import streamlit as st
from chatbot import ITSupportChatbot
import json

# Page configuration
st.set_page_config(
    page_title="IT Support Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .source-card {
        background-color: #fff3e0;
        padding: 0.8rem;
        border-radius: 0.3rem;
        border-left: 3px solid #ff9800;
        margin: 0.5rem 0;
    }
    .function-result {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    .common-question-btn {
        background-color: #e3f2fd;
        padding: 0.8rem;
        border-radius: 0.5rem;
        border: 2px solid #1f77b4;
        cursor: pointer;
        margin: 0.5rem 0;
        transition: all 0.3s;
    }
    .common-question-btn:hover {
        background-color: #bbdefb;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    try:
        st.session_state.chatbot = ITSupportChatbot()
        st.session_state.initialized = True
    except Exception as e:
        st.session_state.initialized = False
        st.session_state.error = str(e)

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'show_kb_stats' not in st.session_state:
    st.session_state.show_kb_stats = False

# Header
st.markdown('<div class="main-header">🤖 IT Support Chatbot</div>', unsafe_allow_html=True)
st.markdown("---")

# Check initialization
if not st.session_state.get('initialized', False):
    st.error(f"⚠️ Failed to initialize chatbot: {st.session_state.get('error', 'Unknown error')}")
    st.info("💡 Please ensure you have:")
    st.markdown("""
    1. Created a `.env` file with your OpenAI or Azure OpenAI credentials
    2. Run `python build_vector_store.py` to create the vector store
    3. Installed all requirements: `pip install -r requirements.txt`
    """)
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚡ Quick Actions")
    
    # Clear Chat History
    if st.button("🔄 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chatbot.reset_conversation()
        st.rerun()
    
    st.markdown("---")
    
    # Knowledge Base Stats - Creative Visualization
    st.header("📚 Knowledge Base")
    
    if st.button("🔍 Explore Knowledge Base", use_container_width=True):
        st.session_state.show_kb_stats = not st.session_state.show_kb_stats
    
    if st.session_state.show_kb_stats:
        with open('it_knowledge_base.json', 'r') as f:
            kb = json.load(f)
        
        # Total articles with emoji
        st.metric("📖 Total Articles", len(kb))
        
        # Category breakdown with progress bars
        st.subheader("📊 Categories")
        categories = {}
        for article in kb:
            cat = article['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        # Sort by count
        sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        
        for cat, count in sorted_cats:
            # Create visual progress bar
            percentage = (count / len(kb)) * 100
            st.write(f"**{cat}**")
            st.progress(percentage / 100)
            st.caption(f"{count} article(s) • {percentage:.1f}%")
        
        # Tag cloud (most common tags)
        st.subheader("🏷️ Popular Tags")
        all_tags = {}
        for article in kb:
            for tag in article['tags']:
                all_tags[tag] = all_tags.get(tag, 0) + 1
        
        # Top 10 tags
        top_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Display as columns
        cols = st.columns(3)
        for idx, (tag, count) in enumerate(top_tags):
            with cols[idx % 3]:
                st.metric(f"#{tag}", count, delta=None)
        
        # Quick stats
        st.markdown("---")
        st.subheader("📈 Quick Stats")
        total_tags = sum(len(article['tags']) for article in kb)
        avg_tags = total_tags / len(kb)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🔖 Total Tags", total_tags)
        with col2:
            st.metric("📊 Avg Tags/Article", f"{avg_tags:.1f}")
        
        # Most comprehensive article
        max_content = max(kb, key=lambda x: len(x['content']))
        st.markdown("---")
        st.subheader("📝 Most Detailed Article")
        st.write(f"**{max_content['title']}**")
        st.caption(f"{len(max_content['content'])} characters • {max_content['category']}")

# Main chat interface
st.subheader("💬 Chat with IT Support")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-message"><strong>IT Support:</strong> {message["content"]}</div>', 
                   unsafe_allow_html=True)
        
        # Show sources if available
        if "sources" in message and message["sources"]:
            with st.expander("📚 Knowledge Base Sources"):
                for source in message["sources"]:
                    st.markdown(f"""
                    <div class="source-card">
                        <strong>{source['title']}</strong> (ID: {source['id']})<br>
                        <em>Category: {source['category']}</em>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your IT question here...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get chatbot response
    with st.spinner("🔍 Searching knowledge base..."):
        response, sources, func_result = st.session_state.chatbot.process_message(user_input)
    
    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "sources": sources,
        "function_result": func_result
    })
    
    # Rerun to display new messages
    st.rerun()

# Welcome message if no chat history
if not st.session_state.messages:
    st.info("👋 Welcome! I'm your IT Support Assistant. How can I help you today?")
    
    st.markdown("### 💡 Common Questions:")
    
    # Define common questions
    common_questions = [
        {"text": "🔐 How do I reset my password?", "query": "How do I reset my password?"},
        {"text": "📧 Outlook not syncing", "query": "My Outlook is not syncing emails"},
        {"text": "🔌 VPN connection issues", "query": "I can't connect to VPN"},
        {"text": "🖨️ Printer not working", "query": "My printer is not responding"}
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, question in enumerate(common_questions):
        with col1 if idx % 2 == 0 else col2:
            if st.button(question["text"], key=f"common_q_{idx}", use_container_width=True):
                # Add user message to history
                st.session_state.messages.append({"role": "user", "content": question["query"]})
                
                # Get chatbot response
                with st.spinner("🔍 Searching knowledge base..."):
                    response, sources, func_result = st.session_state.chatbot.process_message(question["query"])
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "sources": sources,
                    "function_result": func_result
                })
                
                # Rerun to display the conversation
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>
        🤖 IT Support Chatbot powered by RAG + LangChain + OpenAI<br>
        Need urgent help? Call IT Help Desk: ext. 4357
    </small>
</div>
""", unsafe_allow_html=True)