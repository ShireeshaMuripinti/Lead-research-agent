"""
Database initialization and management for Lead Research Agent.
Handles SQLite database operations and schema creation.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from contextlib import contextmanager
from config.settings import settings

class Database:
    """Database connection and operations handler."""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection."""
        self.db_path = db_path or settings.DATABASE_PATH
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database and tables if they don't exist."""
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not db_file.exists():
            self._create_tables()
    
    def _create_tables(self):
        """Create all required tables using schema.sql."""
        schema_path = Path(__file__).parent / "schema.sql"
        
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        with self.get_connection() as conn:
            conn.executescript(schema)
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    # Research Request Methods
    
    def create_research_request(self, company_name: str, website: str = None, 
                                location: str = None, industry: str = None) -> int:
        """Create a new research request."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO research_requests (company_name, website, location, industry, status)
                VALUES (?, ?, ?, ?, 'pending')
            """, (company_name, website, location, industry))
            conn.commit()
            return cursor.lastrowid
    
    def get_research_request(self, request_id: int) -> Optional[Dict]:
        """Retrieve a research request by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM research_requests WHERE id = ?", (request_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_request_status(self, request_id: int, status: str, error_message: str = None):
        """Update research request status."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE research_requests 
                SET status = ?, error_message = ?
                WHERE id = ?
            """, (status, error_message, request_id))
            conn.commit()
    
    def get_all_requests(self, limit: int = 50) -> List[Dict]:
        """Get all research requests with limit."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM research_requests 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    # General Info Results Methods
    
    def save_general_info(self, request_id: int, info: Dict) -> int:
        """Save general information results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO general_info_results 
                (request_id, company_description, founded_year, company_size, headquarters, website_url, linkedin_profile)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                request_id,
                json.dumps(info.get('company_description')) if isinstance(info.get('company_description'), (list, dict)) else str(info.get('company_description', '')),
                json.dumps(info.get('founded_year')) if isinstance(info.get('founded_year'), (list, dict)) else str(info.get('founded_year', '')),
                json.dumps(info.get('company_size')) if isinstance(info.get('company_size'), (list, dict)) else str(info.get('company_size', '')),
                json.dumps(info.get('headquarters')) if isinstance(info.get('headquarters'), (list, dict)) else str(info.get('headquarters', '')),
                json.dumps(info.get('website_url')) if isinstance(info.get('website_url'), (list, dict)) else str(info.get('website_url', '')),
                json.dumps(info.get('linkedin_profile')) if isinstance(info.get('linkedin_profile'), (list, dict)) else str(info.get('linkedin_profile', ''))
            ))
            conn.commit()
            return cursor.lastrowid
    
    # Financial Results Methods
    
    def save_financial_info(self, request_id: int, info: Dict) -> int:
        """Save financial information results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO financial_results 
                (request_id, revenue, funding_rounds, total_funding, profitability, financial_health, key_metrics)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                request_id,
                json.dumps(info.get('revenue', '')) if isinstance(info.get('revenue'), (list, dict)) else str(info.get('revenue', '')),
                json.dumps(info.get('funding_rounds', [])) if isinstance(info.get('funding_rounds'), (list, dict)) else str(info.get('funding_rounds', '')),
                json.dumps(info.get('total_funding', '')) if isinstance(info.get('total_funding'), (list, dict)) else str(info.get('total_funding', '')),
                json.dumps(info.get('profitability', '')) if isinstance(info.get('profitability'), (list, dict)) else str(info.get('profitability', '')),
                json.dumps(info.get('financial_health', '')) if isinstance(info.get('financial_health'), (list, dict)) else str(info.get('financial_health', '')),
                json.dumps(info.get('key_metrics', {}))
            ))
            conn.commit()
            return cursor.lastrowid
    
    # Industrial & Media Results Methods
    
    def save_industrial_media_info(self, request_id: int, info: Dict) -> int:
        """Save industrial and media information results with SWOT analysis."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO industrial_media_results 
                (request_id, industry_vertical, market_position, competitors, market_trends, media_coverage, press_releases, swot_strengths, swot_weaknesses, swot_opportunities, swot_threats)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                request_id,
                info.get('industry_vertical'),
                info.get('market_position'),
                json.dumps(info.get('competitors', [])) if isinstance(info.get('competitors'), (list, dict)) else str(info.get('competitors', '')),
                json.dumps(info.get('market_trends', [])) if isinstance(info.get('market_trends'), (list, dict)) else str(info.get('market_trends', '')),
                json.dumps(info.get('media_coverage', [])) if isinstance(info.get('media_coverage'), (list, dict)) else str(info.get('media_coverage', '')),
                json.dumps(info.get('press_releases', [])) if isinstance(info.get('press_releases'), (list, dict)) else str(info.get('press_releases', '')),
                json.dumps(info.get('swot_strengths', [])) if isinstance(info.get('swot_strengths'), (list, dict)) else str(info.get('swot_strengths', '')),
                json.dumps(info.get('swot_weaknesses', [])) if isinstance(info.get('swot_weaknesses'), (list, dict)) else str(info.get('swot_weaknesses', '')),
                json.dumps(info.get('swot_opportunities', [])) if isinstance(info.get('swot_opportunities'), (list, dict)) else str(info.get('swot_opportunities', '')),
                json.dumps(info.get('swot_threats', [])) if isinstance(info.get('swot_threats'), (list, dict)) else str(info.get('swot_threats', ''))
            ))
            conn.commit()
            return cursor.lastrowid
    
    # Decision Makers Methods
    
    def save_decision_maker(self, request_id: int, maker: Dict) -> int:
        """Save a decision maker/business lead with all contact details."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO decision_makers 
                (request_id, name, title, email, phone, linkedin_profile, other_profiles, source_url, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                request_id,
                str(maker.get('name', '')),
                str(maker.get('title', '')),
                str(maker.get('email', '')) if maker.get('email') else None,
                str(maker.get('phone', '')) if maker.get('phone') else None,
                str(maker.get('linkedin_profile', '')) if maker.get('linkedin_profile') else None,
                str(maker.get('other_profiles', '')) if maker.get('other_profiles') else None,
                str(maker.get('source_url', '')) if maker.get('source_url') else None,
                str(maker.get('confidence', 'medium'))
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_decision_makers(self, request_id: int) -> List[Dict]:
        """Get all decision makers for a research request."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM decision_makers 
                WHERE request_id = ?
                ORDER BY created_at DESC
            """, (request_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    # Research Report Methods
    
    def create_research_report(self, request_id: int, title: str, executive_summary: str,
                              general_info: Dict, financial: Dict, industrial_media: Dict,
                              decision_makers: List[Dict], recommendations: str) -> int:
        """Create a comprehensive research report."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Combine all data into report content
            report_content = self._generate_report_content(
                title, executive_summary, general_info, financial, 
                industrial_media, decision_makers, recommendations
            )
            
            cursor.execute("""
                INSERT INTO research_reports 
                (request_id, title, executive_summary, general_info_json, financial_json, 
                 industrial_media_json, decision_makers_json, recommendations, report_content, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'final')
            """, (
                request_id,
                title,
                executive_summary,
                json.dumps(general_info),
                json.dumps(financial),
                json.dumps(industrial_media),
                json.dumps(decision_makers),
                recommendations,
                report_content
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_research_report(self, report_id: int) -> Optional[Dict]:
        """Retrieve a research report by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM research_reports WHERE id = ?", (report_id,))
            row = cursor.fetchone()
            if row:
                result = dict(row)
                # Parse JSON fields
                result['general_info_json'] = json.loads(result['general_info_json'])
                result['financial_json'] = json.loads(result['financial_json'])
                result['industrial_media_json'] = json.loads(result['industrial_media_json'])
                result['decision_makers_json'] = json.loads(result['decision_makers_json'])
                return result
            return None
    
    def get_report_by_request(self, request_id: int) -> Optional[Dict]:
        """Retrieve a research report by request ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM research_reports WHERE request_id = ?", (request_id,))
            row = cursor.fetchone()
            if row:
                result = dict(row)
                # Parse JSON fields
                result['general_info_json'] = json.loads(result['general_info_json'])
                result['financial_json'] = json.loads(result['financial_json'])
                result['industrial_media_json'] = json.loads(result['industrial_media_json'])
                result['decision_makers_json'] = json.loads(result['decision_makers_json'])
                return result
            return None
    
    # Chat History Methods
    
    def save_chat_message(self, report_id: int, query: str, response: str):
        """Save chat message to history."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Ensure both are strings
            query_str = str(query) if query else ""
            response_str = str(response) if response else ""
            
            cursor.execute("""
                INSERT INTO chat_history (report_id, user_query, assistant_response)
                VALUES (?, ?, ?)
            """, (report_id, query_str, response_str))
            conn.commit()
    
    def get_chat_history(self, report_id: int, limit: int = 50) -> List[Dict]:
        """Get chat history for a report."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM chat_history 
                WHERE report_id = ?
                ORDER BY created_at DESC 
                LIMIT ?
            """, (report_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    # Cache Methods
    
    def save_search_cache(self, query: str, results: List[Dict], expires_days: int = 7):
        """Save search results to cache."""
        expires_at = datetime.now() + timedelta(days=expires_days)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO research_cache (query, search_results, expires_at)
                VALUES (?, ?, ?)
            """, (query, json.dumps(results), expires_at))
            conn.commit()
    
    def get_search_cache(self, query: str) -> Optional[List[Dict]]:
        """Retrieve cached search results if not expired."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT search_results FROM research_cache 
                WHERE query = ? AND expires_at > datetime('now')
            """, (query,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None
    
    @staticmethod
    def _generate_report_content(title: str, executive_summary: str, general_info: Dict,
                                financial: Dict, industrial_media: Dict,
                                decision_makers: List[Dict], recommendations: str) -> str:
        """Generate formatted report content."""
        report = f"""
# {title}

## Executive Summary
{executive_summary}

## General Information
{json.dumps(general_info, indent=2)}

## Financial Information
{json.dumps(financial, indent=2)}

## Industrial & Market Analysis
{json.dumps(industrial_media, indent=2)}

## Decision Makers & Business Leads
{json.dumps(decision_makers, indent=2)}

## Recommendations
{recommendations}
"""
        return report


# Initialize global database instance
db = Database()
