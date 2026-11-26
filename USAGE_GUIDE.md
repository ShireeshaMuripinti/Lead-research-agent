# Usage Guide - Lead Research Agent

## 📖 Complete Usage Walkthrough

### Table of Contents
1. [Getting Started](#getting-started)
2. [Performing Research](#performing-research)
3. [Understanding Reports](#understanding-reports)
4. [Chatting with Reports](#chatting-with-reports)
5. [Advanced Features](#advanced-features)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation Recap
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Verify setup
python test_setup.py

# 4. Run application
streamlit run streamlit_app/main.py
```

### Browser Access
Open: **http://localhost:8501**

---

## Performing Research

### Step 1: Start New Research

1. **Click "Start New Research" tab** in the web interface
2. **Enter Company Name** (Required)
   - Examples: `Apple Inc.`, `Microsoft`, `Tesla`, `Netflix`
   - Be specific for better results
   - Minimum 2 characters, max 200 characters

### Step 2: Optional Details

Add information to narrow down research:

```
Website (Optional)
├─ Format: https://example.com or example.com
├─ Used to find company homepage
└─ Helps verify correct company

Location (Optional)
├─ Format: City, State or Country
├─ Examples: "San Francisco, CA", "London, UK"
└─ Useful for disambiguation

Industry (Optional)
├─ Format: Industry name
├─ Examples: "Technology", "Finance", "Healthcare"
└─ Focuses search on industry-specific information
```

### Step 3: Configure API Keys

**Expand "🔐 API Configuration" to add:**

```
Gemini API Key (Recommended)
├─ Enhances analysis with AI
├─ Generates better summaries
├─ Creates strategic recommendations
└─ Can be provided here or in .env

Tavily API Key (Optional Override)
├─ If different from .env
├─ Usually same for all requests
└─ Leave empty to use .env value
```

### Step 4: Start Research

Click **"🚀 Start Research"** button

**What Happens:**
1. Input validation checks
2. Research request created in database (Request ID: `#123`)
3. All 4 agents activate:
   - 🏢 **General Info Agent** (~30 seconds) - Company basics
   - 💰 **Financial Agent** (~30 seconds) - Revenue and funding
   - 📊 **Industrial Agent** (~30 seconds) - Market position
   - 👥 **Decision Maker Agent** (~20 seconds) - Contacts
4. Gemini analyzes all findings (~20 seconds)
5. Editor generates final report (~10 seconds)
6. **Total time:** 2-3 minutes

### Step 5: View Results

Once complete, see report with tabs:
- **Summary**: Executive summary & recommendations
- **General Info**: Company details, founded date, size
- **Financial**: Revenue, funding, profitability
- **Industry**: Market position, competitors, trends
- **Decision Makers**: Contacts with emails, phones

---

## Understanding Reports

### Report Structure

#### 📋 Summary Tab
```
Executive Summary
├─ Overview of company
├─ Business model
├─ Key strengths
└─ Strategic position

Recommendations
├─ 5-7 actionable insights
├─ Business opportunities
├─ Engagement strategies
└─ Risk considerations
```

#### 🏢 General Information Tab
```
Company Details
├─ Company Size (e.g., "1,001-5,000 employees")
├─ Founded Year (e.g., 1998)
├─ Headquarters (e.g., "Cupertino, CA")
├─ Website (clickable link)
└─ LinkedIn Profile (if available)

Description
└─ Comprehensive company overview
```

#### 💰 Financial Tab
```
Metrics (Top Row)
├─ Revenue (most recent year)
├─ Total Funding (if startup)
└─ Profitability Status

Details
├─ Funding Rounds (for startups)
├─ Financial Health Assessment
└─ Key Metrics (specific to industry)
```

#### 📊 Industry Tab
```
Market Analysis
├─ Industry Vertical (e.g., "Enterprise Software")
├─ Market Position (e.g., "Market Leader")
├─ Competitors (list of 5-10)
├─ Market Trends (relevant to company)
├─ Recent Media Coverage (5 latest articles)
└─ Press Releases (if available)
```

#### 👥 Decision Makers Tab
```
Each Contact Card Shows:
├─ Name
├─ Title/Position
├─ Email (if available)
├─ Phone (if available)
├─ LinkedIn Profile (clickable)
└─ Department (if known)
```

### Example Report Interpretation

**For Apple Inc.:**

```
General Info:
- Founded: 1976
- Size: 164,000+ employees
- HQ: Cupertino, California

Financial:
- Revenue: $394.3 Billion (2023)
- Profitability: Highly Profitable
- Status: Mature, Stable

Industry:
- Position: Market Leader
- Main Competitors: Microsoft, Samsung, Google
- Trends: AI, Services Revenue, Wearables

Contacts:
- Tim Cook (CEO)
- Craig Federighi (SVP Software Engineering)
- etc.
```

---

## Chatting with Reports

### Accessing Chat Interface

1. **Navigate to "Chat with Report" tab**
2. **Select Report from Sidebar**
   - Dropdown shows all available reports
   - Format: `Company Name - YYYY-MM-DD`
   - Most recent first

3. **Report Summary Shown**
   - Expandable section with executive summary preview

### Asking Questions

**Click the chat input box** and type your question:

```
Examples of Good Questions:

"What is the company's current revenue?"
→ Gets exact revenue figure from report

"Who is the CEO and how can I contact them?"
→ Finds CEO info and email from contacts

"What are the main competitors?"
→ Lists competitors from industry analysis

"What is their financial health?"
→ Summarizes profitability and funding status

"What are investment opportunities?"
→ Extracts recommendations from report

"How is the company positioned in the market?"
→ Gives market position and competitive advantages

"What were the major funding rounds?"
→ Lists funding history for startups

"Are they profitable? What's their revenue?"
→ Comprehensive financial summary
```

### Chat Workflow

```
You ask:
"What is Tesla's main business?"
       ↓
Question sent to Gemini AI
       ↓
AI reads full research report
       ↓
AI extracts relevant information
       ↓
AI generates conversational response
       ↓
You see answer in chat box
       ↓
Response saved to database
```

### Chat History

**Access Previous Conversations:**

1. Click "📜 View Chat History" in sidebar
2. Expands to show all previous Q&A for this report
3. Can review past questions and answers
4. Automatically saved to database

### Example Chat Session

```
User: "What is their revenue?"
Assistant: Based on the research report, Apple's
revenue is $394.3 billion as of 2023. This represents
a 2.2% increase from the previous year. The company
generates revenue from multiple segments including
iPhone sales, Services, Mac, iPad, and Wearables...

User: "Which segment generates most revenue?"
Assistant: According to the report, iPhone sales
represent the largest revenue segment, accounting for
approximately 52% of total revenue...

User: "Who should I contact for partnerships?"
Assistant: Based on the decision makers identified
in the research, you could contact:
- Business Development team contact: contact@...
- Or directly reach out to executives listed...
```

---

## Advanced Features

### Viewing Previous Reports

1. Go to **"View Reports"** tab
2. See table of all research requests
3. Columns show:
   - Company name
   - Location
   - Status (✅ Completed, ⏳ In Progress, ❌ Failed)
   - Date created
   - Action button

4. Click **"View"** to display any previous report
5. All reports are persistent in database

### Report Status Tracking

```
Status Meanings:

✅ Completed
└─ Report generation successful, fully viewable

⏳ In Progress
├─ Currently being researched
├─ Refresh page to see updates
└─ Wait for completion notification

❌ Failed
├─ Error during research
├─ Check error message
└─ Try researching again
```

### Data Persistence

All data stored locally in SQLite:
- ✅ Every research request
- ✅ All agent findings
- ✅ Final reports
- ✅ Chat conversations
- ✅ Search cache

**Access database directly:**
```bash
sqlite3 database/lra_research.db
sqlite> SELECT * FROM research_reports;
```

### Caching & Re-searches

Same company researched twice:
- Cache checked first
- If recent (< 7 days), cached results used
- Saves API costs and time
- Can be disabled by searching with new parameters

---

## Troubleshooting

### Research Not Starting

**Problem:** Button click does no do anything

**Solutions:**
1. Check browser console for errors
2. Verify .env file exists with API keys
3. Run `python test_setup.py`
4. Check terminal output for error messages

### API Key Errors

**"TAVILY_API_KEY not provided"**
- Add to .env file: `TAVILY_API_KEY=xxxxx`
- Restart app: `Ctrl+C`, then rerun

**"Gemini API key invalid"**
- Check key in .env or config
- Verify key from https://ai.google.dev/
- Generate new key if needed

### Research Fails Halfway

**Problem:** Some agents fail, partial results shown

**This is OK!** The system shows partial results.

**Reasons:**
- API temporarily unavailable
- Search returned no results for that query
- Timeout during processing

**Solution:** Try researching again

### Chat Not Responding

**Problem:** Questions get no response

**Solutions:**
1. Ensure Gemini API key configured
2. Key can be added in "🔐 Provide Gemini API Key" section
3. Check that report is selected
4. Verify internet connection

### Database Errors

**Problem:** "Database locked" or connection errors

**Solutions:**
```bash
# Close app (Ctrl+C)

# Clear corrupted database
rm database/lra_research.db

# Restart app (will recreate DB)
streamlit run streamlit_app/main.py
```

### Port Already in Use

**Problem:** Port 8501 occupied by another process

**Solution:**
```bash
# Use different port
streamlit run streamlit_app/main.py --server.port 8502

# Or kill process using 8501
lsof -i :8501
kill -9 <PID>
```

### Slow Performance

**Problem:** Searches taking > 5 minutes

**Reasons:**
- Tavily API slow response
- Internet connection issues
- System resources low

**Solutions:**
- Reduce MAX_TAVILY_RESULTS in .env
- Increase RESEARCH_TIMEOUT in .env
- Try with simpler company names

---

## Performance Tips

### For Faster Research

1. **Use specific company names**
   - "Apple Inc." instead of "Apple"
   - "Microsoft Corporation" instead of "Microsoft"

2. **Add website URL**
   - Helps identify correct company
   - Speeds up searches

3. **Specify location**
   - Especially for common company names
   - Reduces false matches

4. **Reuse searches**
   - Same company uses cache
   - Subsequent searches are instant

### For Better Results

1. **Include industry** for context
2. **Use official company names** as they appear
3. **Check multiple sources** (review our sources list)
4. **Ask specific questions** in chat

---

## Data Export

### Export a Report

The report content is stored in database. To export:

```bash
# Open database
sqlite3 database/lra_research.db

# Export to CSV
.mode csv
.output report.csv
SELECT * FROM research_reports WHERE id = 1;

# Or JSON format
# Copy report_content field to text file
```

### Custom Reports

Create Python script to access data:

```python
from database.db import db

# Get report
report = db.get_research_report(report_id=1)

# Export to JSON
import json
with open("report.json", "w") as f:
    json.dump(report, f, indent=2)

# Export to CSV
import pandas as pd
decision_makers = db.get_decision_makers(request_id=1)
df = pd.DataFrame(decision_makers)
df.to_csv("decision_makers.csv")
```

---

## Best Practices

### For Accurate Research

1. ✅ Use official company names
2. ✅ Verify findings from multiple research runs
3. ✅ Check decision maker information separately
4. ✅ Cross-reference financial data

### For AI Analysis

1. ✅ Provide Gemini API key for best analysis
2. ✅ Ask clear, specific questions
3. ✅ Ask follow-up questions for clarification
4. ✅ Review all available information

### For Documentation

1. ✅ Export reports for archival
2. ✅ Take screenshots of key findings
3. ✅ Document any limitations
4. ✅ Note update dates for reports

---

**Happy Researching! 🔍**
