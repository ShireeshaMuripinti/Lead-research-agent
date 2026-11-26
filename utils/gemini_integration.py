"""
Google Gemini Integration for Lead Research Agent.
Uses the latest google-genai SDK with HTML table formatting and streaming.
"""

import json
from typing import Dict, List, Any
from config.settings import settings

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class GeminiAnalyzer:
    """Gemini AI integration for research analysis using latest google-genai SDK."""
    
    def __init__(self, api_key: str = None, logger=None):
        """Initialize Gemini client.
        
        Args:
            api_key: Gemini API key (defaults to settings.GEMINI_API_KEY)
            logger: Optional ResearchLogger instance for logging LLM calls
        """
        if not GEMINI_AVAILABLE:
            raise ImportError("google-genai not installed. Install with: pip install google-genai")
        
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.logger = logger
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = settings.GEMINI_MODEL or "gemini-2-0-flash"
    
    def _generate_with_thinking(self, prompt: str) -> str:
        """Generate content with extended thinking for better analysis."""
        try:
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)],
                ),
            ]
            
            generate_content_config = types.GenerateContentConfig(
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=4096,
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            )
            
            return response.text if hasattr(response, 'text') else str(response)
        
        except Exception as e:
            print(f"Error generating with thinking: {str(e)}")
            return f"Error: {str(e)}"
    
    def analyze_general_info(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze general company information using Gemini."""
        prompt = f"""Extract and provide well-formatted company information based on these search results.

Provide information about:
1. Company description - 2-3 sentences about what the company does
2. Founded year - Just the year
3. Company size - Employee count or range
4. Headquarters - City and country
5. Website URL - Full URL if available
6. LinkedIn profile - Full LinkedIn URL if available

Search results:
{json.dumps(search_results, indent=2)}

Return ONLY a valid JSON object, no markdown or explanations."""
        
        if self.logger:
            self.logger.log_llm_call("GeneralInfoAgent", "Company Fundamentals", len(prompt))
        
        response = self._generate_with_thinking(prompt)
        
        if self.logger:
            self.logger.log_llm_response("GeneralInfoAgent", "Company Fundamentals", len(response),
                                        ["company_description", "founded_year", "company_size", "headquarters", "website_url", "linkedin_profile"])
        
        return self._parse_json_response(response)
    
    def analyze_financial_info(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial information using Gemini."""
        prompt = f"""Extract and provide well-formatted financial information based on these search results.

Extract information about:
1. Revenue - Most recent annual revenue (e.g., "$50M in 2024")
2. Funding rounds - List of funding rounds with amounts
3. Total funding - Total amount raised
4. Profitability - Profitable or not, with status
5. Financial health - Overall assessment in 1-2 sentences
6. Key metrics - 2-3 important financial metrics

Search results:
{json.dumps(search_results, indent=2)}

Return ONLY a valid JSON object, no markdown or explanations."""
        
        if self.logger:
            self.logger.log_llm_call("FinancialAgent", "Financial Metrics", len(prompt))
        
        response = self._generate_with_thinking(prompt)
        
        if self.logger:
            self.logger.log_llm_response("FinancialAgent", "Financial Metrics", len(response),
                                        ["revenue", "funding_rounds", "total_funding", "profitability", "financial_health", "key_metrics"])
        
        return self._parse_json_response(response)
    
    def analyze_industry_media(self, search_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze industry position, media coverage, and SWOT analysis."""
        prompt = f"""Extract and provide well-formatted industry and market information based on these search results.

Provide information about:
1. Industry vertical - The industry/sector the company operates in
2. Market position - Company's position relative to competitors
3. Competitors - Main competitors (comma-separated list)
4. Market trends - Key trends affecting the industry
5. Media coverage - Recent media mentions and articles
6. Press releases - Recent press releases or announcements
7. SWOT Analysis - Provide a comprehensive SWOT analysis with:
   - swot_strengths: Array of 3-5 key internal strengths
   - swot_weaknesses: Array of 3-5 key internal weaknesses
   - swot_opportunities: Array of 3-5 external opportunities
   - swot_threats: Array of 3-5 external threats

Search results:
{json.dumps(search_results, indent=2)}

Return ONLY a valid JSON object, no markdown or explanations."""
        
        if self.logger:
            self.logger.log_llm_call("IndustrialMediaAgent", "Industry & Market Position", len(prompt))
        
        response = self._generate_with_thinking(prompt)
        
        if self.logger:
            self.logger.log_llm_response("IndustrialMediaAgent", "Industry & Market Position", len(response),
                                        ["industry_vertical", "market_position", "competitors", "market_trends", "media_coverage", "press_releases", "swot_strengths", "swot_weaknesses", "swot_opportunities", "swot_threats"])
        
        return self._parse_json_response(response)
    
    def generate_executive_summary(self, company_name: str, general_info: Dict,
                                  financial_info: Dict, industry_info: Dict) -> str:
        """Generate executive summary using Gemini with proper HTML formatting."""
        prompt = f"""Create a concise executive summary (2-3 paragraphs) for {company_name}.

Company Overview:
- Founded: {general_info.get('founded_year', 'Unknown')}
- Size: {general_info.get('company_size', 'Unknown')}
- Headquarters: {general_info.get('headquarters', 'Unknown')}
- Description: {general_info.get('company_description', 'Unknown')}

Financial Status:
- Revenue: {financial_info.get('revenue', 'Unknown')}
- Total Funding: {financial_info.get('total_funding', 'Unknown')}
- Profitability: {financial_info.get('profitability', 'Unknown')}
- Health: {financial_info.get('financial_health', 'Unknown')}

Market Position:
- Industry: {industry_info.get('industry_vertical', 'Unknown')}
- Position: {industry_info.get('market_position', 'Unknown')}

Format your response as follows:
<div class="summary-content">
<p>First paragraph about company overview and positioning</p>
<p>Second paragraph about financial status and metrics</p>
<p>Third paragraph about market opportunity and future outlook</p>
</div>

Return ONLY the HTML content, no code blocks or markdown."""
        
        return self._generate_with_thinking(prompt)
    
    def generate_recommendations(self, company_name: str, general_info: Dict,
                                financial_info: Dict, industry_info: Dict,
                                decision_makers: List[Dict]) -> str:
        """Generate actionable recommendations using Gemini with proper HTML table formatting."""
        prompt = f"""Based on the research about {company_name}, provide 5-7 strategic recommendations for business engagement.

Company Details:
- Name: {company_name}
- Founded: {general_info.get('founded_year', 'Unknown')}
- Size: {general_info.get('company_size', 'Unknown')}
- Industry: {industry_info.get('industry_vertical', 'Unknown')}

Financial Status:
- Revenue: {financial_info.get('revenue', 'Unknown')}
- Profitability: {financial_info.get('profitability', 'Unknown')}

Key Contacts ({len(decision_makers)} identified):
{json.dumps(decision_makers[:5], indent=2)}

Format your response as an HTML table with these columns: Recommendation | Priority | Timeline | Key Contact | Expected Impact

Structure:
<table class="recommendations-table">
<thead><tr>
<th>Recommendation</th>
<th>Priority</th>
<th>Timeline</th>
<th>Key Contact</th>
<th>Expected Impact</th>
</tr></thead>
<tbody>
<tr><td>recommendation text</td><td>High/Medium/Low</td><td>timeframe</td><td>contact name/role</td><td>impact description</td></tr>
...more rows...
</tbody>
</table>

Return ONLY the HTML table, no code blocks or markdown."""
        
        return self._generate_with_thinking(prompt)
    
    def answer_query_about_report(self, query: str, report_content: str) -> str:
        """Answer user queries about the research report with HTML formatting."""
        prompt = f"""You are an expert research assistant. Answer the following question based on the provided research report.
Format your response as clean HTML suitable for web display (use tables if presenting data, use lists for points, etc).

Question: {query}

Research Report:
{report_content}

Provide a clear, accurate answer based only on information from the report.
Return ONLY the HTML content, no code blocks."""
        
        return self._generate_with_thinking(prompt)
    
    @staticmethod
    def _parse_json_response(response_text: str) -> Dict[str, Any]:
        """Parse JSON from response text."""
        try:
            # Try to extract JSON if wrapped in code blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            
            return json.loads(response_text)
        
        except json.JSONDecodeError:
            return {"raw_response": response_text}
        
        except Exception as e:
            return {"error": str(e)}


def get_gemini_analyzer(api_key: str = None, logger=None) -> GeminiAnalyzer:
    """Factory function to get Gemini analyzer instance.
    
    Args:
        api_key: Gemini API key
        logger: Optional ResearchLogger instance for logging LLM calls
    
    Returns:
        GeminiAnalyzer instance
    """
    return GeminiAnalyzer(api_key=api_key, logger=logger)
