# 🚀 Running the Venture Validator

This project is split into a **FastAPI Backend** (with a LangGraph multi-agent pipeline) and a **React Frontend**. It also includes an alternative **Streamlit Frontend**. Follow these steps to get everything running locally on **Windows**.

---

## 📋 Prerequisites

- **Python 3.9+** (with `pip`)
- **Node.js 18+** & **npm**
- **API Key**: You need a [Google Gemini API key](https://aistudio.google.com/app/apikey)

---

## 🛠️ Step 1: Clone & Install

### 1. Backend Setup

Open a **PowerShell** terminal in the project root:

```powershell
# Create a virtual environment (skip if venv/ already exists)
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate

# Install all Python dependencies
pip install -r backend\requirements.txt
```

### 2. Frontend Setup (React)

Open a **second PowerShell** terminal:

```powershell
cd frontend
npm install
```

> **Note:** The first `npm install` will take a few minutes as it downloads all React, Tailwind, MUI, and Radix UI packages.

---

## 🔑 Step 2: Environment Variables

1. Navigate to the `backend/` folder.
2. Copy `.env.example` to `.env`:
   ```powershell
   copy backend\.env.example backend\.env
   ```
3. Open `backend/.env` and replace the placeholder with your real API key:
   ```text
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   VITE_API_URL=http://localhost:8000
   ```

---

## 📦 Step 3: Prepare the Dataset (One-Time)

The Competitor Agent uses a **ChromaDB vector database** built from a cleaned CSV. You must load this data before the first run.

### Option A — Pre-cleaned CSV exists

If `data/processed/cleaned_investments_sent.csv` already exists (check the file), you can skip cleaning and go straight to loading:

```powershell
# Activate venv if not already active
.\venv\Scripts\activate

cd backend
python -c "from agents.competitor_agent import load_csv_to_database; load_csv_to_database()"
```

This will embed ~15,000+ startups into ChromaDB (stored in `data/startup_vectordb/`). It takes **2–5 minutes** on the first run.

### Option B — Build from raw data

If you only have the raw Kaggle CSV (`data/raw/kaggle/investments_VC_dataset.csv`):

```powershell
.\venv\Scripts\activate

# Step 1: Clean the raw CSV
python utilities\data_cleaning.py

# Step 2: Load into ChromaDB
cd backend
python -c "from agents.competitor_agent import load_csv_to_database; load_csv_to_database()"
```

> **Note:** The `data_cleaning.py` script expects the raw CSV at `data/raw/kaggle/investments_VC_dataset.csv` and outputs to `data/processed/`. You may need to adjust the paths inside the script if your file locations differ. See the [Troubleshooting](#-troubleshooting) section below.

---

## 🏃 Step 4: Start the Servers

You need **two terminals** open simultaneously.

### Terminal 1 — FastAPI Backend

```powershell
.\venv\Scripts\activate
cd backend
uvicorn main:app --reload
```

✅ Backend available at: **http://127.0.0.1:8000**  
✅ API docs at: **http://127.0.0.1:8000/docs**

### Terminal 2 — React Frontend

```powershell
cd frontend
npm run dev
```

✅ Frontend available at: **http://localhost:5173**

### Alternative: Streamlit Frontend

If you prefer the Streamlit UI instead of React:

```powershell
.\venv\Scripts\activate
cd backend
streamlit run app.py
```

✅ Streamlit UI available at: **http://localhost:8501**

> **Important:** The FastAPI backend (Terminal 1) must be running regardless of which frontend you use.

---

## 🧪 Step 5: Testing

### Quick Pipeline Test (No UI)

```powershell
.\venv\Scripts\activate
cd backend
python -c "from langgraph_pipeline import run_pipeline; print(run_pipeline('An AI tool for automated video summarization'))"
```

### API Test via curl

```powershell
curl -X POST http://127.0.0.1:8000/validate `
  -H "Content-Type: application/json" `
  -d '{"startup_name":"TestStartup","idea_description":"An AI tool for video summarization","target_market":"Students","revenue_model":"Subscription"}'
```

### Run Unit Tests

```powershell
.\venv\Scripts\activate
cd backend
python -m pytest ..\tests\ -v
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'google.genai'` | Run `pip install google-genai` (not `google-generativeai`) |
| `[Competitor Agent] ERROR: CSV not found` | Ensure `data/processed/cleaned_investments_sent.csv` exists. Run data cleaning first (Step 3). |
| `[Agent 2] WARNING: Database is empty!` | Run the ChromaDB loading command from Step 3. |
| Frontend shows "Cannot connect to backend" | Make sure the FastAPI server is running on port 8000. |
| `npm install` fails | Ensure Node.js 18+ is installed. Delete `node_modules/` and `package-lock.json`, then retry. |
| `GEMINI_API_KEY` errors | Check that `backend/.env` exists and contains a valid key. |

---

## 📁 Project Structure

```
Startup-validator/
├── backend/               # FastAPI server + multi-agent pipeline
│   ├── agents/            # Agent implementations (Idea, Competitor, Scoring)
│   ├── graph/             # LangGraph state, nodes, and graph builder
│   ├── main.py            # FastAPI entry point
│   ├── app.py             # Streamlit frontend (alternative UI)
│   ├── langgraph_pipeline.py  # LangGraph pipeline controller
│   ├── pipeline.py        # Legacy 3-stage pipeline (direct)
│   ├── models.py          # Pydantic request/response models
│   ├── llm_service.py     # Gemini API wrapper
│   ├── scoring.py         # Scoring engine integration
│   └── requirements.txt   # Python dependencies
├── frontend/              # React + Vite + Tailwind CSS dashboard
│   ├── src/app/           # App pages, routes, API service
│   ├── src/styles/        # Global styles
│   └── package.json       # Node dependencies
├── data/                  # Datasets for analysis
│   ├── raw/kaggle/        # Original Kaggle VC dataset
│   ├── interim/           # Intermediate cleaned data
│   └── processed/         # Final cleaned CSV for ChromaDB
├── utilities/             # Data cleaning scripts, setup helpers
├── prompts/               # LLM prompt templates and design docs
├── tests/                 # Unit and integration tests
├── Screenshots/           # UI screenshots
└── docs/                  # Guides and documentation
```
