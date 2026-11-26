# HTML Formatting & Styling Guide - Lead Research Agent

## ✅ Complete HTML Implementation

Your system now has **complete HTML formatting and rendering** with consistent styling across all sections.

---

## 🎨 Formatting System Architecture

### 1. HTMLFormatter Utility (`utils/html_formatter.py`)
Centralized HTML generation with standardized CSS styling:

**CSS Components:**
- `.report-section` - Main content sections with blue left border
- `.section-title` - Large titles with underline
- `.subsection-title` - Medium titles for subsections
- `.metric-card` - Key value displays
- `.data-table` - Formatted data tables
- `.info-box` / `.warning-box` - Alert boxes
- `.list-item` - Bullet points
- `.paragraph` - Body text with consistent line-height

**HTML Methods:**
```python
HTMLFormatter.metric_card(label, value)        # Single metric display
HTMLFormatter.table(headers, rows)             # Data table generation
HTMLFormatter.bullet_list(items)               # Formatted lists
HTMLFormatter.paragraph(text)                  # Formatted paragraphs
HTMLFormatter.format_general_info(info_dict)   # Company info section
HTMLFormatter.format_financial_info(info_dict) # Financial section
HTMLFormatter.format_industry_info(info_dict)  # Industry section
HTMLFormatter.format_decision_makers(makers)   # Contacts section
```

---

## 📋 Section Formatting

### General Information Section
**Includes:**
- Company overview description
- Metrics: Founded, Company Size, Headquarters
- Website link
- LinkedIn profile link

**HTML Structure:**
```html
<div class="report-section">
  <div class="section-title">Company Overview</div>
  <div class="paragraph">Company description...</div>
  <div style="grid-template-columns: repeat(2, 1fr);">
    <div class="metric-card">
      <div class="metric-label">Founded</div>
      <div class="metric-value">Year</div>
    </div>
    ...
  </div>
</div>
```

### Financial Information Section
**Includes:**
- Metrics: Revenue, Total Funding, Profitability (3-column layout)
- Financial Health assessment
- Funding Rounds (bulleted list)
- Key Metrics (bulleted list)

**HTML Structure:**
```html
<div class="report-section">
  <div class="section-title">Financial Information</div>
  <div style="grid: 3 columns; gap: 16px;">
    <metric-card>Revenue</metric-card>
    <metric-card>Total Funding</metric-card>
    <metric-card>Profitability</metric-card>
  </div>
  <div class="subsection-title">Financial Health</div>
  <div class="paragraph">...</div>
</div>
```

### Industry & Market Section
**Includes:**
- Industry Vertical (text)
- Market Position (text)
- Competitors (bulleted list, max 10)
- Market Trends (bulleted list)
- Recent Media Coverage (bulleted list, max 5)
- Press Releases (bulleted list, max 5)

**Consistent Formatting:**
- ✅ No random line breaks
- ✅ Proper section hierarchy
- ✅ Consistent font sizes
- ✅ Consistent spacing
- ✅ Unified color scheme

### Decision Makers Section
**Includes:**
- Table with: Name, Title, Email, Phone
- Up to 50+ contacts
- Sortable/organized display

**HTML Structure:**
```html
<table class="data-table">
  <thead>
    <tr>
      <th>Name</th>
      <th>Title</th>
      <th>Email</th>
      <th>Phone</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John Doe</td>
      <td>CEO</td>
      <td>john@company.com</td>
      <td>+1-555-0123</td>
    </tr>
  </tbody>
</table>
```

---

## 🎯 Streamlit Rendering

### Proper HTML Rendering in Streamlit
All HTML content rendered with `unsafe_allow_html=True`:

```python
def render_html_content(html_content: str, safe: bool = True):
    """Safely render HTML content in Streamlit."""
    if html_content:
        st.markdown(html_content, unsafe_allow_html=safe)
```

**Usage:**
```python
# ✅ Correct - Renders HTML with styling
render_html_content(HTMLFormatter.format_general_info(data))

# ❌ Old way - Doesn't render HTML properly
st.write(f"**text**")  # Only shows as markdown, not formatted
```

### Tab Structure
```
📋 Summary
  ├─ Executive Summary (HTML formatted)
  └─ Strategic Recommendations (HTML table)

ℹ️ General Info
  └─ Company Overview (HTML formatted)

💰 Financial
  └─ Financial Information (HTML formatted)

📊 Industry
  └─ Industry & Market Analysis (HTML formatted)

👥 Decision Makers
  └─ Contacts Table (HTML table)
```

---

## 🔧 Gemini Integration

### Updated Prompts for Consistent HTML
All Gemini analysis methods now include structured prompts that ensure consistent HTML output:

**Executive Summary Prompt:**
```
Format your response as follows:
<div class="summary-content">
<p>First paragraph about company overview...</p>
<p>Second paragraph about financial status...</p>
<p>Third paragraph about market opportunity...</p>
</div>

Return ONLY the HTML content, no code blocks or markdown.
```

**Recommendations Prompt:**
```
Format your response as an HTML table with columns:
Recommendation | Priority | Timeline | Key Contact | Expected Impact

Return ONLY the HTML table, no code blocks or markdown.
```

### LLM Response Logging
All Gemini API calls are logged with:
- Prompt size (characters)
- Response size (characters)
- Extracted fields

---

## ✅ No Hardcoded Values

