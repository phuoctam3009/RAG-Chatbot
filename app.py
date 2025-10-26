"""
Streamlit UI for IT Support Chatbot
"""

import streamlit as st
from chatbot import ITSupportChatbot
from function_calling import (
    create_support_ticket, check_ticket_status, 
    check_system_status, search_employee_directory
)
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

if 'ticket_counter' not in st.session_state:
    st.session_state.ticket_counter = 1000

# Header
st.markdown('<div class="main-header">🤖 IT Support Chatbot</div>', unsafe_allow_html=True)
st.markdown("---")

# Check initialization
if not st.session_state.get('initialized', False):
    st.error(f"⚠️ Failed to initialize chatbot: {st.session_state.get('error', 'Unknown error')}")
    st.info("💡 Please ensure you have:")
    st.markdown("""
    1. Created a `.env` file with your Azure OpenAI credentials
    2. Run `python build_vector_store.py` to create the vector store
    3. Installed all requirements: `pip install -r requirements.txt`
    """)
    st.stop()

# Sidebar
with st.sidebar:
    st.header("🛠️ IT Support Tools")
    
    # System Status Checker
    with st.expander("📊 Check System Status"):
        system = st.selectbox(
            "Select System",
            ["email", "vpn", "file_server", "internet", "office365", "printer"]
        )
        if st.button("Check Status"):
            status = check_system_status(system)
            if status.get("status") == "operational":
                st.success(f"✅ {system.upper()} is operational")
                st.info(f"Uptime: {status.get('uptime', 'N/A')}")
            elif status.get("status") == "degraded":
                st.warning(f"⚠️ {system.upper()} is experiencing issues")
                st.info(status.get("note", ""))
            else:
                st.error(f"❌ {system.upper()} status unknown")
    
    # Ticket Status Checker
    with st.expander("🎫 Check Ticket Status"):
        ticket_id = st.text_input("Ticket ID (e.g., INC1000)")
        if st.button("Check Ticket"):
            if ticket_id:
                status = check_ticket_status(ticket_id)
                if status.get("found"):
                    st.success(f"Ticket found: {status['ticket_id']}")
                    st.write(f"**Status:** {status['status']}")
                    st.write(f"**Priority:** {status['priority']}")
                    st.write(f"**Title:** {status['title']}")
                    st.write(f"**Created:** {status['created_at']}")
                else:
                    st.error(status.get("message", "Ticket not found"))
    
    # Employee Directory
    with st.expander("👥 Search Employee Directory"):
        emp_name = st.text_input("Employee Name")
        emp_dept = st.text_input("Department")
        if st.button("Search"):
            results = search_employee_directory(name=emp_name, department=emp_dept)
            if results:
                for emp in results:
                    st.write(f"**{emp['name']}**")
                    st.write(f"Email: {emp['email']}")
                    st.write(f"Department: {emp['department']}")
                    st.write(f"Phone: {emp['phone']}")
                    st.write("---")
            else:
                st.info("No employees found")
    
    # Create Ticket
    with st.expander("📝 Create Support Ticket"):
        ticket_title = st.text_input("Issue Title")
        ticket_desc = st.text_area("Description")
        ticket_category = st.selectbox(
            "Category",
            ["password", "hardware", "software", "network", "access", "other"]
        )
        ticket_priority = st.selectbox(
            "Priority",
            ["low", "medium", "high", "critical"]
        )
        if st.button("Create Ticket"):
            if ticket_title and ticket_desc:
                ticket = create_support_ticket(
                    title=ticket_title,
                    description=ticket_desc,
                    category=ticket_category,
                    priority=ticket_priority
                )
                st.success(f"✅ Ticket created: {ticket['ticket_id']}")
                st.json(ticket)
            else:
                st.error("Please fill in title and description")
    
    st.markdown("---")
    
    # Quick Actions
    st.header("⚡ Quick Actions")
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chatbot.reset_conversation()
        st.rerun()
    
    if st.button("📚 Show Knowledge Base Stats"):
        articles = st.session_state.chatbot.get_relevant_articles("", k=15)
        st.info(f"Knowledge Base contains {len(articles)} articles")

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
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔐 How do I reset my password?"):
            st.session_state.messages.append({"role": "user", "content": "How do I reset my password?"})
            st.rerun()
        
        if st.button("📧 Outlook not syncing"):
            st.session_state.messages.append({"role": "user", "content": "My Outlook is not syncing emails"})
            st.rerun()
    
    with col2:
        if st.button("🔌 VPN connection issues"):
            st.session_state.messages.append({"role": "user", "content": "I can't connect to VPN"})
            st.rerun()
        
        if st.button("🖨️ Printer not working"):
            st.session_state.messages.append({"role": "user", "content": "My printer is not responding"})
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>
        🤖 IT Support Chatbot powered by RAG + LangChain + Azure OpenAI<br>
        Need urgent help? Call IT Help Desk: ext. 4357
    </small>
</div>
""", unsafe_allow_html=True)
