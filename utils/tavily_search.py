"""
Tavily Search Integration for Lead Research Agent
"""

import json
import logging
from typing import List, Dict, Any
from datetime import datetime
from config.settings import settings

try:
    from tavily import Client
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False

# Setup logging for Tavily operations
logger = logging.getLogger(__name__)


class TavilySearcher:
    def __init__(self, api_key: str = None, request_id: int = None):
        if not TAVILY_AVAILABLE:
            raise ImportError("tavily-python not installed")
        
        self.api_key = api_key or settings.TAVILY_API_KEY
        self.request_id = request_id

        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found")

        # Initialize Tavily client - api_key is passed as positional argument
        self.client = Client(self.api_key)
        
        if self.request_id:
            logger.info(f"[Request {self.request_id}] Tavily searcher initialized")

    def _run_search(self, query: str, max_results: int = None) -> List[Dict]:
        try:
            if self.request_id:
                logger.info(f"[Request {self.request_id}] Tavily query: '{query}'")
            
            # Use provided max_results, or fallback to settings
            max_res = max_results if max_results is not None else settings.MAX_TAVILY_RESULTS
            response = self.client.search(query, max_results=max_res)
            results = response.get('results', [])
            
            if self.request_id:
                logger.info(f"[Request {self.request_id}] Found {len(results)} results for '{query}'")
                for idx, result in enumerate(results[:3]):
                    logger.debug(f"[Request {self.request_id}]   Result {idx+1}: {result.get('title')} - {result.get('url')}")
            
            return results
        except Exception as e:
            error_msg = f"Search error for query '{query}': {str(e)}"
            if self.request_id:
                logger.error(f"[Request {self.request_id}] {error_msg}")
            else:
                logger.error(error_msg)
            return []

    def _search_general_info(self, query: str):
        """Search for general company information with 8 comprehensive queries."""
        queries = [
            f"{query} company overview",
            f"{query} about us",
            f"{query} company profile",
            f"{query} founding history leadership team",
            f"{query} mission vision values",
            f"{query} business model operations",
            f"{query} headquarters location global presence",
            f"{query} website contact information",
        ]

        if self.request_id:
            logger.info(f"[Request {self.request_id}] Starting general info searches with 8 queries")

        results = {q: self._run_search(q, max_results=10) for q in queries}
        return self._aggregate_results(results, "general_info")

    def search_company_general_info(self, company_name: str, website: str = None):
        return self._search_general_info(company_name)

    def _search_financial_info(self, query: str):
        """Search for financial information with 8 comprehensive queries."""
        queries = [
            f"{query} revenue funding",
            f"{query} financial information",
            f"{query} valuation market cap",
            f"{query} investors funding rounds",
            f"{query} profitability earnings net income",
            f"{query} annual revenue financial results",
            f"{query} stock price market valuation",
            f"{query} financial performance metrics ratios",
        ]

        if self.request_id:
            logger.info(f"[Request {self.request_id}] Starting financial info searches with 8 queries")

        results = {q: self._run_search(q, max_results=10) for q in queries}
        return self._aggregate_results(results, "financial")

    def search_company_financial_info(self, company_name: str):
        return self._search_financial_info(company_name)

    def _search_industry_media(self, query: str, industry: str = None):
        """Search for industry and media information with 8 comprehensive queries."""
        queries = [
            f"{query} industry competitors",
            f"{query} market position",
            f"{query} news articles",
            f"{query} press releases",
            f"{query} industry trends analysis",
            f"{query} market size growth opportunities",
            f"{query} regulatory environment compliance",
            f"{query} competitive advantages industry ranking",
        ]

        if industry:
            queries.append(f"{industry} market analysis {query}")

        if self.request_id:
            logger.info(f"[Request {self.request_id}] Starting industry/media searches with 8 queries")

        results = {q: self._run_search(q, max_results=10) for q in queries}
        return self._aggregate_results(results, "industry_media")

    def search_company_industry_media(self, company_name: str, industry: str = None):
        return self._search_industry_media(company_name, industry)

    def _search_decision_makers(self, query: str):
        """Search for decision makers with 8 targeted queries for comprehensive coverage."""
        queries = [
            f"{query} CEO founder president executive leadership",
            f"{query} chief technology officer CTO VP technology engineering",
            f"{query} chief financial officer CFO VP finance accounting",
            f"{query} VP sales business development senior vice president commercial",
            f"{query} VP operations chief operating officer COO operations",
            f"{query} HR director human resources talent people organizational",
            f"{query} board members board of directors advisory board",
            f"{query} key executives management team linkedin profiles",
        ]

        if self.request_id:
            logger.info(f"[Request {self.request_id}] Starting decision makers search with 8 queries")

        # Use max_results=10 for decision maker searches to get more comprehensive data
        results = {q: self._run_search(q, max_results=10) for q in queries}
        return self._extract_contacts(results)

    def search_decision_makers(self, company_name: str):
        return self._search_decision_makers(company_name)

    @staticmethod
    def _aggregate_results(results: Dict, result_type: str):
        aggregated = {
            "type": result_type,
            "timestamp": datetime.now().isoformat(),
            "sources": [],
            "raw_data": results
        }

        seen_urls = set()

        for query_results in results.values():
            if isinstance(query_results, list):
                for result in query_results:
                    url = result.get("url")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        aggregated["sources"].append({
                            "url": url,
                            "title": result.get("title"),
                            "snippet": result.get("content"),
                        })

        return aggregated

    @staticmethod
    def _extract_contacts(results: Dict) -> List[Dict[str, Any]]:
        """Extract clean, structured contact information from search results with 8-query comprehensive parsing."""
        import re
        
        contacts = []
        seen_names = set()
        seen_emails = set()

        for query_results in results.values():
            if isinstance(query_results, list):
                for result in query_results:
                    content = result.get('content', '')
                    url = result.get('url', '')
                    
                    # Skip short content
                    if len(content) < 20:
                        continue
                    
                    # Parse individual names with improved regex patterns
                    # Pattern 1: "Name - Title" or "Name – Title"
                    pattern1 = r'([A-Z][a-z]+ (?:[A-Z][a-z]+)*?)\s*(?:-|–|—)\s*([A-Za-z\s,&()]+?)(?:\.|,|;|$)'
                    # Pattern 2: "Name, Title" format
                    pattern2 = r'([A-Z][a-z]+ (?:[A-Z][a-z]+)*?),\s*([A-Za-z\s,&()]+?)(?:\.|,|$)'
                    # Pattern 3: "Name serves as/is Title"
                    pattern3 = r'([A-Z][a-z]+ (?:[A-Z][a-z]+)*?)\s+(?:serves as|is|was)\s+(?:the\s+)?([A-Za-z\s,&()]+?)(?:\.|,|;|$)'
                    
                    patterns = [pattern1, pattern2, pattern3]
                    
                    for pattern in patterns:
                        matches = re.finditer(pattern, content, re.MULTILINE)
                        for match in matches:
                            name = match.group(1).strip()
                            role = match.group(2).strip()
                            
                            # Validate name: must be 2+ words, 3+ chars minimum per word
                            name_parts = name.split()
                            if len(name_parts) < 2 or any(len(part) < 2 for part in name_parts):
                                continue
                            
                            # Skip if name already seen or contains common noise
                            if name in seen_names or len(name) > 100:
                                continue
                            if any(skip.lower() in name.lower() for skip in ['menu', 'navigation', 'subscribe']):
                                continue
                            
                            # Clean role: limit to first meaningful part (before "at", "of", etc)
                            role = re.sub(r'\s+at\b.*', '', role, flags=re.IGNORECASE).strip()
                            role = re.sub(r'\s+of\b.*', '', role, flags=re.IGNORECASE).strip()
                            # Limit role length to 80 chars
                            role = role[:80] if role else 'Executive'
                            
                            seen_names.add(name)
                            
                            # Extract email from entire content
                            email = None
                            email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
                            email_matches = re.findall(email_pattern, content)
                            if email_matches:
                                # Prioritize emails from search result, avoid duplicates
                                for em in email_matches:
                                    if em not in seen_emails:
                                        email = em
                                        seen_emails.add(em)
                                        break
                            
                            # Extract phone number
                            phone = None
                            phone_pattern = r'\+?1?\s*\(?([0-9]{3})\)?[\s.\-]?([0-9]{3})[\s.\-]?([0-9]{4})\b'
                            phone_matches = re.findall(phone_pattern, content)
                            if phone_matches:
                                phone = f"({phone_matches[0][0]}) {phone_matches[0][1]}-{phone_matches[0][2]}"
                            
                            # Extract LinkedIn profile URL
                            linkedin = None
                            linkedin_match = re.search(r'(https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9-]+)/?', url, re.IGNORECASE)
                            if linkedin_match:
                                linkedin = linkedin_match.group(1)
                            else:
                                # Try to find in content
                                linkedin_match = re.search(r'linkedin\.com/in/([a-zA-Z0-9-]+)', content, re.IGNORECASE)
                                if linkedin_match:
                                    linkedin = f"https://linkedin.com/in/{linkedin_match.group(1)}"
                            
                            # Extract other platforms (Twitter, GitHub, etc)
                            other_profiles = None
                            if 'linkedin' not in url.lower():
                                # Extract social profiles if URL is not LinkedIn
                                if any(platform in url.lower() for platform in ['twitter', 'github', 'facebook', 'instagram']):
                                    other_profiles = url
                            
                            # Create contact record with high confidence if has email/phone
                            contact = {
                                "name": name,
                                "title": role,
                                "email": email,
                                "phone": phone,
                                "linkedin_profile": linkedin,
                                "other_profiles": other_profiles,
                                "source_url": url,
                                "confidence": "high" if (email or phone) else "medium"
                            }
                            contacts.append(contact)
                            
                            # Limit to top 10 unique contacts for quality
                            if len(contacts) >= 10:
                                return contacts

        return contacts[:10]  # Return top 10 contacts


def get_tavily_searcher(request_id: int = None) -> TavilySearcher:
    return TavilySearcher(request_id=request_id)