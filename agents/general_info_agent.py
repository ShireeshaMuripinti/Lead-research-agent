"""
General Information Agent for Lead Research Agent.
Enhanced version with targeted research questions for better analysis.
"""

from typing import Dict, Any
from utils.tavily_search import get_tavily_searcher
from utils.gemini_integration import get_gemini_analyzer
from utils.logging_util import ResearchLogger
from database.db import db
import json


class GeneralInfoAgent:
    """Research agent for general company information with targeted research questions."""
    
    # Strategic research questions that analysts ask
    RESEARCH_QUESTIONS = {
        "founding_and_history": [
            "When was the company founded and by whom?",
            "What is the company's founding story and key milestones?",
        ],
        "business_overview": [
            "What are the company's core products or services?",
            "What is the company's mission and value proposition?",
            "Who are the primary customer segments?",
        ],
        "organization": [
            "How many employees does the company have globally?",
            "What is the organizational structure and key departments?",
            "What is the company's leadership team composition?",
        ],
        "location_presence": [
            "Where is the company headquartered?",
            "What is the company's global presence and office locations?",
            "What are the key operational regions?",
        ],
        "digital_presence": [
            "What is the company's official website and online presence?",
            "What are the company's social media profiles and digital channels?",
            "What is the company's LinkedIn profile and online reputation?",
        ],
    }
    
    def __init__(self):
        """Initialize the agent."""
        self.searcher = None
        self.analyzer = None
    
    def research(self, request_id: int, company_name: str, website: str = None, 
                gemini_api_key: str = None) -> Dict[str, Any]:
        """
        Research general information with targeted questions.
        
        Args:
            request_id: Database request ID
            company_name: Company name
            website: Optional website
            gemini_api_key: Gemini API key for enhanced analysis
        
        Returns:
            Dictionary with comprehensive general information
        """
        logger = ResearchLogger(request_id)
        
        try:
            logger.log_agent_start("GeneralInfoAgent", {
                "company_name": company_name,
                "website": website,
                "research_questions": len(self.RESEARCH_QUESTIONS)
            })
            
            # Initialize searcher with request_id for logging
            self.searcher = get_tavily_searcher(request_id=request_id)
            
            # Update status
            db.update_request_status(request_id, "in_progress")
            
            # Perform targeted searches
            logger.logger.info(f"Starting Tavily search for general information on '{company_name}'")
            search_results = self.searcher.search_company_general_info(company_name, website)
            
            # Log search results
            if search_results.get("sources"):
                logger.logger.info(f"Found {len(search_results.get('sources', []))} sources:")
                for idx, source in enumerate(search_results.get("sources", [])[:5]):
                    logger.logger.debug(f"  Source {idx+1}: {source.get('title')} ({source.get('url')})")
                    logger.logger.debug(f"    Snippet: {source.get('snippet', '')[:200]}...")
            
            # Analyze with Gemini if available
            if gemini_api_key:
                logger.logger.info("Analyzing results with Gemini API")
                self.analyzer = get_gemini_analyzer(api_key=gemini_api_key, logger=logger)
                general_info = self.analyzer.analyze_general_info(search_results)
                logger.logger.info("✅ Gemini analysis completed")
            else:
                logger.logger.info("No Gemini API key - using basic parsing")
                general_info = self._parse_basic_info(search_results)
            
            # Ensure all fields are strings
            general_info = self._ensure_string_fields(general_info)
            
            # Save to database
            db.save_general_info(request_id, general_info)
            logger.log_database_save("general_info_results", 1, {"company": company_name})
            
            logger.log_agent_complete("GeneralInfoAgent", {
                "status": "success",
                "fields_extracted": list(general_info.keys())
            })
            
            return {
                "status": "success",
                "data": general_info,
                "raw_sources": search_results.get("sources", []),
                "research_questions_count": sum(len(q) for q in self.RESEARCH_QUESTIONS.values())
            }
        
        except Exception as e:
            logger.log_error("GeneralInfoAgent", str(e))
            return {
                "status": "error",
                "error": str(e)
            }
    
    @staticmethod
    def _parse_basic_info(search_results: Dict) -> Dict[str, Any]:
        """Extract basic information without AI."""
        sources = search_results.get("sources", [])
        
        description = ""
        website = ""
        
        if sources:
            description = sources[0].get("snippet", "Not available")
            website = sources[0].get("url", "")
        
        return {
            "company_description": description,
            "founded_year": "Not determined",
            "company_size": "Not determined",
            "headquarters": "Not determined",
            "website_url": website,
            "linkedin_profile": "Not determined"
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
