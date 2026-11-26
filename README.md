# Lead Research Agent

A sophisticated AI-powered research platform that gathers comprehensive information about companies using agentic AI, Tavily search, and Google Gemini.

## 🚀 Features

- **Multi-Node Research Architecture**: 4 specialized research agents
  - **General Info Node**: Company overview, history, size, headquarters
  - **Financial Node**: Revenue, funding, profitability, financial metrics
  - **Industrial & Media Node**: Market position, competitors, media coverage
  - **Decision Makers Node**: Key contacts, executives, business leads

- **AI-Powered Analysis**: Uses Google Gemini for intelligent analysis and report generation
- **Comprehensive Search**: Tavily API integration for online research
- **Local Database**: SQLite for storing requests and reports
- **Interactive Chat**: Ask questions about generated research reports
- **Beautiful UI**: Streamlit-based web interface

## 📋 Project Structure

```
LRA/
├── config/
│   └── settings.py                 # Configuration management
├── database/
│   ├── db.py                       # Database operations
│   ├── schema.sql                  # Database schema
│   └── lra_research.db             # SQLite database (created on first run)
├── agents/
│   ├── general_info_agent.py       # General information research
│   ├── financial_agent.py          # Financial information research
│   ├── industrial_agent.py         # Industry & media research
│   ├── decision_maker_agent.py     # Decision maker research
│   ├── curator_agent.py            # Orchestrates all agents
│   └── editor_agent.py             # Generates final reports
├── utils/
│   ├── tavily_search.py            # Tavily API integration
│   ├── gemini_integration.py       # Google Gemini integration
│   └── validators.py               # Input validation utilities
├── streamlit_app/
│   ├── main.py                     # Main Streamlit app
│   ├── pages/
│   │   ├── research_report.py      # Research & report display
│   │   └── chat_with_report.py     # Interactive Q&A about reports
│   └── components/
│       └── report_display.py       # Reusable UI components
├── service-account-key.json        # Google Cloud credentials (your file)
├── .env                            # Environment variables (create this)
├── .env.example                    # Example environment file
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Tavily API key (get from [tavily.com](https://tavily.com))
- Google Gemini API key (optional but recommended)
- Google service account JSON file (already provided)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment

1. **Copy the example env file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and fill in your API keys:**
   ```bash
   # Required
   TAVILY_API_KEY=your_tavily_api_key

   # Recommended for AI-powered analysis
   GEMINI_API_KEY=your_gemini_api_key

   # Already provided
   GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
   GOOGLE_PROJECT_ID=your_project_id
   ```

### Step 3: Verify Database Setup

The SQLite database will be created automatically on first run:
```bash
# Check database location
ls -la database/
```

## ▶️ Running the Application

### Start Streamlit App

```bash
streamlit run streamlit_app/main.py
```

The app will be available at: `http://localhost:8501`

### Alternative: Using a helper script

Create a file named `run.sh`:
```bash
#!/bin/bash
source venv/bin/activate  # if using virtual environment
streamlit run streamlit_app/main.py
```

Then run:
```bash
chmod +x run.sh
./run.sh
```

## 💻 Usage Guide

### 1. Start New Research

1. Click "Start New Research" tab
2. Enter company name (required)
3. Optionally provide:
   - Website URL
   - Location
   - Industry

4. Optionally configure:
   - Gemini API Key (for AI analysis)
   - Tavily API Key (if different from .env)

5. Click "🚀 Start Research"

The system will:
- Create a research request in the database
- Run all 4 research agents in parallel
- Analyze findings with Gemini
- Generate a comprehensive report
- Display the report in formatted tabs

### 2. View Reports

- Browse all previous research reports
- Click "View" to display any report
- Reports show:
  - Executive summary
  - General company information
  - Financial data
  - Market position & competitors
  - Decision makers & contacts
  - Strategic recommendations

### 3. Chat with Report

1. Select a report from the sidebar
2. Ask any question about the research
3. AI provides answers based on the report content
4. Chat history is saved to database

