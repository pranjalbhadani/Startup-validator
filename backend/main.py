"""
FastAPI Backend Server
Exposes the /validate endpoint that runs the multi-agent pipeline.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import StartupInput
from pipeline import run_pipeline

# Initialize the FastAPI application
app = FastAPI(
    title="Venture Validator",
    description="Multi-Agent Pipeline for Venture Idea Validation",
    version="1.0.0",
)

# Allow CORS so the Streamlit frontend can communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "running", "message": "Venture Validator API is live."}


@app.post("/validate")
def validate(data: StartupInput):
    """
    Main validation endpoint.
    Accepts a StartupInput and runs it through the Idea → Competitor pipeline.
    Returns a structured validation report.
    """

    result = run_pipeline(
        idea_description=data.idea_description,
        startup_name=data.startup_name,
        target_market=data.target_market,
        revenue_model=data.revenue_model or "",
    )

    return result
