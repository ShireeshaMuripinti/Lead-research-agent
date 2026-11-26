"""
Streamlit Components for Lead Research Agent.
Reusable UI components for the application with consistent HTML rendering.
"""

import streamlit as st
from typing import Dict, List, Any
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.html_formatter import HTMLFormatter


def render_sidebar():
    """Render application sidebar with navigation."""
    with st.sidebar:
        st.title("🔍 Lead Research Agent")
        
        page = st.radio(
            "Navigation",
            ["Start New Research", "View Reports", "Chat with Report"],
            key="nav_radio"
        )
        
        st.divider()
        
        # Display settings info
        with st.expander("⚙️ Configuration"):
            st.caption("Environment Configuration")
            st.info("✓ Database: SQLite" if st.secrets.get("database_path") else "⚠ Database not configured")
            st.info("✓ Tavily API: Connected" if st.secrets.get("tavily_api_key") else "⚠ Tavily API not configured")
            st.info("✓ Gemini API: Connected" if st.secrets.get("gemini_api_key") else "⚠ Gemini API not configured")
        
        st.divider()
        
        # About section
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Lead Research Agent** is an AI-powered research platform that:
            - Gathers company information from multiple sources
            - Analyzes financial metrics and market position
            - Identifies key decision makers and contacts
            - Generates comprehensive research reports
            - Provides interactive Q&A about research findings
            """)
        
        return page


def render_html_content(html_content: str, use_container: bool = False):
    """Render HTML content in Streamlit with proper styling."""
    if not html_content:
        return
    
    # Add CSS styles inline for proper rendering
    styled_html = f"""
    <style>
        .report-section {{
            background-color: #f8f9fa;
            border-left: 4px solid #1f77b4;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .section-title {{
            font-size: 22px;
            font-weight: 600;
            color: #1f77b4;
            margin: 0 0 16px 0;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 8px;
        }}
        .subsection-title {{
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin: 16px 0 8px 0;
        }}
        .metric-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 16px;
            margin: 10px 0;
        }}
        .metric-label {{
            font-size: 13px;
            color: #666;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}
        .metric-value {{
            font-size: 18px;
            color: #1f77b4;
            font-weight: 600;
        }}
        .paragraph {{
            margin: 12px 0;
            line-height: 1.7;
            color: #333;
            font-size: 15px;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 14px;
        }}
        .data-table th {{
            background-color: #1f77b4;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #0d47a1;
        }}
        .data-table td {{
            padding: 10px 12px;
            border: 1px solid #e0e0e0;
            color: #333;
        }}
        .data-table tr:nth-child(even) {{
            background-color: #f5f5f5;
        }}
        .link-style {{
            color: #1f77b4;
            text-decoration: none;
            font-weight: 500;
        }}
        .link-style:hover {{
            text-decoration: underline;
        }}
        .summary-content {{
            color: #333;
            line-height: 1.7;
        }}
        .recommendations-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 13px;
        }}
        .recommendations-table th {{
            background-color: #1f77b4;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #0d47a1;
        }}
        .recommendations-table td {{
            padding: 10px;
            border: 1px solid #e0e0e0;
            color: #333;
        }}
        .recommendations-table tr:nth-child(even) {{
            background-color: #f5f5f5;
        }}
    </style>
    {html_content}
    """
    
    # Use st.html() for proper HTML rendering in Streamlit
    st.html(styled_html)


def render_report_display(report: Dict[str, Any]):
    """Render a research report with LLM HTML output directly - no Streamlit headers."""
    
    # Get company name from report
    company_name = report.get("company_name", "Research Report")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 Summary", "ℹ️ General Info", "💰 Financial", "📊 Industry", "👥 Decision Makers"]
    )
    
    with tab1:
        # Executive Summary
        summary = report.get("executive_summary", "")
        if summary:
            render_html_content(summary)
        else:
            st.info("No summary available")
        
        # Recommendations
        recommendations = report.get("recommendations", "")
        if recommendations:
            render_html_content(recommendations)
        else:
            st.info("No recommendations available")
    
    with tab2:
        general_info = report.get("general_info_json", {})
        if general_info:
            html_content = HTMLFormatter.format_general_info(general_info)
            render_html_content(html_content)
        else:
            st.info("No general information available")
    
    with tab3:
        financial = report.get("financial_json", {})
        if financial:
            html_content = HTMLFormatter.format_financial_info(financial)
            render_html_content(html_content)
        else:
            st.info("No financial information available")
    
    with tab4:
        industry = report.get("industrial_media_json", {})
        if industry:
            html_content = HTMLFormatter.format_industry_info(industry)
            render_html_content(html_content)
        else:
            st.info("No industry information available")
    
    with tab5:
        decision_makers = report.get("decision_makers_json", [])
        if decision_makers:
            html_content = HTMLFormatter.format_decision_makers(decision_makers)
            render_html_content(html_content)
        else:
            st.info("No decision makers found")


def render_loading_spinner(text: str = "Processing research..."):
    """Render loading spinner with text."""
    with st.spinner(text):
        return True


def render_error_message(error: str):
    """Render error message."""
    st.error(f"❌ Error: {error}")


def render_success_message(message: str):
    """Render success message."""
    st.success(f"✅ {message}")


def render_info_message(message: str):
    """Render info message."""
    st.info(f"ℹ️ {message}")
