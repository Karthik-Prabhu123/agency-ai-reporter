@"
# 📊 AI-Assisted Campaign Reporter (SaaS MVP)

![Application Interface Dashboard](app_screenshot.png)


A lightweight, automated web application built for digital marketing agencies to eliminate manual spreadsheet work. This tool securely ingests raw ad platform exports (Meta Ads & Google Ads), automatically processes and blends performance metrics, and leverages high-performance LLMs via Groq to draft client-ready weekly performance briefs—exportable instantly as corporate-styled PDFs.

## 🚀 Core Features
- **Cross-Channel Data Ingestion:** Drag-and-drop standard CSV/XLSX analytics exports from Meta Ads Manager and Google Ads.
- **Automated Performance Aggregation:** Instantly maps inconsistent column naming conventions to compute Blended Spend, Conversion counts, and True Platform ROAS.
- **AI-Generated Draft Briefs:** Generates smart, professional executive summaries and clear optimization action lists via Groq Cloud infrastructure.
- **Interactive Review Workspace:** An editable text interface that keeps account managers "in-the-loop" to refine summaries before sending.
- **Corporate PDF Exporting:** Compiles raw textual analytics briefs into clean, executive-styled PDF report files using automated typographical flow structures.

## 🛠️ The Tech Stack
- **Frontend Framework:** Streamlit (Python-driven interactive interface engine)
- **Data Engineering:** Pandas (High-speed matrix array cleanup and scalar parsing)
- **AI Engine SDK:** Groq API Cloud Client Client Environment 
- **Document Compiling:** ReportLab (Granular document layout structure compiler)

## 💻 Local Installation & Setup

1. **Clone the project repository folder:**
   ```bash
   git clone https://github.com
   cd agency-ai-reporter
   ```

2. **Install all required package dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Fire up the local Streamlit development server instance:**
   ```bash
   python -m streamlit run app.py
   ```
"@ | Out-File -Encoding ascii README.md
