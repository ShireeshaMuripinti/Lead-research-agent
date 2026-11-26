"""
Chat with Report Page for Lead Research Agent.
Interactive Q&A about generated research reports.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import settings
from database.db import db
from utils.gemini_integration import get_gemini_analyzer
from streamlit_app.components.report_display import render_error_message, render_info_message

# Page config
st.set_page_config(
    page_title="Chat with Report - Lead Research Agent",
    page_icon="💬",
    layout="wide"
)

st.title("💬 Chat with Research Report")
st.markdown("### Ask questions about company research findings")

# Initialize session state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "selected_report_id" not in st.session_state:
    st.session_state.selected_report_id = None

# Sidebar for report selection
st.sidebar.markdown("### 📑 Select Report")

try:
    # Get all available reports
    all_requests = db.get_all_requests(limit=50)
    report_options = []
    
    for request in all_requests:
        report = db.get_report_by_request(request.get("id"))
        if report:
            report_options.append({
                "label": f"{request.get('company_name')} - {request.get('created_at')[:10]}",
                "id": report.get("id"),
                "company": request.get("company_name")
            })
    
    if report_options:
        selected_option = st.sidebar.selectbox(
            "Choose a report:",
            options=[opt["label"] for opt in report_options],
            key="report_selector"
        )
        
        st.session_state.selected_report_id = next(
            opt["id"] for opt in report_options if opt["label"] == selected_option
        )
        
        # Get selected report
        selected_report = db.get_research_report(st.session_state.selected_report_id)
        
        if selected_report:
            st.sidebar.success(f"✅ Loaded: {selected_report.get('title')}")
            
            # Display report summary in sidebar
            with st.sidebar.expander("📋 Report Summary"):
                st.write(selected_report.get("executive_summary", "No summary available")[:200] + "...")
        
        # Main chat area
        st.divider()
        
        # Display chat history
        if st.session_state.chat_messages:
            st.markdown("### Conversation")
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    # Render HTML if message contains HTML tags
                    if "<" in message["content"] and ">" in message["content"]:
                        st.markdown(message["content"], unsafe_allow_html=True)
                    else:
                        st.markdown(message["content"])
        
        else:
            st.info("👋 Ask me anything about this research report!")
        
        # Chat input
        st.divider()
        
        user_query = st.chat_input(
            "Ask a question about the research report...",
            key="chat_input"
        )
        
        if user_query:
            # Add user message to chat
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_query
            })
            
            with st.chat_message("user"):
                st.markdown(user_query)
            
            # Generate response using Gemini
            try:
                with st.spinner("🤔 Analyzing report..."):
                    
                    # Get Gemini API key from settings (configured in .env)
                    gemini_api_key = settings.GEMINI_API_KEY
                    
                    if not gemini_api_key:
                        st.warning("⚠️ Gemini API key not configured. Please add GEMINI_API_KEY to your .env file.")
                        st.stop()
                    
                    # Initialize analyzer with logger
                    analyzer = get_gemini_analyzer(api_key=gemini_api_key)
                    
                    # Generate response
                    response = analyzer.answer_query_about_report(
                        user_query,
                        selected_report.get("report_content", "")
                    )
                    
                    # Save to database
                    db.save_chat_message(
                        st.session_state.selected_report_id,
                        user_query,
                        response
                    )
                    
                    # Add assistant message to chat
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                    with st.chat_message("assistant"):
                        # Render HTML if response contains HTML tags
                        if "<" in response and ">" in response:
                            st.markdown(response, unsafe_allow_html=True)
                        else:
                            st.markdown(response)
            
            except Exception as e:
                render_error_message(f"Error generating response: {str(e)}")
        
        # Display previous chat history
        if st.sidebar.button("📜 View Chat History"):
            with st.sidebar.expander("Chat History"):
                chat_history = db.get_chat_history(st.session_state.selected_report_id, limit=100)
                
                if chat_history:
                    for chat in reversed(chat_history):
                        st.markdown(f"**Q:** {chat['user_query']}")
                        st.markdown(f"**A:** {chat['assistant_response']}")
                        st.divider()
                else:
                    st.info("No previous chat history for this report.")
    
    else:
        render_info_message("No reports available. Generate a research report first from the 'Research Report' tab.")

except Exception as e:
    render_error_message(f"Error loading reports: {str(e)}")
