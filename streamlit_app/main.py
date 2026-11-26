"""
Main Streamlit Application for Lead Research Agent.
Entry point for the web interface.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings
from database.db import db
from streamlit_app.components.report_display import render_sidebar, render_error_message, render_success_message, render_info_message

# Page configuration
st.set_page_config(
    page_title="Lead Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point."""
    
    # Initialize database
    try:
        db._ensure_db_exists()
    except Exception as e:
        render_error_message(f"Database initialization failed: {str(e)}")
        return
    
    # Render sidebar and get current page
    page = render_sidebar()
    
    if page == "Start New Research":
        st.switch_page("pages/research_report.py")
    
    elif page == "View Reports":
        st.switch_page("pages/research_report.py")
    
    elif page == "Chat with Report":
        st.switch_page("pages/chat_with_report.py")


if __name__ == "__main__":
    main()
