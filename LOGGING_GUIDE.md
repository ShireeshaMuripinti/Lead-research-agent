# Complete Logging Guide - Lead Research Agent

## 📊 Logging Architecture

Your system captures **complete visibility** into the entire research workflow with logs organized by layer:

```
logs/
├── research_1.log          # Request ID 1 - All logs for this research
├── research_2.log          # Request ID 2 - All logs for this research
└── research_N.log          # Request ID N - All logs for this research
```

---

## 🔍 What Gets Logged (Complete List)

### 1️⃣ APPLICATION LEVEL LOGS `[APP]`
- Research request started/completed
- Request status updates
- Errors and exceptions
- Report generation events
- User interactions

**Example:**
```
2024-04-28 10:30:45 - research_1 - INFO - [APP] Research started: CompanyName research
2024-04-28 10:32:15 - research_1 - INFO - [APP] Report generation initiated
```

---

### 2️⃣ AGENT EXECUTION LOGS `[AGENT]`
Each agent logs its complete workflow:

#### **GeneralInfoAgent**
- Agent start with metadata (company name, website, question count)
- Tavily search queries for company fundamentals
- LLM analysis call/response with field names
- Database save operations
- Agent completion status

**Example:**
```
2024-04-28 10:30:45 - research_1 - INFO - Agent 'GeneralInfoAgent' starting research: {...}
2024-04-28 10:30:46 - research_1 - INFO - [TAVILY] Agent 'GeneralInfoAgent' - Company Fundamentals - Query: 'Company X founding history'
2024-04-28 10:30:52 - research_1 - INFO - [TAVILY] Agent 'GeneralInfoAgent' - Company Fundamentals - Found 47 results
2024-04-28 10:30:52 - research_1 - INFO - [LLM] Agent 'GeneralInfoAgent' - Section 'Company Fundamentals' - Sending prompt (2341 chars) to Gemini
2024-04-28 10:30:57 - research_1 - INFO - [LLM] Agent 'GeneralInfoAgent' - Section 'Company Fundamentals' - Received analysis (1823 chars) with fields: company_description, founded_year, company_size, headquarters, website_url, linkedin_profile
2024-04-28 10:30:57 - research_1 - INFO - [DATABASE] Saved 1 record(s) to 'general_info_results': {'company': 'Company X'}
2024-04-28 10:30:57 - research_1 - INFO - Agent 'GeneralInfoAgent' completed with status: success
```

#### **FinancialAgent**
- Financial data search queries
- Revenue, funding, profitability analysis
- LLM analysis with financial field extraction
- Database persistence

#### **IndustrialMediaAgent**
- Industry positioning search
- Competitor analysis queries
- Media coverage search
- LLM analysis with market intelligence
- Database save

#### **DecisionMakerAgent**
- Decision maker/executive search queries
- Contact information extraction
- Count of decision makers found
- Database storage

---

### 3️⃣ TAVILY SEARCH LOGS `[TAVILY]`
**Every search query captured with full details:**

```
[TAVILY] Agent 'FinancialAgent' - Revenue Search - Query: 'Company X revenue 2024 earnings'
[TAVILY] Agent 'FinancialAgent' - Revenue Search - Found 42 results
  [1] Company X Q3 2024 Earnings Report | www.investor.company-x.com/earnings
  [2] Company X Revenue Surges 45% YoY | www.techcrunch.com/articles/...
  [3] Financial Analysis: Company X | www.bloomberg.com/news/...
```

**Captured for each search:**
- ✅ Agent name
- ✅ Search type/category
- ✅ Exact search query
- ✅ Number of results found
- ✅ Top 3 results with title and URL
- ✅ Timestamp

---

### 4️⃣ LLM (GEMINI) LOGS `[LLM]`
**Each AI analysis step logged:**

```
[LLM] Agent 'GeneralInfoAgent' - Section 'Company Fundamentals' - Sending prompt (2341 chars) to Gemini
[LLM] Agent 'GeneralInfoAgent' - Section 'Company Fundamentals' - Received analysis (1823 chars) with fields: company_description, founded_year, company_size, headquarters, website_url, linkedin_profile
```

**Captured:**
- ✅ Agent performing analysis
- ✅ Analysis section/category
- ✅ Prompt size (chars sent to Gemini)
- ✅ Response size (chars received)
- ✅ Extracted fields/keys
- ✅ Timestamp

---

### 5️⃣ DATABASE LOGS `[DATABASE]`
**All data persistence operations:**

```
[DATABASE] Saved 1 record(s) to 'general_info_results': {'company': 'Company X'}
[DATABASE] Saved 18 record(s) to 'decision_makers': {'company': 'Company X'}
[DATABASE] Saved 1 record(s) to 'financial_results': {'company': 'Company X'}
```

**Captured:**
- ✅ Table name
- ✅ Record count saved
- ✅ Metadata (company name, record types)
- ✅ Timestamp

---

## 📝 Log Format

Each log line follows this structure:
```
TIMESTAMP - LOGGER_NAME - LEVEL - MESSAGE
```

**Example:**
```
2024-04-28 10:30:45 - research_1 - INFO - [TAVILY] Agent 'GeneralInfoAgent' - Company Fundamentals - Found 47 results
```

- **TIMESTAMP**: ISO format with milliseconds
- **LOGGER_NAME**: `research_1`, `research_2`, etc. (matches request ID)
- **LEVEL**: DEBUG, INFO, WARNING, ERROR
- **MESSAGE**: Formatted with `[TAG]` prefix for category

---

## 🗂️ Log Levels