## 📊 Database Schema

### Key Tables

- **research_requests**: Main research requests
- **general_info_results**: Company general information
- **financial_results**: Financial data
- **industrial_media_results**: Industry & market analysis
- **decision_makers**: Key contacts and executives
- **research_reports**: Final comprehensive reports
- **chat_history**: Q&A conversation history
- **research_cache**: Search result caching

## 🔌 API Integration

### Tavily Search

- Online research and data gathering
- Up to 10 results per query (configurable)
- Search results caching for efficiency
- Used for all research nodes

### Google Gemini

- AI analysis of search results
- Report generation and summarization
- Answer questions about reports
- Configurable model and temperature settings

### Google Cloud

- Service account authentication
- Project configuration
- API credentials management

## 🛠️ Configuration Details

### Settings (config/settings.py)

All settings are loaded from environment variables with defaults:

```python
from config.settings import settings

settings.TAVILY_API_KEY        # Tavily API key
settings.GEMINI_MODEL          # Gemini model name
settings.DATABASE_PATH         # SQLite database location
settings.MAX_TAVILY_RESULTS    # Max search results per query
settings.RESEARCH_TIMEOUT      # Timeout in seconds
```

## 📝 Example Workflow

1. **Research "Tesla Inc."**
   - General Agent: Finds founding year, company size, headquarters
   - Financial Agent: Discovers revenue and market cap
   - Industrial Agent: Analyzes EV market position, competitors
   - Decision Maker Agent: Finds CEO, executives, contacts
   - Editor: Generates comprehensive report with recommendations

2. **Chat with Report**
   - Q: "What is Tesla's revenue?"
   - A: "Based on the research report, Tesla's revenue is..."

3. **View History**
   - All research and chats are stored in SQLite
   - Access previous reports anytime

## 🐛 Troubleshooting

### "TAVILY_API_KEY not provided"
- Ensure your `.env` file has `TAVILY_API_KEY=your_key`
- Check that `.env` is in the root project directory

### "Gemini not installed"
- Run: `pip install google-generativeai`
- Update requirements.txt if needed

### Database errors
- Check `database/` directory permissions
- Ensure SQLite3 is installed: `which sqlite3`
- Delete `database/lra_research.db` to reset (all data will be lost)

### Port 8501 already in use
```bash
streamlit run streamlit_app/main.py --server.port 8502
```

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web UI framework |
| google-generativeai | 0.3.0 | Gemini AI model |
| tavily-python | 0.2.1 | Online search API |
| sqlalchemy | 2.0.23 | Database ORM |
| python-dotenv | 1.0.0 | Environment variables |
| pandas | 2.1.1 | Data processing |
| requests | 2.31.0 | HTTP requests |

## 🔒 Security Notes

- Never commit `.env` file to version control
- Use `.env.example` for configuration template
- Keep API keys confidential
- Validate all user inputs
- Use HTTPS in production
- Store sensitive data securely

## 🚀 Deployment

### Local Deployment
Already running locally as described above.

### Cloud Deployment (Google Cloud Run)

```bash
# Create Dockerfile
# Deploy with Cloud Run
gcloud run deploy lead-research-agent \
  --source . \
  --platform managed \
  --region us-central1
```

### Docker Setup

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "streamlit_app/main.py"]
```

## 📞 Support & Contributions

For issues, questions, or contributions:
1. Check troubleshooting section
2. Review API documentation
3. Check logs in database
4. Contact project maintainer

## 📄 License

This project is for educational purposes. Ensure compliance with:
- Tavily API terms of service
- Google Cloud terms of service
- Data privacy regulations

## 🎓 Academic Usage

If using this for your final year project:
- Document all agent interactions
- Keep research logs and results
- Cite all external APIs and libraries
- Include database schema documentation
- Add evaluation metrics and results

## Version History

- **v1.0.0** (2026-04-27): Initial release with complete agentic AI architecture

---

**Made with ❤️ for Lead Research Agent Project**
