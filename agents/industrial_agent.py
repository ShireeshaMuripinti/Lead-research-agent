"""
Industrial & Media Agent for Lead Research Agent.
Enhanced version with targeted research questions for better industry analysis.
"""

from typing import Dict, Any
from utils.tavily_search import get_tavily_searcher
from utils.gemini_integration import get_gemini_analyzer
from utils.logging_util import ResearchLogger
from database.db import db
import json


class IndustrialMediaAgent:
    """Research agent for industry and media information with targeted research questions."""
    
    # Strategic industry research questions
    RESEARCH_QUESTIONS = {
        "industry_classification": [
            "What industry vertical does the company operate in?",
            "What are the key industry trends and dynamics?",
            "What regulatory environment affects this industry?",
        ],
        "competitive_position": [
            "Who are the main competitors in this market?",
            "What is the company's market position vs competitors?",
            "What are the company's competitive advantages?",
        ],
        "market_trends": [
            "What are current market trends affecting the company?",
            "What is the market size and growth rate?",
            "What are emerging opportunities and threats?",
        ],
        "media_coverage": [
            "What recent news or media coverage mentions the company?",
            "What is the sentiment of recent coverage?",
            "What are major announcements or press releases?",
        ],
        "industry_recognition": [
            "What awards or recognition has the company received?",
            "What analyst reports mention the company?",
            "What is the company's industry reputation?",
        ],
    }
    
    def __init__(self):
        """Initialize the agent."""
        self.searcher = None
        self.analyzer = None
    
    def research(self, request_id: int, company_name: str, industry: str = None,
                gemini_api_key: str = None) -> Dict[str, Any]:
        """
        Research industry position and media coverage with targeted questions.
        
        Args:
            request_id: Database request ID
            company_name: Company name
            industry: Optional industry classification
            gemini_api_key: Gemini API key for enhanced analysis
        
        Returns:
            Dictionary with comprehensive industry and media information
        """
        logger = ResearchLogger(request_id)
        
        try:
            logger.log_agent_start("IndustrialMediaAgent", {
                "company_name": company_name,
                "industry": industry,
                "research_questions": len(self.RESEARCH_QUESTIONS)
            })
            
            # Initialize searcher with request_id for logging
            self.searcher = get_tavily_searcher(request_id=request_id)
            # Search for industry and media information
            logger.logger.info(f"Starting Tavily search for industry/media information on '{company_name}'")
            search_results = self.searcher.search_company_industry_media(company_name, industry)
            
            # Log search results
            if search_results.get("sources"):
                logger.logger.info(f"Found {len(search_results.get('sources', []))} industry/media sources:")
                for idx, source in enumerate(search_results.get("sources", [])[:5]):
                    logger.logger.debug(f"  Source {idx+1}: {source.get('title')} ({source.get('url')})")
                    logger.logger.debug(f"    Snippet: {source.get('snippet', '')[:200]}...")
            
            # Analyze with Gemini if available
            if gemini_api_key:
                logger.logger.info("Analyzing industry/media results with Gemini API")
                self.analyzer = get_gemini_analyzer(api_key=gemini_api_key, logger=logger)
                industry_info = self.analyzer.analyze_industry_media(search_results)
                logger.logger.info("✅ Gemini industry/media analysis completed")
            else:
                logger.logger.info("No Gemini API key - using basic industry/media parsing")
                industry_info = self._parse_basic_industry(search_results)
            
            # Ensure all fields are strings
            industry_info = self._ensure_string_fields(industry_info)
            
            # Save to database
            db.save_industrial_media_info(request_id, industry_info)
            logger.log_database_save("industrial_media_results", 1, {"company": company_name})
            
            logger.log_agent_complete("IndustrialMediaAgent", {
                "status": "success",
                "fields_extracted": list(industry_info.keys())
            })
            
            return {
                "status": "success",
                "data": industry_info,
                "raw_sources": search_results.get("sources", []),
                "research_questions_count": sum(len(q) for q in self.RESEARCH_QUESTIONS.values())
            }
        
        except Exception as e:
            logger.log_error("IndustrialMediaAgent", str(e))
            return {
                "status": "error",
                "error": str(e)
            }
    
    @staticmethod
    def _parse_basic_industry(search_results: Dict) -> Dict[str, Any]:
        """Extract basic industry information without AI."""
        sources = search_results.get("sources", [])
        
        competitors = []
        media_coverage = []
        
        for source in sources[:3]:
            if "competitor" in source.get("title", "").lower():
                competitors.append(source.get("title", ""))
            else:
                media_coverage.append(source.get("snippet", ""))
        
        return {
            "industry_vertical": "Not determined",
            "market_position": "Requires further analysis",
            "competitors": competitors if competitors else "Not determined",
            "market_trends": "Not available",
            "media_coverage": media_coverage if media_coverage else "Not available",
            "press_releases": "Not available"
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