| Level | What's Logged |
|-------|--------------|
| **DEBUG** | Individual search results, response snippets, analysis details |
| **INFO** | Agent lifecycle, search summaries, LLM calls, database operations |
| **WARNING** | Fallback operations, partial failures |
| **ERROR** | Exceptions, failed searches, API errors |

---

## 📂 Viewing Logs

### Streamlit Interface
After running research, view logs directly in the UI:
```bash
streamlit run streamlit_app/main.py
```

Logs displayed on research report page showing:
- Log file path
- Link to view full log
- Summary of operations

### Terminal
```bash
# View latest research logs
tail -f logs/research_1.log

# Search for specific agent
grep "GeneralInfoAgent" logs/research_1.log

# View all Tavily searches
grep "\[TAVILY\]" logs/research_1.log

# View all LLM operations
grep "\[LLM\]" logs/research_1.log

# Count operations by type
grep -c "\[TAVILY\]" logs/research_1.log
grep -c "\[LLM\]" logs/research_1.log
grep -c "\[DATABASE\]" logs/research_1.log
```

---

## 📊 Example Complete Log File

```
2024-04-28 10:30:45 - research_1 - INFO - [APP] Research started: TechStartup Inc
2024-04-28 10:30:45 - research_1 - INFO - Agent 'GeneralInfoAgent' starting research: {'company_name': 'TechStartup Inc', 'website': None, 'research_questions': 5}
2024-04-28 10:30:46 - research_1 - INFO - [TAVILY] Agent 'GeneralInfoAgent' - Company Fundamentals - Query: 'TechStartup Inc founding history'
2024-04-28 10:30:50 - research_1 - INFO - [TAVILY] Agent 'GeneralInfoAgent' - Company Fundamentals - Found 47 results
2024-04-28 10:30:50 - research_1 - DEBUG -   [1] TechStartup Inc - Wikipedia | www.wikipedia.org/wiki/TechStartup
2024-04-28 10:30:50 - research_1 - DEBUG -   [2] Founded in 2015 | www.techstartup.com/about
2024-04-28 10:30:50 - research_1 - DEBUG -   [3] TechStartup Inc Company Profile | www.crunchbase.com/organization/...
2024-04-28 10:30:52 - research_1 - INFO - [LLM] Agent 'GeneralInfoAgent' - Section 'Company Fundamentals' - Sending prompt (2341 chars) to Gemini
2024-04-28 10:30:57 - research_1 - INFO - [LLM] Agent 'GeneralInfoAgent' - Section 'Company Fundamentals' - Received analysis (1823 chars) with fields: company_description, founded_year, company_size, headquarters, website_url, linkedin_profile
2024-04-28 10:30:57 - research_1 - INFO - [DATABASE] Saved 1 record(s) to 'general_info_results': {'company': 'TechStartup Inc'}
2024-04-28 10:30:57 - research_1 - INFO - Agent 'GeneralInfoAgent' completed with status: success

2024-04-28 10:31:00 - research_1 - INFO - Agent 'FinancialAgent' starting research: {'company_name': 'TechStartup Inc', 'research_questions': 5}
2024-04-28 10:31:01 - research_1 - INFO - [TAVILY] Agent 'FinancialAgent' - Revenue Search - Query: 'TechStartup Inc revenue 2024'
2024-04-28 10:31:04 - research_1 - INFO - [TAVILY] Agent 'FinancialAgent' - Revenue Search - Found 28 results
2024-04-28 10:31:04 - research_1 - DEBUG -   [1] TechStartup Inc Q3 2024 Revenue | investor.techstartup.com/earnings
2024-04-28 10:31:04 - research_1 - DEBUG -   [2] Startup Funding News | www.crunchbase.com/funding/techstartup
2024-04-28 10:31:04 - research_1 - DEBUG -   [3] Series B Funding Announcement | techcrunch.com/2024/...
2024-04-28 10:31:06 - research_1 - INFO - [LLM] Agent 'FinancialAgent' - Section 'Financial Metrics' - Sending prompt (3120 chars) to Gemini
2024-04-28 10:31:12 - research_1 - INFO - [LLM] Agent 'FinancialAgent' - Section 'Financial Metrics' - Received analysis (2145 chars) with fields: revenue, funding_rounds, total_funding, profitability, financial_health, key_metrics
2024-04-28 10:31:12 - research_1 - INFO - [DATABASE] Saved 1 record(s) to 'financial_results': {'company': 'TechStartup Inc'}
2024-04-28 10:31:12 - research_1 - INFO - Agent 'FinancialAgent' completed with status: success

... [Industrial and Decision Maker agents follow same pattern] ...

2024-04-28 10:33:45 - research_1 - INFO - [APP] Report generation completed
2024-04-28 10:33:50 - research_1 - INFO - Research complete: {'status': 'success', 'total_agents': 4, 'total_searches': 28, 'records_saved': 45}
```

---

## 🎯 Key Takeaways

✅ **Every search query is logged** - See exactly what Tavily searched for  
✅ **All Gemini API calls logged** - Track LLM analysis with prompt/response sizes  
✅ **Complete database operations tracked** - Know what was saved when  
✅ **Per-request isolation** - Each research request has its own log file  
✅ **Debug-friendly format** - Search logs by `[TAG]` for quick filtering  
✅ **Full traceability** - Follow entire workflow from search → analysis → storage  

---

## 🚀 Getting Started

Run a research request and check the logs:
```bash
# Terminal 1: Start Streamlit
streamlit run streamlit_app/main.py

# Terminal 2: Monitor logs
tail -f logs/research_1.log

# Terminal 3: Search logs for specific operations
watch "grep -c '\[TAVILY\]' logs/research_1.log"
```

All Tavily outputs, LLM operations, and system events will be recorded! 📝
