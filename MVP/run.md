````markdown
# Startup Validator MVP – Setup & Run Guide

## 1. Clone or Create the Project Folder

Create a new directory and move into it.

```bash
mkdir startup-validator
cd startup-validator
````

Project structure:

```
startup-validator/
│
├── main.py
├── models.py
├── llm_service.py
├── scoring.py
├── app.py
├── requirements.txt
└── .env
```

---

# 2. Create Virtual Environment

Create a Python virtual environment.

```bash
python -m venv venv
```

Activate it.

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

# 3. Install Dependencies

Install required libraries.

```bash
pip install -r requirements.txt
```

Example `requirements.txt`

```
fastapi
uvicorn
streamlit
pydantic
python-dotenv
google-generativeai
requests
```

---

# 4. Add Gemini API Key

Create a `.env` file.

```
GEMINI_API_KEY=your_api_key_here
```

Get API key from:

```
https://aistudio.google.com/app/apikey
```

---

# 5. Start Backend Server

Run the FastAPI backend.

```bash
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

This allows testing the API directly.

---

# 6. Run the Frontend

Open another terminal in the same project folder and run:

```bash
streamlit run app.py
```

Frontend will start at:

```
http://localhost:8501
```

---

# 7. Use the Application

1. Open the Streamlit UI.
2. Enter the following fields:

* Startup Name
* Idea Description
* Target Market
* Revenue Model

3. Click **Validate**

The system will return:

* Market Score
* Competition Score
* Feasibility Score
* Overall Validation Score
* Risk Level
* SWOT Analysis
* Recommendations

---

# 8. System Workflow

```
User Input (Streamlit UI)
        ↓
FastAPI Backend
        ↓
Gemini API Analysis
        ↓
Scoring Engine
        ↓
Structured Validation Output
```

---

# 9. Stopping the Project

Stop running servers using:

```
CTRL + C
```

in the terminal.

---

# 10. Quick Demo Checklist (for Viva)

Before presenting:

* Backend running (`uvicorn main:app`)
* Frontend running (`streamlit run app.py`)
* API working in `/docs`
* Test idea ready for demo

```
```
