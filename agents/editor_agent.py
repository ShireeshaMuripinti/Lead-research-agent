"""
Editor Agent for Lead Research Agent.
Generates final comprehensive reports from curated research data.
"""

from typing import Dict, Any
from utils.gemini_integration import get_gemini_analyzer
from database.db import db


class EditorAgent:
    """Final report generation and editing agent."""
    
    def __init__(self):
        """Initialize the editor agent."""
        self.analyzer = None
    
    def generate_report(self, request_id: int, company_name: str,
                       general_info: Dict[str, Any],
                       financial_info: Dict[str, Any],
                       industry_media: Dict[str, Any],
                       decision_makers: list,
                       gemini_api_key: str = None) -> Dict[str, Any]:
        """
        Generate final comprehensive research report.
        
        Args:
            request_id: Database request ID
            company_name: Company name
            general_info: General information findings
            financial_info: Financial findings
            industry_media: Industry and media findings
            decision_makers: List of decision makers
            gemini_api_key: API key for Gemini
        
        Returns:
            Generated report ID and status
        """
        try:
            # Initialize analyzer if API key provided
            if gemini_api_key:
                self.analyzer = get_gemini_analyzer(api_key=gemini_api_key)
                
                # Generate executive summary
                executive_summary = self.analyzer.generate_executive_summary(
                    company_name, general_info, financial_info, industry_media
                )
                
                # Generate recommendations
                recommendations = self.analyzer.generate_recommendations(
                    company_name, general_info, financial_info, industry_media, decision_makers
                )
            else:
                executive_summary = "Executive summary generation requires Gemini API key."
                recommendations = "Recommendations generation requires Gemini API key."
            
            # Create report title
            title = f"Lead Research Report: {company_name}"
            
            # Save comprehensive report
            report_id = db.create_research_report(
                request_id=request_id,
                title=title,
                executive_summary=executive_summary,
                general_info=general_info or {},
                financial=financial_info or {},
                industrial_media=industry_media or {},
                decision_makers=decision_makers or [],
                recommendations=recommendations
            )
            
            # Update request status
            db.update_request_status(request_id, "completed")
            
            return {
                "status": "success",
                "report_id": report_id,
                "title": title
            }
        
        except Exception as e:
            db.update_request_status(request_id, "failed", str(e))
            return {
                "status": "error",
                "error": str(e)
            }
