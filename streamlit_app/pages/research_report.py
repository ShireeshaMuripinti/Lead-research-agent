"""
Research Report Page for Lead Research Agent.
Handles company research initiation and report display.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import settings
from database.db import db
from agents.curator_agent import CuratorAgent
from agents.editor_agent import EditorAgent
from utils.validators import validate_company_name, validate_website, validate_location, validate_industry
from streamlit_app.components.report_display import (
    render_report_display, render_loading_spinner, 
    render_error_message, render_success_message, render_info_message, render_sidebar
)

# Page config
st.set_page_config(
    page_title="Research Report - Lead Research Agent",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if "current_request_id" not in st.session_state:
    st.session_state.current_request_id = None

# Tabs for different sections
tab1, tab2 = st.tabs(["📝 New Research", "📊 View Reports"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        company_name = st.text_input(
            "Company Name *",
            placeholder="e.g., Apple Inc., Tesla, Microsoft",
            key="company_name_input"
        )
    
    with col2:
        st.write("")  # Spacing
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        website = st.text_input(
            "Website (Optional)",
            placeholder="https://example.com",
            key="website_input"
        )
    
    with col2:
        location = st.text_input(
            "Location (Optional)",
            placeholder="e.g., San Francisco, CA",
            key="location_input"
        )
    
    with col3:
        industry = st.text_input(
            "Industry (Optional)",
            placeholder="e.g., Technology, Finance",
            key="industry_input"
        )
    
    # API Keys section (collapsible)
    with st.expander("🔐 API Configuration (Optional for AI Analysis)"):
        st.info("Provide API keys for enhanced AI-powered analysis using Gemini. Leave empty to use basic search only.")
        
        gemini_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Your Gemini API key",
            key="gemini_key_input"
        )
        
        tavily_api_key = st.text_input(
            "Tavily API Key",
            type="password",
            placeholder="Your Tavily API key",
            key="tavily_key_input"
        )
    
    # Validation and submission
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        submit_button = st.button("🚀 Start Research", use_container_width=True)
    
    with col2:
        clear_button = st.button("🔄 Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.current_request_id = None
        st.rerun()
    
    # Process research request
    if submit_button:
        # Validate inputs
        is_valid, message = validate_company_name(company_name)
        if not is_valid:
            render_error_message(message)
            st.stop()
        
        if website:
            is_valid, message = validate_website(website)
            if not is_valid:
                render_error_message(message)
                st.stop()
        
        if location:
            is_valid, message = validate_location(location)
            if not is_valid:
                render_error_message(message)
                st.stop()
        
        if industry:
            is_valid, message = validate_industry(industry)
            if not is_valid:
                render_error_message(message)
                st.stop()
        
        # Create research request in database
        try:
            request_id = db.create_research_request(
                company_name=company_name,
                website=website,
                location=location,
                industry=industry
            )
            st.session_state.current_request_id = request_id
            
            render_success_message(f"Research request created (ID: {request_id})")
            
            # Run research agents
            with st.spinner("🔄 Initiating research process..."):
                
                # Initialize curator agent
                curator = CuratorAgent()
                
                # Get API keys - use provided or load from settings
                gemini_key = gemini_api_key or settings.GEMINI_API_KEY or None
                tavily_key = tavily_api_key if tavily_api_key else settings.TAVILY_API_KEY
                
                # Show what API keys will be used
                with st.expander("ℹ️ API Configuration Info", expanded=False):
                    if gemini_key:
                        st.success("✅ Gemini API key found - LLM analysis will be enabled")
                    else:
                        st.warning("⚠️ No Gemini API key - using basic parsing only (add to .env file or form)")
                    if tavily_key:
                        st.success("✅ Tavily API key configured")
                    else:
                        st.error("❌ Tavily API key missing!")
                
                # Orchestrate research
                curator_results = curator.orchestrate_research(
                    request_id=request_id,
                    company_name=company_name,
                    website=website,
                    location=location,
                    industry=industry,
                    gemini_api_key=gemini_key
                )
                
                if curator_results.get("errors"):
                    for error in curator_results.get("errors"):
                        render_error_message(error)
                
                # Generate final report
                editor = EditorAgent()
                report_result = editor.generate_report(
                    request_id=request_id,
                    company_name=company_name,
                    general_info=curator_results.get("general_info"),
                    financial_info=curator_results.get("financial_info"),
                    industry_media=curator_results.get("industry_media"),
                    decision_makers=curator_results.get("decision_makers", []),
                    gemini_api_key=gemini_key
                )
                
                if report_result.get("status") == "success":
                    render_success_message(f"Report generated successfully! (Report ID: {report_result.get('report_id')})")
                    
                    # Retrieve and display report
                    report = db.get_research_report(report_result.get("report_id"))
                    if report:
                        render_report_display(report)
                else:
                    render_error_message(report_result.get("error"))
        
        except Exception as e:
            render_error_message(f"Research failed: {str(e)}")

with tab2:
    try:
        all_requests = db.get_all_requests(limit=20)
        
        if all_requests:
            # Filter requests that have completed reports
            reports_with_status = []
            
            for request in all_requests:
                request_id = request.get("id")
                report = db.get_report_by_request(request_id)
                
                reports_with_status.append({
                    "id": request_id,
                    "company": request.get("company_name"),
                    "website": request.get("website"),
                    "location": request.get("location"),
                    "status": request.get("status"),
                    "created_at": request.get("created_at"),
                    "has_report": report is not None,
                    "report": report
                })
            
            # Display reports in a table
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
            
            with col1:
                st.write("**Company**")
            with col2:
                st.write("**Location**")
            with col3:
                st.write("**Status**")
            with col4:
                st.write("**Created**")
            with col5:
                st.write("**Action**")
            
            st.divider()
            
            for report_info in reports_with_status:
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])
                
                with col1:
                    st.write(report_info["company"])
                with col2:
                    st.write(report_info["location"] or "N/A")
                with col3:
                    status_emoji = "✅" if report_info["status"] == "completed" else "⏳" if report_info["status"] == "in_progress" else "❌"
                    st.write(f"{status_emoji} {report_info['status']}")
                with col4:
                    st.caption(report_info["created_at"][:10])
                with col5:
                    if report_info["has_report"] and st.button("View", key=f"view_{report_info['id']}"):
                        st.session_state.current_request_id = report_info["id"]
                        st.rerun()
            
            # Display selected report if any
            if st.session_state.current_request_id:
                st.divider()
                report = db.get_research_report(
                    [r["report"]["id"] for r in reports_with_status 
                     if r["id"] == st.session_state.current_request_id and r["report"]][0]
                )
                if report:
                    render_report_display(report)
        
        else:
            render_info_message("No research reports found. Start a new research to see reports here.")
    
    except Exception as e:
        render_error_message(f"Failed to load reports: {str(e)}")
