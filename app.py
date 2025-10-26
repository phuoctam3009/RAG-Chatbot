"""
Streamlit UI for IT Support Chatbot
"""

import streamlit as st
import json
from chatbot import ITSupportChatbot

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
    1. Created a `.env` file with your API credentials
    2. Run `python build_vector_store.py` to create the vector store
    3. Installed all requirements: `pip install -r requirements.txt`
    """)
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚡ Quick Actions")
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chatbot.reset_conversation()
        st.rerun()
    
    st.markdown("---")
    st.header("📚 Knowledge Base")
    
    if st.button("🔍 Explore Knowledge Base"):
        st.session_state.show_kb_stats = not st.session_state.show_kb_stats
    
    if st.session_state.show_kb_stats:
        try:
            with open('it_knowledge_base.json', 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
            
            st.metric("📖 Total Articles", len(kb_data))
            
            st.subheader("📊 Categories")
            categories = {}
            for article in kb_data:
                cat = article['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(kb_data)) * 100
                st.write(f"**{cat}**")
                st.progress(percentage / 100)
                st.caption(f"{count} articles ({percentage:.1f}%)")
            
            st.subheader("🏷️ Popular Tags")
            all_tags = {}
            for article in kb_data:
                for tag in article.get('tags', []):
                    all_tags[tag] = all_tags.get(tag, 0) + 1
            
            top_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:10]
            cols = st.columns(3)
            for i, (tag, count) in enumerate(top_tags):
                with cols[i % 3]:
                    st.metric(f"#{tag}", count)
            
            st.subheader("📈 Quick Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Tags", sum(all_tags.values()))
            with col2:
                avg_tags = sum(len(article.get('tags', [])) for article in kb_data) / len(kb_data)
                st.metric("Avg Tags/Article", f"{avg_tags:.1f}")
            
            st.subheader("📝 Most Detailed")
            longest = max(kb_data, key=lambda x: len(x['content']))
            st.info(f"**{longest['title']}**\n\n{len(longest['content'])} characters • {longest['category']}")
            
        except Exception as e:
            st.error(f"Error loading KB stats: {e}")

# Main chat interface
st.subheader("💬 Chat with IT Support")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-message assistant-message"><strong>IT Support:</strong> {message["content"]}</div>',
            unsafe_allow_html=True
        )
        
        if "sources" in message and message["sources"]:
            with st.expander("📚 Knowledge Base Sources"):
                for source in message["sources"]:
                    st.markdown(
                        f'<div class="source-card"><strong>{source["title"]}</strong> (ID: {source["id"]})<br>'
                        f'<em>Category: {source["category"]}</em></div>',
                        unsafe_allow_html=True
                    )

# Chat input
user_input = st.chat_input("Type your IT question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("🔍 Searching knowledge base..."):
        response, sources, _ = st.session_state.chatbot.process_message(user_input)
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "sources": sources
    })
    
    st.rerun()

# Welcome message
if not st.session_state.messages:
    st.info("👋 Welcome! I'm your IT Support Assistant. How can I help you today?")
    
    st.markdown("### 💡 Common Questions:")
    
    common_questions = [
        {"text": "🔐 How do I reset my password?", "query": "How do I reset my password?"},
        {"text": "📧 Outlook not syncing", "query": "My Outlook is not syncing emails"},
        {"text": "🔌 VPN connection issues", "query": "I can't connect to VPN"},
        {"text": "🖨️ Printer not working", "query": "My printer is not responding"}
    ]
    
    col1, col2 = st.columns(2)
    for i, q in enumerate(common_questions):
        with col1 if i % 2 == 0 else col2:
            if st.button(q["text"], key=f"q_{i}"):
                st.session_state.messages.append({"role": "user", "content": q["query"]})
                with st.spinner("🔍 Searching knowledge base..."):
                    response, sources, _ = st.session_state.chatbot.process_message(q["query"])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "sources": sources
                })
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>🤖 IT Support Chatbot powered by RAG + LangChain</small>
</div>
""", unsafe_allow_html=True)