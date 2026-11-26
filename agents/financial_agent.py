"""
Financial Agent for Lead Research Agent.
Enhanced version with targeted research questions for better financial analysis.
"""

from typing import Dict, Any
from utils.tavily_search import get_tavily_searcher
from utils.gemini_integration import get_gemini_analyzer
from utils.logging_util import ResearchLogger
from database.db import db
import json


class FinancialAgent:
    """Research agent for financial information with targeted research questions."""
    
    # Strategic financial research questions
    RESEARCH_QUESTIONS = {
        "revenue_metrics": [
            "What is the company's annual revenue (most recent fiscal year)?",
            "What is the revenue growth rate (YoY)?",
            "What are the company's revenue streams by segment or geography?",
        ],
        "funding": [
            "What is the company's funding history and total capital raised?",
            "Who are the major investors and venture firms?",
            "What is the latest funding round and valuation?",
        ],
        "profitability": [
            "Is the company profitable? What is the profit margin?",
            "What are the company's operating costs and expenses?",
            "What is the company's EBITDA or net income?",
        ],
        "financial_health": [
            "What is the company's debt-to-equity ratio?",
            "What is the company's cash position and runway?",
            "What are key financial ratios and metrics?",
        ],
        "market_position": [
            "What is the company's market cap (if public)?",
            "How does the company compare financially to competitors?",
            "What is the market share in their industry?",
        ],
    }
    
    def __init__(self):
        """Initialize the agent."""
        self.searcher = None
        self.analyzer = None
    
    def research(self, request_id: int, company_name: str, 
                gemini_api_key: str = None) -> Dict[str, Any]:
        """
        Research financial information with targeted questions.
        
        Args:
            request_id: Database request ID
            company_name: Company name
            gemini_api_key: Gemini API key for enhanced analysis
        
        Returns:
            Dictionary with comprehensive financial information
        """
        logger = ResearchLogger(request_id)
        
        try:
            logger.log_agent_start("FinancialAgent", {
                "company_name": company_name,
                "research_questions": len(self.RESEARCH_QUESTIONS)
            })
            
            # Initialize searcher with request_id for logging
            self.searcher = get_tavily_searcher(request_id=request_id)
            # Search for financial information
            logger.logger.info(f"Starting Tavily search for financial information on '{company_name}'")
            search_results = self.searcher.search_company_financial_info(company_name)
            
            # Log search results
            if search_results.get("sources"):
                logger.logger.info(f"Found {len(search_results.get('sources', []))} financial sources:")
                for idx, source in enumerate(search_results.get("sources", [])[:5]):
                    logger.logger.debug(f"  Source {idx+1}: {source.get('title')} ({source.get('url')})")
                    logger.logger.debug(f"    Snippet: {source.get('snippet', '')[:200]}...")
            
            # Analyze with Gemini if available
            if gemini_api_key:
                logger.logger.info("Analyzing financial results with Gemini API")
                self.analyzer = get_gemini_analyzer(api_key=gemini_api_key, logger=logger)
                financial_info = self.analyzer.analyze_financial_info(search_results)
                logger.logger.info("✅ Gemini financial analysis completed")
            else:
                logger.logger.info("No Gemini API key - using basic financial parsing")
                financial_info = self._parse_basic_financial(search_results)
            
            # Ensure all fields are strings
            financial_info = self._ensure_string_fields(financial_info)
            
            # Save to database
            db.save_financial_info(request_id, financial_info)
            logger.log_database_save("financial_results", 1, {"company": company_name})
            
            logger.log_agent_complete("FinancialAgent", {
                "status": "success",
                "fields_extracted": list(financial_info.keys())
            })
            
            return {
                "status": "success",
                "data": financial_info,
                "raw_sources": search_results.get("sources", []),
                "research_questions_count": sum(len(q) for q in self.RESEARCH_QUESTIONS.values())
            }
        
        except Exception as e:
            logger.log_error("FinancialAgent", str(e))
            return {
                "status": "error",
                "error": str(e)
            }
    
    @staticmethod
    def _parse_basic_financial(search_results: Dict) -> Dict[str, Any]:
        """Extract basic financial information without AI."""
        sources = search_results.get("sources", [])
        
        revenue_info = ""
        if sources:
            revenue_info = sources[0].get("snippet", "Not available")
        
        return {
            "revenue": revenue_info,
            "funding_rounds": "Not determined",
            "total_funding": "Not determined",
            "profitability": "Not determined",
            "financial_health": "Requires further analysis",
            "key_metrics": {}
        }
    
    @staticmethod
    def _ensure_string_fields(info: Dict) -> Dict:
        """Ensure all fields are strings for database storage."""
        result = {}
        for key, value in info.items():
            if isinstance(value, (list, dict)):
                result[key] = json.dumps(value)
            else:
                result[key] = str(value) if value else ""
        return result
