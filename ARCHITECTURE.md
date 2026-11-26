# Lead Research Agent - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit Web Interface                   │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────────────┐       │
│  │ Research Input   │  │ Chat with Report         │       │
│  │  Page           │  │  Page                    │       │
│  └──────────────────┘  └──────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                     ┌────────┴────────┐
                     │                 │
          ┌──────────▼────────┐  ┌────▼──────────────┐
          │  Curator Agent    │  │  Gemini Analyzer  │
          │  (Orchestrator)   │  │  (AI Analysis)    │
          └──────┬────────────┘  └─────────────────┬─┘
                 │                                  │
        ┌────────┴──────────────────────────────────┘
        │
        │ Coordinates & Aggregates
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│              4 Specialized Research Agents                │
├────────────────┬──────────────────┬──────────────┬────────┤
│ General Info   │ Financial        │ Industrial   │Decision│
│ Agent          │ Agent            │ & Media      │Makers  │
│                │                  │ Agent        │Agent   │
│ • Company      │ • Revenue        │ • Competitors│• CEOs  │
│ • Founded      │ • Funding        │ • Market pos │• Exec  │
│ • Size         │ • Profitability  │ • Media      │• Leads │
│ • Location     │ • Health         │ • Press      │• Email │
└────────────────┴──────────────────┴──────────────┴────────┘
        ▲              ▲                  ▲            ▲
        │              │                  │            │
        │              └──────────────────┼────────────┘
        │                                 │
        │         Uses Tavily API for Search
        │
        └─────────────────────────────────┘

            ▼
┌──────────────────────────────────┐
│      Editor Agent                │
│  (Report Generation)             │
│                                  │
│  • Aggregates all findings       │
│  • Generates executive summary   │
│  • Creates recommendations       │
└──────────────────────────────────┘
            ▼
┌──────────────────────────────────┐
│     SQLite Database              │
│                                  │
│  • research_requests             │
│  • general_info_results          │
│  • financial_results             │
│  • industrial_media_results      │
│  • decision_makers               │
│  • research_reports              │
│  • chat_history                  │
└──────────────────────────────────┘
```

## 🤖 Agent Architecture

### 1. **Curator Agent** (Orchestrator)
**Purpose:** Coordinates all research agents

```python
CuratorAgent.orchestrate_research()
├── GeneralInfoAgent.research()
├── FinancialAgent.research()
├── IndustrialMediaAgent.research()
└── DecisionMakerAgent.research()
```

**Flow:**
1. Receives company details from user
2. Launches all 4 agents simultaneously (can be parallelized)
3. Aggregates results from all agents
4. Passes to Editor Agent for final report

---

### 2. **General Information Agent**
**Purpose:** Gather basic company information

**Search Queries:**
- "{Company} company overview"
- "{Company} about us"
- "{Company} company profile"

**Extracts:** Company description, founding year, size, HQ, website, LinkedIn

**Processing:**
```
Search Results → Tavily API
       ↓
Parse & Extract
       ↓
AI Analysis (Gemini) [Optional]
       ↓
Structured Data → Database
```

---

### 3. **Financial Agent**
**Purpose:** Gather financial information

**Search Queries:**
- "{Company} revenue funding"
- "{Company} financial information"
- "{Company} valuation market cap"
- "{Company} investors funding rounds"

**Extracts:** Revenue, funding rounds, total funding, profitability, financial health

---

### 4. **Industrial & Media Agent**
**Purpose:** Analyze market position and media coverage

**Search Queries:**
- "{Company} industry competitors"
- "{Company} market position"
- "{Company} news articles"
- "{Company} press releases"

**Extracts:** Industry vertical, market position, competitors, trends, media coverage

---

### 5. **Decision Maker Agent**
**Purpose:** Identify key contacts

**Search Queries:**
- "{Company} CEO founder leadership team"
- "{Company} executives management"
- "{Company} key people contact"

**Extracts:** Names, titles, positions, email, phone, LinkedIn profiles

---

### 6. **Editor Agent**
**Purpose:** Generate final comprehensive report

**Functions:**
1. `generate_executive_summary()` - AI-powered summary using Gemini
2. `generate_recommendations()` - Strategic recommendations
3. `create_research_report()` - Final formatted report
4. Database storage with all metadata

**Report Sections:**
- Executive Summary
- General Company Information
- Financial Analysis
- Market & Competitive Analysis
- Decision Makers & Contacts
- Strategic Recommendations

---

## 🔄 Data Flow

### Research Process Flow

```
User Input
    ↓
Validation (Company name, website, location)
    ↓
Create Research Request in DB
    ↓
Curator Agent Invoked
    ↓
┌──────────────────────────────┐
│  4 Agents Run (Parallel)     │
│  Each searches using Tavily  │
└──────────────────────────────┘
    ↓
Results Aggregated
    ↓
Gemini Analysis (if API key provided)
    ↓
Editor Agent Generates Report
    ↓
Report Saved to Database
    ↓
Display in UI with Tabs
    ↓
Enable Chat Interactions
```

### Chat Process Flow

```
User Query
    ↓
Send to Gemini Analyzer
    ↓
Include Report Context
    ↓
Gemini Processes Query
    ↓
Response Generated
    ↓
Save to Chat History DB
    ↓
Display in Chat UI
```

---

## 🛢️ Database Schema

### Core Tables

```sql
-- Research Requests
research_requests
├── id (Primary Key)
├── company_name
├── website
├── location
├── industry
├── status (pending|in_progress|completed|failed)
├── created_at
└── error_message

-- Result Tables (Foreign Key: request_id)
general_info_results
├── company_description
├── founded_year
├── company_size
├── headquarters
├── website_url
└── linkedin_profile

financial_results
├── revenue
├── funding_rounds
├── total_funding
├── profitability
├── financial_health
└── key_metrics (JSON)

