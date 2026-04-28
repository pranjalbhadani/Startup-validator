"""
Pipeline Controller
===================
Two-stage pipeline that uses:
  1. Idea Agent       (utilities/idea_agent.py)  → extracts structured data from raw idea text
  2. Competitor Agent  (agents/competitor_agent.py) → finds similar startups in ChromaDB

Flow:
  Raw Idea Text  →  Idea Agent  →  Structured Data  →  Competitor Agent  →  Results
"""

import sys
import os
import time

# --- Ensure project root is on sys.path so 'utilities/' can be imported ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import the two agents
from utilities.idea_agent import extract_startup_details
from agents.competitor_agent import find_competitors


def run_pipeline(
    idea_description: str,
    startup_name: str = "",
    target_market: str = "",
    revenue_model: str = "",
) -> dict:
    """
    Runs the two-stage validation pipeline.

    Flow:
      User Input → Idea Agent (utilities) → Competitor Agent → Final Report

    Args:
        idea_description: Raw startup idea text from the user.
        startup_name:     Optional startup name (used in output only).
        target_market:    Optional target-market hint (used in output only).
        revenue_model:    Optional revenue-model hint (used in output only).

    Returns:
        A structured validation report dict.
    """

    print("=" * 60)
    print("STARTUP VALIDATION PIPELINE - STARTED")
    print("=" * 60)

    # ─── Stage 1: Idea Understanding Agent (utilities/idea_agent.py) ───
    print("\n[Stage 1/2] Running Idea Understanding Agent...")
    start = time.time()
    idea_data = extract_startup_details(user_idea_text=idea_description)
    elapsed = round(time.time() - start, 2)

    if idea_data is None:
        print(f"[Stage 1/2] Idea Agent returned None (took {elapsed}s)")
        # Build a minimal fallback so the pipeline can still continue
        idea_data = {
            "startup_name": startup_name or "Unknown",
            "industry": "Unknown",
            "target_market": target_market,
            "core_proposition": idea_description[:100],
            "revenue_model": revenue_model,
        }
    else:
        print(f"[Stage 1/2] Idea Agent completed in {elapsed}s")

    # Merge in any user-supplied overrides the simple idea agent doesn't handle
    if startup_name and idea_data.get("startup_name", "Unknown") == "Unknown":
        idea_data["startup_name"] = startup_name
    if target_market and not idea_data.get("target_market"):
        idea_data["target_market"] = target_market
    if revenue_model and not idea_data.get("revenue_model"):
        idea_data["revenue_model"] = revenue_model

    # ─── Stage 2: Competitor Similarity Agent ───
    print("\n[Stage 2/2] Running Competitor Similarity Agent...")
    start = time.time()
    competitor_data = find_competitors(idea_data)
    elapsed = round(time.time() - start, 2)
    print(f"[Stage 2/2] Competitor Agent completed in {elapsed}s")

    # ─── Build Final Output ───
    competitors = competitor_data.get("competitors", [])
    competition_score = competitor_data.get("competition_score", 0)

    final_result = {
        "startup_name": idea_data.get("startup_name", startup_name or "Unknown"),
        "industry_detected": idea_data.get("industry", "Unknown"),
        "target_market": idea_data.get("target_market", target_market),
        "core_proposition": idea_data.get("core_proposition", ""),
        "revenue_model": idea_data.get("revenue_model", revenue_model),
        "competition_score": competition_score,
        "competitors": competitors,
    }

    print("\n" + "=" * 60)
    print("STARTUP VALIDATION PIPELINE - COMPLETE")
    print(f"  Startup Name:      {final_result['startup_name']}")
    print(f"  Industry:          {final_result['industry_detected']}")
    print(f"  Competitors Found: {len(competitors)}")
    print(f"  Competition Score: {competition_score}/10")
    print("=" * 60)

    return final_result