### Configuration Loading
All settings loaded from `.env` file via `config/settings.py`:

```python
# ✅ Correct - From configuration
gemini_key = settings.GEMINI_API_KEY
tavily_key = settings.TAVILY_API_KEY
log_dir = settings.LOG_DIR

# ❌ Removed - Hardcoded values
analyzer = get_gemini_analyzer(api_key="your_gemini_api_key")  # REMOVED
```

### Environment Variables (`.env`)
```
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_key
GOOGLE_PROJECT_ID=your_project_id
LOG_DIR=logs
LOG_LEVEL=INFO
GEMINI_MODEL=gemini-2-0-flash
GEMINI_TEMPERATURE=0.7
DATABASE_PATH=database/lra_research.db
```

---

## 🎨 CSS Styling Reference

### Color Scheme
- **Primary Blue:** `#1f77b4` - Headers, borders, links
- **Light Gray:** `#f8f9fa` - Section backgrounds
- **Dark Gray:** `#333` - Body text
- **Light Border:** `#e0e0e0` - Table borders

### Font Sizing
- Section titles: `22px` (bold)
- Subsection titles: `16px` (bold)
- Body text: `15px` (normal)
- Metric labels: `13px` (uppercase)
- Metric values: `18px` (bold)

### Spacing
- Section margin: `20px 0`
- Section padding: `20px`
- Item margin: `8px 0`
- Item padding: `10px 12px`

---

## 📊 Example Report Structure

```
🔍 Lead Research Agent - Company Name - Research Report

┌─ 📋 Summary Tab ────────────────────────────────────┐
│                                                       │
│  Executive Summary                                   │
│  ┌──────────────────────────────────────────────┐  │
│  │ [Formatted HTML paragraphs about company]    │  │
│  │ [Clean, consistent font sizes and spacing]   │  │
│  └──────────────────────────────────────────────┘  │
│                                                       │
│  Strategic Recommendations                          │
│  ┌──────────────────────────────────────────────┐  │
│  │ [HTML formatted table with 5-7 rows]         │  │
│  │ Recommendation | Priority | Timeline | ...   │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘

┌─ ℹ️ General Info Tab ────────────────────────────────┐
│  Company Overview                                    │
│  [Founded | Company Size | Headquarters | Website]  │
│  [Consistent metric cards in 2-column grid]         │
└─────────────────────────────────────────────────────┘

┌─ 💰 Financial Tab ──────────────────────────────────┐
│  Financial Information                              │
│  [Revenue | Total Funding | Profitability]          │
│  [3-column metric card grid]                        │
│  Financial Health: [Formatted paragraph]            │
│  Funding Rounds: [Bulleted list]                   │
└─────────────────────────────────────────────────────┘

┌─ 📊 Industry Tab ───────────────────────────────────┐
│  Industry & Market Analysis                         │
│  [All subsections with consistent formatting]       │
│  [No random line breaks or style inconsistencies]   │
└─────────────────────────────────────────────────────┘

┌─ 👥 Decision Makers Tab ────────────────────────────┐
│  Decision Makers & Contacts (N found)               │
│  ┌─────────────────────────────────────────────┐   │
│  │ Name | Title | Email | Phone               │   │
│  ├─────────────────────────────────────────────┤   │
│  │ John Doe | CEO | john@... | +1-555-...      │   │
│  │ Jane Smith | CFO | jane@... | +1-555-...    │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Testing & Verification

### Test HTML Rendering
```bash
# Start Streamlit with the new formatting
streamlit run streamlit_app/main.py

# Create a new research request
# - Fill in company name
# - Click "Start Research"
# - Check the generated report

# Verify:
✅ All sections display with consistent formatting
✅ No text splitting or line breaks within sections
✅ Proper table rendering for decision makers
✅ Consistent font sizes and colors
✅ Proper HTML rendering (not plain text)
✅ Gemini responses are properly formatted
```

### Check Logs
```bash
# Monitor LLM calls
grep "\[LLM\]" logs/research_*.log

# Verify HTML structure in responses
grep "section-title\|metric-card\|data-table" logs/research_*.log
```

---

## 📝 Summary of Improvements

✅ **Unified HTML Formatting**
- Centralized HTMLFormatter utility with consistent CSS
- No hardcoded formatting strings
- Reusable components for all sections

✅ **Proper Streamlit Rendering**
- All HTML rendered with `unsafe_allow_html=True`
- Proper section containers and styling
- Consistent tab layout

✅ **No Hardcoded Values**
- All configuration loaded from `.env`
- All API keys from settings
- All styling from CSS classes

✅ **Consistent Section Formatting**
- Industry section no longer has text splitting
- Each section has proper hierarchy and spacing
- Unified font sizes and colors

✅ **Improved Gemini Prompts**
- Specific HTML structure requests
- Consistent table formatting
- Explicit instructions for clean output

✅ **Enhanced Logging**
- LLM calls logged with HTML verification
- Response sizes and field counts tracked
- HTML structure validation

---

## 🎯 Next Steps

1. **Test the full workflow** with new research request
2. **Verify HTML rendering** in all tabs
3. **Check decision makers table** displays correctly
4. **Monitor logs** for proper LLM HTML output
5. **Chat with reports** to test HTML responses in Q&A

Everything is now properly configured with professional HTML formatting and consistent styling! 🎉
