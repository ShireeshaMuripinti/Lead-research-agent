"""
HTML Formatting Utilities for consistent report rendering.
Provides standardized HTML structure and styling for Streamlit display.
"""

from typing import Dict, List, Any, Optional
import json


class HTMLFormatter:
    """Utility for generating consistent, well-formatted HTML."""
    
    # CSS styles for consistent formatting
    STYLES = """
    <style>
        .report-section {
            background-color: #f8f9fa;
            border-left: 4px solid #1f77b4;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }
        
        .section-title {
            font-size: 22px;
            font-weight: 600;
            color: #1f77b4;
            margin: 0 0 16px 0;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 8px;
        }
        
        .subsection-title {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin: 16px 0 8px 0;
        }
        
        .metric-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 16px;
            margin: 10px 0;
        }
        
        .metric-label {
            font-size: 13px;
            color: #666;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        
        .metric-value {
            font-size: 18px;
            color: #1f77b4;
            font-weight: 600;
        }
        
        .info-box {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 12px 16px;
            margin: 10px 0;
            border-radius: 4px;
            color: #0d47a1;
        }
        
        .warning-box {
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 12px 16px;
            margin: 10px 0;
            border-radius: 4px;
            color: #e65100;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 14px;
        }
        
        .data-table th {
            background-color: #1f77b4;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #0d47a1;
        }
        
        .data-table td {
            padding: 10px 12px;
            border: 1px solid #e0e0e0;
            color: #333;
        }
        
        .data-table tr:nth-child(even) {
            background-color: #f5f5f5;
        }
        
        .data-table tr:hover {
            background-color: #f0f0f0;
        }
        
        .list-item {
            margin: 8px 0;
            line-height: 1.6;
            color: #333;
        }
        
        .paragraph {
            margin: 12px 0;
            line-height: 1.7;
            color: #333;
            font-size: 15px;
        }
        
        .tag {
            display: inline-block;
            background: #e3f2fd;
            color: #1565c0;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: 500;
            margin: 4px 4px 4px 0;
        }
        
        .link-style {
            color: #1f77b4;
            text-decoration: none;
            font-weight: 500;
        }
        
        .link-style:hover {
            text-decoration: underline;
        }
    </style>
    """
    
    @staticmethod
    def section_title(title: str) -> str:
        """Format a section title."""
        return f'<div class="section-title">{title}</div>'
    
    @staticmethod
    def subsection_title(title: str) -> str:
        """Format a subsection title."""
        return f'<div class="subsection-title">{title}</div>'
    
    @staticmethod
    def paragraph(text: str) -> str:
        """Format a paragraph."""
        if not text:
            return ""
        return f'<div class="paragraph">{text}</div>'
    
    @staticmethod
    def metric_card(label: str, value: str) -> str:
        """Format a metric card."""
        if not value:
            value = "N/A"
        return f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """
    
    @staticmethod
    def info_box(text: str) -> str:
        """Format an info box."""
        return f'<div class="info-box">{text}</div>'
    
    @staticmethod
    def warning_box(text: str) -> str:
        """Format a warning box."""
        return f'<div class="warning-box">{text}</div>'
    
    @staticmethod
    def list_item(item: str, level: int = 0) -> str:
        """Format a list item."""
        indent = "&nbsp;" * (level * 4)
        return f'<div class="list-item">{indent}• {item}</div>'
    
    @staticmethod
    def bullet_list(items: List[str]) -> str:
        """Format a bullet list."""
        html = ""
        for item in items:
            if isinstance(item, dict):
                html += HTMLFormatter.list_item(item.get("text", str(item)))
            else:
                html += HTMLFormatter.list_item(str(item))
        return html
    
    @staticmethod
    def table(headers: List[str], rows: List[List[str]]) -> str:
        """Format a data table."""
        html = '<table class="data-table"><thead><tr>'
        
        # Headers
        for header in headers:
            html += f'<th>{header}</th>'
        html += '</tr></thead><tbody>'
        
        # Rows
        for row in rows:
            html += '<tr>'
            for cell in row:
                html += f'<td>{cell}</td>'
            html += '</tr>'
        
        html += '</tbody></table>'
        return html
    
    @staticmethod
    def tag(label: str) -> str:
        """Format a tag/badge."""
        return f'<span class="tag">{label}</span>'
    
    @staticmethod
    def link(text: str, url: str) -> str:
        """Format a hyperlink."""
        return f'<a href="{url}" class="link-style" target="_blank">{text}</a>'
    
    @staticmethod
    def section_container(content: str, title: str = None) -> str:
        """Wrap content in a section container."""
        section_html = '<div class="report-section">'
        
        if title:
            section_html += HTMLFormatter.section_title(title)
        
        section_html += content + '</div>'
        return section_html
    
    @staticmethod
    def safe_text(text: str) -> str:
        """Safely escape HTML special characters."""
        if not text:
            return ""
        text = str(text)
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&#39;")
        return text
    
    @staticmethod
    def format_general_info(info: Dict[str, Any]) -> str:
        """Format general company information."""
        if not info:
            return HTMLFormatter.info_box("No general information available")
        
        html = HTMLFormatter.section_title("Company Overview")
        
        # Description
        if info.get("company_description"):
            html += HTMLFormatter.paragraph(info.get("company_description"))
        
        # Metrics
        html += '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;">'
        html += HTMLFormatter.metric_card("Founded", info.get("founded_year", "N/A"))
        html += HTMLFormatter.metric_card("Company Size", info.get("company_size", "N/A"))
        html += HTMLFormatter.metric_card("Headquarters", info.get("headquarters", "N/A"))
        html += HTMLFormatter.metric_card("Website", 
                                         HTMLFormatter.link(info.get("website_url", "N/A"), info.get("website_url")) 
                                         if info.get("website_url") else "N/A")
        html += '</div>'
        
        # LinkedIn
        if info.get("linkedin_profile"):
            html += HTMLFormatter.info_box(f'<strong>LinkedIn:</strong> {HTMLFormatter.link("View Profile", info.get("linkedin_profile"))}')
        
        return html
    
    @staticmethod
    def format_financial_info(info: Dict[str, Any]) -> str:
        """Format financial information."""
        if not info:
            return HTMLFormatter.info_box("No financial information available")
        
        html = HTMLFormatter.section_title("Financial Information")
        
        # Metrics
        html += '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">'
        html += HTMLFormatter.metric_card("Revenue", info.get("revenue", "N/A"))
        html += HTMLFormatter.metric_card("Total Funding", info.get("total_funding", "N/A"))
        html += HTMLFormatter.metric_card("Profitability", info.get("profitability", "N/A"))
        html += '</div>'
        
        # Financial health
        if info.get("financial_health"):
            html += HTMLFormatter.subsection_title("Financial Health")
            html += HTMLFormatter.paragraph(info.get("financial_health"))
        
        # Funding rounds
        if info.get("funding_rounds"):
            html += HTMLFormatter.subsection_title("Funding Rounds")
            funding = info.get("funding_rounds")
            if isinstance(funding, str):
                html += HTMLFormatter.paragraph(funding)
            else:
                html += HTMLFormatter.bullet_list([str(f) for f in funding])
        
        # Key metrics
        if info.get("key_metrics"):
            html += HTMLFormatter.subsection_title("Key Metrics")
            metrics = info.get("key_metrics")
            if isinstance(metrics, str):
                html += HTMLFormatter.paragraph(metrics)
            else:
                html += HTMLFormatter.bullet_list([str(m) for m in metrics])
        
        return html
    
    @staticmethod
    def format_industry_info(info: Dict[str, Any]) -> str:
        """Format industry and market information with SWOT analysis."""
        if not info:
            return HTMLFormatter.info_box("No industry information available")
        
        html = HTMLFormatter.section_title("Industry & Market Analysis")
        
        # Industry vertical
        if info.get("industry_vertical"):
            html += HTMLFormatter.subsection_title("Industry Vertical")
            html += HTMLFormatter.paragraph(info.get("industry_vertical"))
        
        # Market position
        if info.get("market_position"):
            html += HTMLFormatter.subsection_title("Market Position")
            html += HTMLFormatter.paragraph(info.get("market_position"))
        
        # Competitors
        if info.get("competitors"):
            html += HTMLFormatter.subsection_title("Main Competitors")
            competitors = info.get("competitors")
            if isinstance(competitors, str):
                html += HTMLFormatter.paragraph(competitors)
            else:
                html += HTMLFormatter.bullet_list([str(c) for c in competitors[:10]])  # Limit to 10
        
        # Market trends
        if info.get("market_trends"):
            html += HTMLFormatter.subsection_title("Market Trends")
            trends = info.get("market_trends")
            if isinstance(trends, str):
                html += HTMLFormatter.paragraph(trends)
            else:
                html += HTMLFormatter.bullet_list([str(t) for t in trends])
        
        # SWOT Analysis
        if any([info.get("swot_strengths"), info.get("swot_weaknesses"), 
                info.get("swot_opportunities"), info.get("swot_threats")]):
            html += HTMLFormatter.subsection_title("SWOT Analysis")
            html += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0;">'
            
            # Strengths (Green)
            strengths = info.get("swot_strengths", [])
            if isinstance(strengths, str):
                strengths = [s.strip() for s in strengths.split(",")]
            html += '<div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 16px; border-radius: 8px;">'
            html += '<h4 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">💪 Strengths</h4>'
            html += '<ul style="margin: 0; padding-left: 20px; line-height: 1.6;">'
            for s in strengths[:5]:
                html += f"<li>{str(s).strip()}</li>"
            html += "</ul></div>"
            
            # Weaknesses (Red)
            weaknesses = info.get("swot_weaknesses", [])
            if isinstance(weaknesses, str):
                weaknesses = [w.strip() for w in weaknesses.split(",")]
            html += '<div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 16px; border-radius: 8px;">'
            html += '<h4 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">⚠️ Weaknesses</h4>'
            html += '<ul style="margin: 0; padding-left: 20px; line-height: 1.6;">'
            for w in weaknesses[:5]:
                html += f"<li>{str(w).strip()}</li>"
            html += "</ul></div>"
            
            # Opportunities (Blue)
            opportunities = info.get("swot_opportunities", [])
            if isinstance(opportunities, str):
                opportunities = [o.strip() for o in opportunities.split(",")]
            html += '<div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 16px; border-radius: 8px;">'
            html += '<h4 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">🚀 Opportunities</h4>'
            html += '<ul style="margin: 0; padding-left: 20px; line-height: 1.6;">'
            for o in opportunities[:5]:
                html += f"<li>{str(o).strip()}</li>"
            html += "</ul></div>"
            
            # Threats (Orange)
            threats = info.get("swot_threats", [])
            if isinstance(threats, str):
                threats = [t.strip() for t in threats.split(",")]
            html += '<div style="background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: white; padding: 16px; border-radius: 8px;">'
            html += '<h4 style="margin: 0 0 12px 0; font-size: 16px; font-weight: 600;">🎯 Threats</h4>'
            html += '<ul style="margin: 0; padding-left: 20px; line-height: 1.6;">'
            for t in threats[:5]:
                html += f"<li>{str(t).strip()}</li>"
            html += "</ul></div>"
            html += "</div>"
        
        # Media coverage
        if info.get("media_coverage"):
            html += HTMLFormatter.subsection_title("Recent Media Coverage")
            coverage = info.get("media_coverage")
            if isinstance(coverage, str):
                html += HTMLFormatter.paragraph(coverage)
            else:
                html += HTMLFormatter.bullet_list([str(c) for c in coverage[:5]])  # Limit to 5
        
        # Press releases
        if info.get("press_releases"):
            html += HTMLFormatter.subsection_title("Press Releases")
            releases = info.get("press_releases")
            if isinstance(releases, str):
                html += HTMLFormatter.paragraph(releases)
            else:
                html += HTMLFormatter.bullet_list([str(r) for r in releases[:5]])  # Limit to 5
        
        return html
    
    @staticmethod
    def format_decision_makers(makers: List[Dict[str, Any]]) -> str:
        """Format decision makers information with detailed contact info."""
        if not makers:
            return HTMLFormatter.info_box("No decision makers found")
        
        html = HTMLFormatter.section_title(f"Decision Makers & Key Contacts ({len(makers)})")
        
        # Create detailed table
        headers = ["Name", "Position", "Phone", "Email", "LinkedIn", "Other Profiles"]
        rows = []
        
        for maker in makers:
            # Get all fields, default to N/A if not present
            name = HTMLFormatter.safe_text(maker.get("name", "N/A"))
            title = HTMLFormatter.safe_text(maker.get("title", "N/A"))
            phone = HTMLFormatter.safe_text(maker.get("phone", "N/A")) if maker.get("phone") else "N/A"
            email = HTMLFormatter.safe_text(maker.get("email", "N/A")) if maker.get("email") else "N/A"
            
            # LinkedIn with link
            linkedin = "N/A"
            if maker.get("linkedin_profile"):
                linkedin = f'<a href="{maker.get("linkedin_profile")}" target="_blank">LinkedIn</a>'
            
            # Other profiles/business directions - keep concise
            other_profiles = HTMLFormatter.safe_text(maker.get("other_profiles", "")) or \
                           HTMLFormatter.safe_text(maker.get("business_direction", "")) or "N/A"
            if other_profiles and len(other_profiles) > 50:
                other_profiles = other_profiles[:47] + "..."
            
            row = [name, title, phone, email, linkedin, other_profiles]
            rows.append(row)
        
        html += HTMLFormatter.table(headers, rows)
        
        return html
    
    @staticmethod
    def get_full_html(sections: Dict[str, str], title: str = "Research Report") -> str:
        """Generate complete HTML document."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{HTMLFormatter.safe_text(title)}</title>
            {HTMLFormatter.STYLES}
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; color: #333; line-height: 1.6; padding: 20px;">
            <h1 style="color: #1f77b4; margin-bottom: 30px;">{HTMLFormatter.safe_text(title)}</h1>
        """
        
        for section_name, section_content in sections.items():
            if section_content:
                html += section_content + "\n"
        
        html += """
        </body>
        </html>
        """
        return html
