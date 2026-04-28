# Startup Validator MVP – Setup & Run Guide

## Project Structure

```
startup-validator/
│
├── MVP/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── idea_agent.py        # Agent 1: Idea Understanding
│   │   ├── market_agent.py      # Agent 2: Market Potential
│   │   ├── competitor_agent.py  # Agent 3: Competitor Similarity
│   │   └── risk_agent.py        # Agent 4: Feasibility & Risk
│   │
│   ├── pipeline.py              # Pipeline Controller
│   ├── main.py                  # FastAPI Backend
│   ├── scoring.py               # Scoring Engine
│   ├── models.py                # Pydantic Models
│   ├── llm_service.py           # Shared LLM Utility
│   ├── app.py                   # Streamlit Frontend
│   ├── requirements.txt         # Python Dependencies
│   └── .env                     # API Keys (not committed)
│
└── data/
    └── datasets/
        └── investments_VC_dataset.csv  # Competitor database CSV
```

---

## 1. Navigate to the MVP Folder

```bash
cd MVP
```

All commands below must be run from inside the `MVP/` folder.

---

## 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Add Gemini API Key

Create a `.env` file inside the `MVP/` folder:

```
GEMINI_API_KEY=your_api_key_here
```

Get API key from: https://aistudio.google.com/app/apikey

---

## 5. Load Competitor Database (One-Time Setup)

Before using the competitor agent, load your CSV dataset into the vector database:

```bash
python agents/competitor_agent.py
```

This reads `data/datasets/investments_VC_dataset.csv` and populates a local ChromaDB vector store.
You only need to do this **once**.

---

## 6. Start the Backend Server

Open a terminal in the `MVP/` folder and run:

```bash
cd MVP
uvicorn main:app --reload
```

Backend will start at:

```
http://127.0.0.1:8000
```

Open API documentation:

```
http://127.0.0.1:8000/docs
```

---

## 7. Start the Frontend

Open **another terminal** in the `MVP/` folder and run:

```bash
cd MVP
streamlit run app.py
```

Frontend will start at:

```
http://localhost:8501
```

---

## 8. Use the Application

1. Open the Streamlit UI at `http://localhost:8501`
2. Enter the following fields:
   - **Startup Name** (e.g., EduAI)
   - **Idea Description** (detailed description of the idea)
   - **Target Market** (e.g., Indian universities)
   - **Revenue Model** (e.g., B2B SaaS subscription)
3. Click **Validate Startup Idea**
4. Wait 15-30 seconds for the multi-agent pipeline to complete.

The system will return:

- Market Score (0-10)
- Competition Score (0-10)
- Feasibility Score (0-10)
- Overall Validation Score
- Risk Level (Low / Medium / High)
- Detected Industry & Keywords
- List of Similar Competitors

---

## 9. System Workflow (Multi-Agent Pipeline)

```
User Input (Streamlit UI)
        ↓
[Agent 1] Idea Understanding Agent
        ↓
[Agent 2] Market Potential Agent
        ↓
[Agent 3] Competitor Similarity Agent
        ↓
[Agent 4] Feasibility & Risk Agent
        ↓
Scoring Engine
        ↓
Structured Validation Report (returned to UI)
```

---

## 10. Stopping the Project

Stop running servers using:

```
CTRL + C
```

in the terminal.

---

## 11. Quick Demo Checklist (for Viva)

Before presenting:

- [ ] `.env` file has a valid Gemini API key
- [ ] Competitor database is loaded (Step 5)
- [ ] Backend running (`uvicorn main:app --reload`)
- [ ] Frontend running (`streamlit run app.py`)
- [ ] API working at `http://127.0.0.1:8000/docs`
- [ ] Test idea ready for demo
