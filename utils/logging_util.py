"""
Logging utility for the Lead Research Agent.
Provides structured logging for all research activities.
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from config.settings import settings


class ResearchLogger:
    """Centralized logging for research operations."""
    
    def __init__(self, request_id: int):
        """Initialize logger for a specific research request."""
        self.request_id = request_id
        self.log_dir = Path(settings.LOG_DIR)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.log_dir / f"research_{request_id}.log"
        
        self.logger = logging.getLogger(f"research_{request_id}")
        self.logger.setLevel(getattr(logging, settings.LOG_LEVEL))
        
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_agent_start(self, agent_name: str, details: dict = None):
        """Log when an agent starts research."""
        msg = f"Agent '{agent_name}' starting research"
        if details:
            msg += f": {json.dumps(details, indent=2)}"
        self.logger.info(msg)
    
    def log_agent_complete(self, agent_name: str, results: dict):
        """Log when an agent completes research."""
        status = results.get("status", "unknown")
        msg = f"Agent '{agent_name}' completed with status: {status}"
        self.logger.info(msg)
        if results.get("data"):
            self.logger.debug(f"Results: {json.dumps(results.get('data'), indent=2, default=str)}")
    
    def log_error(self, agent_name: str, error: str):
        """Log errors during research."""
        self.logger.error(f"Agent '{agent_name}' error: {error}")
    
    def log_search_query(self, agent_name: str, query: str):
        """Log search queries."""
        self.logger.debug(f"Agent '{agent_name}' search query: {query}")
    
    def log_research_complete(self, summary: dict):
        """Log when entire research is complete."""
        self.logger.info(f"Research complete: {json.dumps(summary, indent=2, default=str)}")
    
    def log_llm_call(self, agent_name: str, section: str, prompt_length: int):
        """Log LLM (Gemini) API call details."""
        self.logger.info(f"[LLM] Agent '{agent_name}' - Section '{section}' - Sending prompt ({prompt_length} chars) to Gemini")
    
    def log_llm_response(self, agent_name: str, section: str, response_length: int, analysis_fields: list = None):
        """Log LLM (Gemini) response details."""
        msg = f"[LLM] Agent '{agent_name}' - Section '{section}' - Received analysis ({response_length} chars)"
        if analysis_fields:
            msg += f" with fields: {', '.join(analysis_fields)}"
        self.logger.info(msg)
    
    def log_tavily_search_start(self, agent_name: str, search_type: str, query: str):
        """Log Tavily search initiation."""
        self.logger.info(f"[TAVILY] Agent '{agent_name}' - {search_type} - Query: '{query}'")
    
    def log_tavily_results(self, agent_name: str, search_type: str, result_count: int, top_results: list = None):
        """Log Tavily search results."""
        msg = f"[TAVILY] Agent '{agent_name}' - {search_type} - Found {result_count} results"
        if top_results:
            for i, result in enumerate(top_results[:3], 1):
                title = result.get('title', 'N/A')[:50]
                url = result.get('url', 'N/A')[:60]
                msg += f"\n  [{i}] {title} | {url}"
        self.logger.info(msg)
    
    def log_database_save(self, table_name: str, record_count: int, details: dict = None):
        """Log database save operations."""
        msg = f"[DATABASE] Saved {record_count} record(s) to '{table_name}'"
        if details:
            msg += f": {json.dumps(details, default=str)}"
        self.logger.info(msg)
    
    def log_app_event(self, event_type: str, details: str):
        """Log application-level events."""
        self.logger.info(f"[APP] {event_type}: {details}")
    
    def get_log_path(self) -> str:
        """Get the path to the log file."""
        return str(self.log_file)
