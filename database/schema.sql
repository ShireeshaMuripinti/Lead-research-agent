-- Lead Research Agent Database Schema
-- SQLite database for storing research requests and reports

-- Research Requests Table
CREATE TABLE IF NOT EXISTS research_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    website TEXT,
    location TEXT,
    industry TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending', -- pending, in_progress, completed, failed
    error_message TEXT
);

-- General Information Node Results
CREATE TABLE IF NOT EXISTS general_info_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    company_description TEXT,
    founded_year INTEGER,
    company_size TEXT,
    headquarters TEXT,
    website_url TEXT,
    linkedin_profile TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES research_requests(id) ON DELETE CASCADE
);

-- Financial Information Node Results
CREATE TABLE IF NOT EXISTS financial_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    revenue TEXT,
    funding_rounds TEXT,
    total_funding TEXT,
    profitability TEXT,
    financial_health TEXT,
    key_metrics TEXT, -- JSON format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES research_requests(id) ON DELETE CASCADE
);

-- Industrial & Media Node Results
CREATE TABLE IF NOT EXISTS industrial_media_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    industry_vertical TEXT,
    market_position TEXT,
    competitors TEXT, -- JSON format
    market_trends TEXT,
    media_coverage TEXT,
    press_releases TEXT,
    swot_strengths TEXT, -- JSON array format
    swot_weaknesses TEXT, -- JSON array format
    swot_opportunities TEXT, -- JSON array format
    swot_threats TEXT, -- JSON array format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES research_requests(id) ON DELETE CASCADE
);

-- Decision Makers & Business Leads
CREATE TABLE IF NOT EXISTS decision_makers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    title TEXT,
    email TEXT,
    phone TEXT,
    linkedin_profile TEXT,
    other_profiles TEXT,
    department TEXT,
    source_url TEXT,
    confidence TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES research_requests(id) ON DELETE CASCADE
);

-- Final Research Report
CREATE TABLE IF NOT EXISTS research_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    executive_summary TEXT,
    general_info_json TEXT,
    financial_json TEXT,
    industrial_media_json TEXT,
    decision_makers_json TEXT,
    recommendations TEXT,
    report_content TEXT,
    status TEXT DEFAULT 'draft', -- draft, final
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES research_requests(id) ON DELETE CASCADE
);

-- Chat History (for chatbot against report)
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    user_query TEXT NOT NULL,
    assistant_response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES research_reports(id) ON DELETE CASCADE
);

-- Research Data Cache (for Tavily search results)
CREATE TABLE IF NOT EXISTS research_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT UNIQUE NOT NULL,
    search_results TEXT, -- JSON format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_research_requests_status ON research_requests(status);
CREATE INDEX IF NOT EXISTS idx_research_requests_company ON research_requests(company_name);
CREATE INDEX IF NOT EXISTS idx_research_reports_request ON research_reports(request_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_report ON chat_history(report_id);
CREATE INDEX IF NOT EXISTS idx_decision_makers_request ON decision_makers(request_id);
