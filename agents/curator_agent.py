"""
Curator Agent for Lead Research Agent using LangGraph.
Coordinates all research agents using graph-based orchestration.
"""

from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from agents.general_info_agent import GeneralInfoAgent
from agents.financial_agent import FinancialAgent
from agents.industrial_agent import IndustrialMediaAgent
from agents.decision_maker_agent import DecisionMakerAgent
from config.settings import settings
from database.db import db


class ResearchState(TypedDict):
    """State object for research workflow."""
    request_id: int
    company_name: str
    website: str
    location: str
    industry: str
    gemini_api_key: str
    general_info: Dict[str, Any]
    financial_info: Dict[str, Any]
    industry_media: Dict[str, Any]
    decision_makers: list
    errors: list


class CuratorAgent:
    """Curator agent using LangGraph for orchestration."""
    
    def __init__(self):
        """Initialize research agents and build graph."""
        self.general_agent = GeneralInfoAgent()
        self.financial_agent = FinancialAgent()
        self.industrial_agent = IndustrialMediaAgent()
        self.decision_maker_agent = DecisionMakerAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build LangGraph workflow."""
        workflow = StateGraph(ResearchState)
        
        # Add nodes
        workflow.add_node("general_info", self._general_info_node)
        workflow.add_node("financial", self._financial_node)
        workflow.add_node("industrial", self._industrial_node)
        workflow.add_node("decision_makers", self._decision_makers_node)
        workflow.add_node("aggregate", self._aggregate_node)
        
        # Set entry point
        workflow.set_entry_point("general_info")
        
        # Add edges
        workflow.add_edge("general_info", "financial")
        workflow.add_edge("financial", "industrial")
        workflow.add_edge("industrial", "decision_makers")
        workflow.add_edge("decision_makers", "aggregate")
        workflow.add_edge("aggregate", END)
        
        return workflow.compile()
    
    def _general_info_node(self, state: ResearchState) -> ResearchState:
        """Node for general information research."""
        try:
            result = self.general_agent.research(
                state["request_id"],
                state["company_name"],
                state["website"],
                state["gemini_api_key"]
            )
            state["general_info"] = result.get("data") if result.get("status") == "success" else None
            if result.get("status") == "error":
                state["errors"].append(f"General Info: {result.get('error')}")
        except Exception as e:
            state["errors"].append(f"General Info Node: {str(e)}")
        return state
    
    def _financial_node(self, state: ResearchState) -> ResearchState:
        """Node for financial information research."""
        try:
            result = self.financial_agent.research(
                state["request_id"],
                state["company_name"],
                state["gemini_api_key"]
            )
            state["financial_info"] = result.get("data") if result.get("status") == "success" else None
            if result.get("status") == "error":
                state["errors"].append(f"Financial: {result.get('error')}")
        except Exception as e:
            state["errors"].append(f"Financial Node: {str(e)}")
        return state
    
    def _industrial_node(self, state: ResearchState) -> ResearchState:
        """Node for industrial/market research."""
        try:
            result = self.industrial_agent.research(
                state["request_id"],
                state["company_name"],
                state["industry"],
                state["gemini_api_key"]
            )
            state["industry_media"] = result.get("data") if result.get("status") == "success" else None
            if result.get("status") == "error":
                state["errors"].append(f"Industrial: {result.get('error')}")
        except Exception as e:
            state["errors"].append(f"Industrial Node: {str(e)}")
        return state
    
    def _decision_makers_node(self, state: ResearchState) -> ResearchState:
        """Node for decision makers research."""
        try:
            result = self.decision_maker_agent.research(
                state["request_id"],
                state["company_name"]
            )
            state["decision_makers"] = result.get("data") if result.get("status") == "success" else []
            if result.get("status") == "error":
                state["errors"].append(f"Decision Makers: {result.get('error')}")
        except Exception as e:
            state["errors"].append(f"Decision Makers Node: {str(e)}")
        return state
    
    def _aggregate_node(self, state: ResearchState) -> ResearchState:
        """Node for aggregating results."""
        # All results are already aggregated in state
        return state
    
    def orchestrate_research(self, request_id: int, company_name: str, 
                           website: str = None, location: str = None,
                           industry: str = None, gemini_api_key: str = None) -> Dict[str, Any]:
        """
        Orchestrate research using LangGraph workflow.
        
        Args:
            request_id: Database request ID
            company_name: Company name
            website: Company website
            location: Company location
            industry: Industry classification
            gemini_api_key: API key for Gemini (loads from settings if not provided)
        
        Returns:
            Aggregated research results from all agents
        """
        try:
            # Load Gemini API key from settings if not provided
            api_key = gemini_api_key or settings.GEMINI_API_KEY or ""
            
            # Create initial state
            initial_state: ResearchState = {
                "request_id": request_id,
                "company_name": company_name,
                "website": website or "",
                "location": location or "",
                "industry": industry or "",
                "gemini_api_key": api_key,
                "general_info": None,
                "financial_info": None,
                "industry_media": None,
                "decision_makers": [],
                "errors": []
            }
            
            # Execute graph
            final_state = self.graph.invoke(initial_state)
            
            return {
                "request_id": request_id,
                "company_name": company_name,
                "general_info": final_state.get("general_info"),
                "financial_info": final_state.get("financial_info"),
                "industry_media": final_state.get("industry_media"),
                "decision_makers": final_state.get("decision_makers", []),
                "errors": final_state.get("errors", [])
            }
        
        except Exception as e:
            db.update_request_status(request_id, "failed", str(e))
            return {
                "request_id": request_id,
                "company_name": company_name,
                "general_info": None,
                "financial_info": None,
                "industry_media": None,
                "decision_makers": [],
                "errors": [f"Curator Graph: {str(e)}"]
            }