industrial_media_results
├── industry_vertical
├── market_position
├── competitors (JSON)
├── market_trends
├── media_coverage
└── press_releases

decision_makers
├── name
├── title
├── email
├── phone
├── linkedin_profile
├── department
└── request_id (Foreign Key)

-- Reports
research_reports
├── id (Primary Key)
├── request_id (Foreign Key)
├── title
├── executive_summary
├── general_info_json
├── financial_json
├── industrial_media_json
├── decision_makers_json
├── recommendations
├── report_content
└── status (draft|final)

-- Chat History
chat_history
├── id (Primary Key)
├── report_id (Foreign Key)
├── user_query
├── assistant_response
└── created_at

-- Cache
research_cache
├── query (Unique)
├── search_results (JSON)
├── created_at
└── expires_at
```

---

## 🔌 Integration Points

### 1. **Tavily API Integration**
- **Purpose:** Online search and data gathering
- **Class:** `TavilySearcher` (utils/tavily_search.py)
- **Methods:**
  - `search_company_general_info()`
  - `search_company_financial_info()`
  - `search_company_industry_media()`
  - `search_decision_makers()`
- **Features:**
  - Caching of results
  - Configurable result limits
  - Error handling
  - Multi-query aggregation

### 2. **Google Gemini Integration**
- **Purpose:** AI-powered analysis and report generation
- **Class:** `GeminiAnalyzer` (utils/gemini_integration.py)
- **Methods:**
  - `analyze_general_info()` - Structure search data
  - `analyze_financial_info()` - Extract financial metrics
  - `analyze_industry_media()` - Analyze competitive position
  - `generate_executive_summary()` - Create summary
  - `generate_recommendations()` - Strategic insights
  - `answer_query_about_report()` - Chat responses

### 3. **SQLite Database**
- **Purpose:** Persistent data storage
- **Class:** `Database` (database/db.py)
- **Features:**
  - Context manager for connections
  - JSON field support for complex data
  - Indexed queries for performance
  - Foreign key relationships

### 4. **Google Cloud Integration**
- **Purpose:** Authentication (service account)
- **File:** `service-account-key.json`
- **Usage:** For any future GCP APIs

---

## ⚙️ Configuration System

### Environment Variables

All settings loaded from `.env` file:

```python
# config/settings.py - Settings class
GOOGLE_APPLICATION_CREDENTIALS  # Service account path
GOOGLE_PROJECT_ID              # GCP project
GEMINI_MODEL                   # Model name
GEMINI_TEMPERATURE             # Output creativity
TAVILY_API_KEY                 # Search API
DATABASE_PATH                  # DB location
MAX_TAVILY_RESULTS             # Search limit
RESEARCH_TIMEOUT               # Timeout seconds
```

### Settings Validation

```python
settings.validate()  # Checks required fields
```

---

## 🔒 Error Handling

### Multi-Level Error Handling

```
Try-Catch at Each Agent
        ↓
Error Logged to Database
        ↓
Graceful Degradation (partial results)
        ↓
User Notified in UI
        ↓
Request Status Updated
```

### Error Recovery

1. **Agent Failure:** Continue with partial results
2. **API Failure:** Fall back to basic parsing
3. **Database Error:** Retry with backoff
4. **Network Error:** Use cached results if available

---

## 🚀 Performance Optimization

### 1. **Caching**
- Search results cached in database
- TTL-based expiration
- Reduces API calls and costs

### 2. **Async Potential**
- Agents can run in parallel
- Current: Sequential execution
- Future: AsyncIO implementation

### 3. **Database Indexing**
- Indexed on frequently queried fields
- Faster request/report retrieval
- Query optimization with indexes

### 4. **Resource Management**
- Connection pooling via context managers
- Proper resource cleanup
- Memory-efficient JSON handling

---

## 📊 Scalability Considerations

### Current (Single Instance)
- SQLite suitable for < 10K requests
- Local database sufficient
- Single Streamlit instance

### Future (Production Scale)
```
├── PostgreSQL → Replace SQLite
├── Redis Cache → Replace file cache
├── Message Queue (Celery)
│   └── Async agent execution
├── API Gateway
│   └── Handle multiple concurrent requests
└── Load Balancer
    └── Multiple Streamlit instances
```

---

## 🧪 Testing Architecture

### Test Setup (test_setup.py)
1. **Import Tests:** Verify all dependencies
2. **Environment Tests:** Check configuration
3. **Database Tests:** Verify DB initialization
4. **Agent Tests:** Check agent initialization
5. **Utility Tests:** Validate helper functions

---

## 📈 Monitoring & Logging

### Current Logging
- Print statements to console
- Database error logging
- Status updates in DB

### Future Enhancements
- File-based logging system
- Structured logging (JSON)
- Performance metrics
- API call statistics

---

## 🔄 Future Architecture Enhancements

1. **Machine Learning Integration**
   - Sentiment analysis on media coverage
   - Company classification ML model
   - Prediction models

2. **Advanced Parsing**
   - NLP for contact extraction
   - Named entity recognition
   - Custom data parsers

3. **Distributed Execution**
   - Celery task queue
   - Redis result backend
   - Multiple worker nodes

4. **Enhanced UI**
   - Data visualization (Plotly, Charts)
   - Export to PDF/Excel
   - Collaborative features
   - User authentication

5. **API Layer**
   - REST API for programmatic access
   - GraphQL endpoint
   - WebSocket for real-time updates

---

## 📚 References

- Streamlit: https://docs.streamlit.io/
- Tavily API: https://tavily.com/
- Google Gemini: https://ai.google.dev/
- SQLAlchemy: https://www.sqlalchemy.org/

---

**Architecture designed for educational final year project with scalability for production deployment.**
