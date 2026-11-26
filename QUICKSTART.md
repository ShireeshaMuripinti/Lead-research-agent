# QUICK START GUIDE - Lead Research Agent

## 🚀 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example configuration
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

**Required:**
- `TAVILY_API_KEY` - Get from https://tavily.com

**Recommended:**
- `GEMINI_API_KEY` - Get from https://ai.google.dev/

### 3. Verify Setup
```bash
python test_setup.py
```

You should see:
```
✅ All tests passed! Ready to run the application.
```

### 4. Run the App
```bash
streamlit run streamlit_app/main.py
```

Open your browser to: **http://localhost:8501**

---

## 💡 First Steps

### Try This Search:
1. Go to "Start New Research" tab
2. Enter company name: `Apple Inc.`
3. Leave others empty (optional)
4. Click "🚀 Start Research"
5. Wait for agents to complete (~2-3 minutes)
6. View the generated report

### Ask Questions:
1. Go to "Chat with Report" tab
2. Select the report you just created
3. Ask: "What is their revenue?"
4. Get AI-powered answers based on research

---

## 📁 Project Structure

```
LRA/
├── .env                    ← EDIT THIS with your API keys
├── requirements.txt        ← Install dependencies
├── test_setup.py          ← Verify configuration
├── run.sh                 ← Easy start script
│
├── config/                ← Settings & configuration
├── database/              ← SQLite database
├── agents/                ← Research agents (4 nodes)
├── utils/                 ← Helper functions
├── streamlit_app/         ← Web interface
│   ├── main.py           ← Main app
│   └── pages/            ← Pages (research, chat)
│
└── README.md              ← Full documentation
```

---

## 🔑 Getting API Keys

### Tavily (Required)
1. Visit https://tavily.com
2. Sign up (free account available)
3. Get API key from dashboard
4. Add to `.env`: `TAVILY_API_KEY=xxxxx`

### Google Gemini (Recommended)
1. Visit https://ai.google.dev/
2. Click "Get API Key"
3. Create new API key
4. Add to `.env`: `GEMINI_API_KEY=xxxxx`

### Google Cloud (Already Have)
- Your `service-account-key.json` is already provided
- Extract Project ID from the JSON file
- Add to `.env`: `GOOGLE_PROJECT_ID=xxxxx`

---

## ⚠️ Common Issues

### "TAVILY_API_KEY not provided"
**Solution:** Add your key to `.env` file

### "Module not found"
**Solution:** Run `pip install -r requirements.txt`

### Port 8501 in use
**Solution:** Use different port:
```bash
streamlit run streamlit_app/main.py --server.port 8502
```

### Database errors
**Solution:** Delete and recreate database:
```bash
rm database/lra_research.db
# Run app again - it will recreate the database
```

---

## 🎯 What Happens When You Research

1. **Request Created** → Stored in database
2. **4 Agents Run in Parallel:**
   - General Info Agent: Company basics
   - Financial Agent: Revenue, funding
   - Industrial Agent: Market position, competitors
   - Decision Maker Agent: Contacts, executives
3. **Gemini Analysis** → AI processes all findings
4. **Report Generated** → Formatted with recommendations
5. **Report Stored** → Saved in database forever
6. **Chat Ready** → Ask questions about report

---

## 📊 Database

**Local SQLite** in `database/lra_research.db`

Stores:
- ✅ All research requests
- ✅ Findings from each agent
- ✅ Final reports
- ✅ Chat history
- ✅ Search cache

**No external database needed!**

---

## 🚀 Next Steps

1. ✅ Setup complete
2. 🔍 Try first company research
3. 💬 Chat with the report
4. 📊 View research history
5. 🎓 Document for your project
6. 🚀 Deploy to cloud (optional)

---

## 📞 Need Help?

1. Check `README.md` for full documentation
2. Run `test_setup.py` to diagnose issues
3. Check `.env` configuration
4. View logs in terminal output
5. Check database: `sqlite3 database/lra_research.db`

---

## 🎓 For Your Project Documentation

Include:
- ✅ Architecture diagram (4 agents → curator → editor)
- ✅ API integrations (Tavily, Gemini, Google Cloud)
- ✅ Database schema
- ✅ Sample reports and chat interactions
- ✅ Performance metrics
- ✅ Future enhancements

---

**Ready to research? Run: `streamlit run streamlit_app/main.py` 🚀**
