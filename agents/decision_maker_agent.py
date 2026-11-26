"""
Decision Maker & Business Leads Agent for Lead Research Agent.
Focuses on identifying key contacts, executives, and decision makers.
"""

from typing import Dict, Any, List
from utils.tavily_search import get_tavily_searcher
from utils.logging_util import ResearchLogger
from database.db import db


class DecisionMakerAgent:
    """Research agent for decision makers and business leads."""
    
    def __init__(self):
        """Initialize the agent."""
        self.searcher = None
    
    def research(self, request_id: int, company_name: str) -> Dict[str, Any]:
        """
        Research decision makers and key contacts.
        
        Args:
            request_id: Database request ID
            company_name: Name of the company to research
        
        Returns:
            Dictionary with decision maker findings
        """
        logger = ResearchLogger(request_id)
        
        try:
            logger.log_agent_start("DecisionMakerAgent", {
                "company_name": company_name
            })
            
            # Initialize searcher with request_id for logging
            self.searcher = get_tavily_searcher(request_id=request_id)
            # Search for decision makers
            logger.logger.info(f"Starting Tavily search for decision makers at '{company_name}'")
            decision_makers = self.searcher.search_decision_makers(company_name)
            
            # Log search results
            logger.logger.info(f"Found {len(decision_makers)} decision makers:")
            for idx, maker in enumerate(decision_makers[:10]):
                logger.logger.debug(f"  {idx+1}. {maker.get('name')} - {maker.get('title')} ({maker.get('source_url', 'N/A')})")
            
            # Save each decision maker to database
            for maker in decision_makers:
                db.save_decision_maker(request_id, maker)
            logger.logger.info(f"✅ {len(decision_makers)} decision makers saved to database")
            
            logger.log_agent_complete("DecisionMakerAgent", {
                "status": "success",
                "count": len(decision_makers)
            })
            
            return {
                "status": "success",
                "data": decision_makers,
                "count": len(decision_makers)
            }
        
        except Exception as e:
            logger.log_error("DecisionMakerAgent", str(e))
            return {
                "status": "error",
                "error": str(e)
            }
