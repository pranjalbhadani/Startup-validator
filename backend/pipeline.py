"""
Pipeline Controller (Legacy)
==============================
Three-stage pipeline that uses:
  1. Idea Agent       (agents/idea_agent.py)       → extracts structured data from raw idea text
  2. Competitor Agent  (agents/competitor_agent.py) → finds similar startups in ChromaDB
  3. Scoring Agent     (agents/scoring_agent.py)    → evaluates feasibility, risk, and insights

Enhanced with multi-dataset support:
  - Unified ChromaDB search across 5 data sources
  - Product Hunt trend scoring
  - Macroeconomic context adjustments

Flow:
  Raw Idea Text  →  Idea Agent  →  Structured Data  →  Competitor Agent  →  Scoring Agent  →  Results
"""

import sys
import os
import time

# --- Ensure project root is on sys.path so 'utilities/' can be imported ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import the three agents
from utilities.idea_agent import extract_startup_details
from agents.competitor_agent import find_competitors
from agents.scoring_agent import score_startups

# Import data loaders for enriched scoring
try:
    from agents.data_ingestion import load_product_hunt_trends, load_macro_context
    _HAS_ENRICHED_DATA = True
except ImportError:
    _HAS_ENRICHED_DATA = False


def run_pipeline(
    idea_description: str,
    startup_name: str = "",
    target_market: str = "",
    revenue_model: str = "",
) -> dict:
    """
    Runs the three-stage validation pipeline with multi-dataset support.
    """

    print("=" * 60)
    print("STARTUP VALIDATION PIPELINE - STARTED")
    print("=" * 60)

    # ─── Stage 1: Idea Understanding Agent ───────────────────────────────
    print("\n[Stage 1/3] Running Idea Understanding Agent...")
    start = time.time()
    idea_data = extract_startup_details(user_idea_text=idea_description)
    elapsed = round(time.time() - start, 2)

    if idea_data is None:
        print(f"[Stage 1/3] Idea Agent returned None (took {elapsed}s)")
        idea_data = {
            "startup_name": startup_name or "Unknown",
            "industry": "Unknown",
            "keywords": [],
            "target_market": target_market,
            "core_proposition": idea_description[:100],
            "revenue_model": revenue_model,
        }
    else:
        print(f"[Stage 1/3] Idea Agent completed in {elapsed}s")

    # Merge user-supplied overrides
    if startup_name and idea_data.get("startup_name", "Unknown") == "Unknown":
        idea_data["startup_name"] = startup_name
    if target_market and not idea_data.get("target_market"):
        idea_data["target_market"] = target_market
    if revenue_model and not idea_data.get("revenue_model"):
        idea_data["revenue_model"] = revenue_model

    keywords = idea_data.get("keywords", [])

    # ─── Stage 2: Competitor Similarity Agent ────────────────────────────
    print("\n[Stage 2/3] Running Competitor Similarity Agent...")
    start = time.time()
    competitor_data = find_competitors(idea_data)
    elapsed = round(time.time() - start, 2)
    print(f"[Stage 2/3] Competitor Agent completed in {elapsed}s")

    competitors = competitor_data.get("competitors", [])
    competition_score = competitor_data.get("competition_score", 0)
    source_breakdown = competitor_data.get("source_breakdown", {})

    # ─── Load enriched data ──────────────────────────────────────────────
    trend_data = []
    macro_context = {}
    if _HAS_ENRICHED_DATA:
        try:
            trend_data = load_product_hunt_trends()
        except Exception:
            pass
        try:
            macro_context = load_macro_context()
        except Exception:
            pass

    # ─── Stage 3: Scoring Engine ─────────────────────────────────────────
    print("\n[Stage 3/3] Running Scoring Engine...")
    start = time.time()
    scoring_report = score_startups(
        competitors,
        keywords=keywords,
        trend_data=trend_data,
        macro_context=macro_context,
    )
    elapsed = round(time.time() - start, 2)
    print(f"[Stage 3/3] Scoring Engine completed in {elapsed}s")

    # ─── Build Final Output ──────────────────────────────────────────────
    final_result = {
        # Idea data
        "startup_name": idea_data.get("startup_name", startup_name or "Unknown"),
        "industry_detected": idea_data.get("industry", "Unknown"),
        "target_market": idea_data.get("target_market", target_market),
        "core_proposition": idea_data.get("core_proposition", ""),
        "revenue_model": idea_data.get("revenue_model", revenue_model),
        "keywords": keywords,
        # Competition data
        "competition_score": competition_score,
        "competitors": competitors,
        # Scoring engine data
        "feasibility_score": scoring_report.get("score", 0),
        "risk_level": scoring_report.get("risk", "Unknown"),
        "market_score": round(scoring_report.get("metrics", {}).get("demand_score", 0) * 10, 1),
        "market_reasoning": (
            f"Market health is {scoring_report.get('insights', {}).get('market_health', 'Unknown')}. "
            f"Competition level is {scoring_report.get('insights', {}).get('competition_level', 'Unknown')}."
        ),
        "risk_reasoning": "; ".join(scoring_report.get("recommendations", [])),
        "overall_validation_score": round(
            (
                scoring_report.get("metrics", {}).get("demand_score", 0) * 10 * 0.35
                + competition_score * 0.30
                + scoring_report.get("score", 0) / 10 * 0.35
            ),
            2,
        ),
        # Full scoring report
        "scoring_report": scoring_report,
        # Enriched data
        "trend_score": scoring_report.get("trend_score", 0),
        "trend_assessment": scoring_report.get("insights", {}).get("trend_assessment", ""),
        "unicorn_potential": scoring_report.get("insights", {}).get("unicorn_potential", ""),
        "data_sources_used": scoring_report.get("metrics", {}).get("sources", []),
        "macro_context": macro_context,
    }

    print("\n" + "=" * 60)
    print("STARTUP VALIDATION PIPELINE - COMPLETE")
    print(f"  Startup Name:      {final_result['startup_name']}")
    print(f"  Industry:          {final_result['industry_detected']}")
    print(f"  Competitors Found: {len(competitors)}")
    print(f"  Data Sources:      {source_breakdown}")
    print(f"  Competition Score: {competition_score}/10")
    print(f"  Feasibility Score: {final_result['feasibility_score']}/100")
    print(f"  Risk Level:        {final_result['risk_level']}")
    print(f"  Trend Score:       {final_result['trend_score']}")
    print(f"  Overall Score:     {final_result['overall_validation_score']}/10")
    print("=" * 60)

    return final_result
