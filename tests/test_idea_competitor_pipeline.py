"""
Test Pipeline: Idea Agent -> Competitor Agent
=============================================
This script tests only two agents in isolation:
  1. Idea Agent       (utilities/idea_agent.py)  - extracts structured data from raw idea text
  2. Competitor Agent  (MVP/agents/competitor_agent.py) - finds similar startups in ChromaDB

Flow:
  Raw Idea Text  ->  Idea Agent  ->  Structured Data  ->  Competitor Agent  ->  Results

Usage:
  python test_idea_competitor_pipeline.py
"""

import sys
import os
import json
import time
from dotenv import load_dotenv

# --- Fix import paths so both modules are reachable ---
# Add project root so we can import from 'utilities/' and 'MVP/agents/'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "MVP"))

# Load the .env from the MVP directory (that's where the GEMINI_API_KEY lives)
load_dotenv(os.path.join(PROJECT_ROOT, "MVP", ".env"))

# Import the two agents we want to test
from utilities.idea_agent import extract_startup_details
from agents.competitor_agent import find_competitors


# --- Sample startup idea to test with ---
SAMPLE_IDEA = (
    "We are building QuickMed, an AI-powered telemedicine platform that uses "
    "natural language processing to triage patient symptoms before connecting "
    "them with the right specialist via video call. Our target market is "
    "working professionals in metro cities aged 25-45 who need fast, "
    "affordable healthcare without visiting a hospital. We plan to monetize "
    "through subscription plans and per-consultation fees."
)


def print_banner(title: str):
    """Print a formatted section banner for clear terminal output."""
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_json(data: dict, indent: int = 2):
    """Pretty-print a dictionary as formatted JSON."""
    print(json.dumps(data, indent=indent, ensure_ascii=False))


def run_test_pipeline():
    """
    Runs a two-stage test pipeline:
      Stage 1 - Idea Agent:       converts raw text -> structured startup data
      Stage 2 - Competitor Agent:  searches ChromaDB for similar startups
    """

    print_banner("TEST PIPELINE: Idea Agent -> Competitor Agent")
    print(f"\n[INPUT] Sample Idea Input:\n{SAMPLE_IDEA}\n")

    # -------------------------------------------------
    # STAGE 1: Idea Understanding Agent
    # -------------------------------------------------
    print_banner("Stage 1/2 - Idea Understanding Agent")
    print("Sending raw idea text to Gemini for structured extraction...\n")

    start = time.time()
    idea_data = extract_startup_details(user_idea_text=SAMPLE_IDEA)
    elapsed = round(time.time() - start, 2)

    # Validate the response
    if idea_data is None:
        print("[FAIL] Idea Agent returned None -- check your GEMINI_API_KEY in .env")
        print("Aborting pipeline.")
        return

    print(f"[OK] Idea Agent completed in {elapsed}s")
    print("\n[OUTPUT] Structured Output from Idea Agent:")
    print_json(idea_data)

    # -------------------------------------------------
    # STAGE 2: Competitor Similarity Agent
    # -------------------------------------------------
    print_banner("Stage 2/2 - Competitor Similarity Agent")
    print("Searching ChromaDB vector database for similar startups...\n")

    start = time.time()
    competitor_data = find_competitors(idea_data)
    elapsed = round(time.time() - start, 2)

    print(f"\n[OK] Competitor Agent completed in {elapsed}s")

    # -- Display competitor results --
    competitors = competitor_data.get("competitors", [])
    competition_score = competitor_data.get("competition_score", 0)

    if competitors:
        print(f"\n[RESULTS] Found {len(competitors)} similar startup(s):\n")
        for i, comp in enumerate(competitors, 1):
            print(f"  {i}. {comp['competitor_name']}")
            print(f"     Market:     {comp['market']}")
            print(f"     Status:     {comp['status']}")
            print(f"     Funding:    ${int(comp.get('funding', 0)):,}")
            print(f"     Similarity: {comp['similarity_distance']}")
            print()
    else:
        print("\n[WARNING] No competitors found -- the ChromaDB may be empty.")
        print(
            "   Run 'python MVP/agents/competitor_agent.py' to load the dataset first.\n"
        )

    # -- Final Summary --
    print_banner("PIPELINE SUMMARY")
    print(f"  Startup Name:      {idea_data.get('startup_name', 'N/A')}")
    print(f"  Industry:          {idea_data.get('industry', 'N/A')}")
    print(f"  Target Market:     {idea_data.get('target_market', 'N/A')}")
    print(f"  Core Proposition:  {idea_data.get('core_proposition', 'N/A')}")
    print(f"  Revenue Model:     {idea_data.get('revenue_model', 'N/A')}")
    print(f"  Competitors Found: {len(competitors)}")
    print(f"  Competition Score: {competition_score}/10")
    print("=" * 60)
    print("[OK] Test pipeline finished successfully!")


if __name__ == "__main__":
    run_test_pipeline()
