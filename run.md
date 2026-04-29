# 🚀 Running the Venture Validator

This project is split into a **FastAPI Backend** and a **React Frontend**. Follow these steps to get everything running locally.

---

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 18+** & **npm**
- **API Keys**: You will need a Google Gemini API key.

---

## 🛠️ Step 1: Installation

### 1. Backend Setup
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Frontend Setup
```powershell
cd frontend
npm install
```

---

## 🔑 Step 2: Environment Variables

1. Navigate to the `backend/` folder.
2. Rename `.env.example` to `.env`.
3. Open `.env` and add your `GEMINI_API_KEY`:
   ```text
   GEMINI_API_KEY=your_key_here
   ```

---

## 🏃 Step 3: Starting the Servers

You need to run the Backend and Frontend simultaneously.

### 1. Start FastAPI Backend (Terminal 1)
The backend must be running for the UI to fetch data.
```powershell
cd backend
# Activate venv if not already active
uvicorn main:app --reload
```
*Backend will be available at: `http://127.0.0.1:8000`*

### 2. Start React Frontend (Terminal 2)
```powershell
cd frontend
npm run dev
```
*Frontend will be available at: `http://localhost:5173`*

---

## 🧪 Testing the Pipeline
If you want to test the multi-agent logic without the UI, you can run:
```powershell
cd backend
python -c "from langgraph_pipeline import run_pipeline; run_pipeline('An AI tool for automated video summarization')"
```

---

## 📁 Project Structure
- `backend/`: FastAPI server, multi-agent logic, and scoring systems.
- `frontend/`: React + Vite + Tailwind CSS dashboard.
- `data/`: Datasets used for market and competitor analysis.
- `docs/`: Guides and project documentation.
