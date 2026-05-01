"""
LangGraph Node Functions
========================
Each function is a LangGraph node:
  - Accepts the shared PipelineState
  - Returns a partial dict with only the keys it updates
  - Reuses existing agent logic — no duplication

Pipeline (STRICT):
  Input → input_agent → retrieval_agent →
    → (parallel) competitor_agent, market_agent, failure_agent
    → normalization_layer → scoring_agent → insight_generator → END
"""

import sys
import os
import time

# Ensure project root is importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Reuse existing agents
from utilities.idea_agent import extract_startup_details
from agents.competitor_agent import find_competitors
from agents.scoring_agent import (
    _preprocess_startups,
    ACTIVE_STATUSES,
    compute_trend_score,
    apply_macro_adjustment,
    generate_ai_insights,
)

from graph.state import PipelineState


# ─── Constants (from spec) ───────────────────────────────────────────────────

MAX_COMPETITION_FOR_NORM = 50
MAX_TOTAL_FUNDING_FOR_DEMAND = 1e9
MAX_AVG_FUNDING_FOR_SCORE = 1e7
CONFIDENCE_DENOMINATOR = 20

# Risk thresholds
RISK_LOW_THRESHOLD = 70
RISK_MEDIUM_THRESHOLD = 40

# Scoring weights (aligned with scoring_agent.py)
WEIGHT_SURVIVAL = 0.25
WEIGHT_COMPETITION = 0.15
WEIGHT_DEMAND = 0.20
WEIGHT_FUNDING = 0.15
WEIGHT_TREND = 0.15
WEIGHT_UNICORN = 0.10


# ─── Cached data loaders (loaded once per process) ──────────────────────────

_cached_trends = None
_cached_macro = None


def _get_product_hunt_trends() -> list[dict]:
    """Load Product Hunt trend data (cached after first call)."""
    global _cached_trends
    if _cached_trends is not None:
        return _cached_trends

    try:
        from agents.data_ingestion import load_product_hunt_trends
        _cached_trends = load_product_hunt_trends()
    except Exception as e:
        print(f"[LangGraph] Could not load PH trends: {e}")
        _cached_trends = []

    return _cached_trends


def _get_macro_context() -> dict:
    """Load macro context (cached after first call)."""
    global _cached_macro
    if _cached_macro is not None:
        return _cached_macro

    try:
        from agents.data_ingestion import load_macro_context
        _cached_macro = load_macro_context()
    except Exception as e:
        print(f"[LangGraph] Could not load macro context: {e}")
        _cached_macro = {}

    return _cached_macro


# ─── Node 1: Input Agent ────────────────────────────────────────────────────


def input_agent(state: PipelineState) -> dict:
    """
    Extracts structured data from the raw idea description using the
    existing Idea Understanding Agent (Agent 1).

    Outputs: idea_data, keywords
    """
    print("\n[LangGraph] Node: input_agent — starting")
    start = time.time()

    idea_data = extract_startup_details(
        user_idea_text=state["idea_description"]
    )

    # Fallback if the LLM call fails
    if idea_data is None:
        idea_data = {
            "startup_name": state.get("startup_name", "Unknown"),
            "industry": "Unknown",
            "keywords": [],
            "target_market": state.get("target_market", ""),
            "core_proposition": state["idea_description"][:100],
            "revenue_model": state.get("revenue_model", ""),
        }

    # Merge user-supplied overrides
    if state.get("startup_name") and idea_data.get("startup_name", "Unknown") == "Unknown":
        idea_data["startup_name"] = state["startup_name"]
    if state.get("target_market") and not idea_data.get("target_market"):
        idea_data["target_market"] = state["target_market"]
    if state.get("revenue_model") and not idea_data.get("revenue_model"):
        idea_data["revenue_model"] = state["revenue_model"]

    keywords = idea_data.get("keywords", [])

    elapsed = round(time.time() - start, 2)
    print(f"[LangGraph] Node: input_agent — done ({elapsed}s)")

    return {"idea_data": idea_data, "keywords": keywords}


# ─── Node 2: Retrieval Agent ────────────────────────────────────────────────


def retrieval_agent(state: PipelineState) -> dict:
    """
    Retrieves similar startups from the unified ChromaDB database,
    loads Product Hunt trend data, and loads macro context.

    Outputs: similar_startups, source_breakdown, product_hunt_trends, macro_context
    """
    print("\n[LangGraph] Node: retrieval_agent — starting")
    start = time.time()

    idea_data = state.get("idea_data", {})

    # Reuse existing ChromaDB retrieval (now unified across all sources)
    result = find_competitors(idea_data, n_results=10)
    raw_competitors = result.get("competitors", [])
    source_breakdown = result.get("source_breakdown", {})

    # Normalize into clean format for downstream scoring agents
    similar_startups = _preprocess_startups(raw_competitors)

    # Load supplementary data
    product_hunt_trends = _get_product_hunt_trends()
    macro_context = _get_macro_context()

    elapsed = round(time.time() - start, 2)
    print(
        f"[LangGraph] Node: retrieval_agent — retrieved "
        f"{len(similar_startups)} startups from {len(source_breakdown)} sources ({elapsed}s)"
    )

    return {
        "similar_startups": similar_startups,
        "raw_competitors": raw_competitors,
        "source_breakdown": source_breakdown,
        "product_hunt_trends": product_hunt_trends,
        "macro_context": macro_context,
    }


# ─── Node 3a: Competitor Agent (parallel) ────────────────────────────────────


def competitor_agent(state: PipelineState) -> dict:
    """
    Computes competition_score from the number of similar startups.
    Outputs: competition_score (float, [0, 1])
    """
    print("\n[LangGraph] Node: competitor_agent — starting")
    start = time.time()

    startups = state.get("similar_startups", [])
    competition = len(startups)

    competition_score = min(competition / MAX_COMPETITION_FOR_NORM, 1.0)

    elapsed = round(time.time() - start, 2)
    print(
        f"[LangGraph] Node: competitor_agent — "
        f"startups={competition}, competition_score={round(competition_score, 4)} ({elapsed}s)"
    )

    return {"competition_score": round(competition_score, 4)}


# ─── Node 3b: Market Agent (parallel) ───────────────────────────────────────


def market_agent(state: PipelineState) -> dict:
    """
    Computes demand_score and funding_score from startup funding data.
    Outputs: demand_score, funding_score
    """
    print("\n[LangGraph] Node: market_agent — starting")
    start = time.time()

    startups = state.get("similar_startups", [])
    total = len(startups)

    total_funding = sum(s.get("funding_total_usd", 0) for s in startups)
    avg_funding = total_funding / total if total > 0 else 0.0

    demand_score = min(
        0.5 * (total / MAX_COMPETITION_FOR_NORM)
        + 0.5 * (total_funding / MAX_TOTAL_FUNDING_FOR_DEMAND),
        1.0,
    )

    funding_score = min(avg_funding / MAX_AVG_FUNDING_FOR_SCORE, 1.0)

    elapsed = round(time.time() - start, 2)
    print(
        f"[LangGraph] Node: market_agent — "
        f"demand_score={round(demand_score, 4)}, "
        f"funding_score={round(funding_score, 4)} ({elapsed}s)"
    )

    return {
        "demand_score": round(demand_score, 4),
        "funding_score": round(funding_score, 4),
    }


# ─── Node 3c: Failure Agent (parallel) ──────────────────────────────────────


def failure_agent(state: PipelineState) -> dict:
    """
    Computes survival_rate from startup status data.
    Outputs: survival_rate (float, [0, 1])
    """
    print("\n[LangGraph] Node: failure_agent — starting")
    start = time.time()

    startups = state.get("similar_startups", [])
    total = len(startups)

    active_count = sum(
        1 for s in startups
        if s.get("status", "").lower() in ACTIVE_STATUSES
    )

    survival_rate = active_count / total if total > 0 else 0.0

    elapsed = round(time.time() - start, 2)
    print(
        f"[LangGraph] Node: failure_agent — "
        f"active={active_count}/{total}, "
        f"survival_rate={round(survival_rate, 4)} ({elapsed}s)"
    )

    return {"survival_rate": round(survival_rate, 4)}


# ─── Node 4: Normalization Layer ────────────────────────────────────────────


def normalization_layer(state: PipelineState) -> dict:
    """Ensures all metric values are clamped to [0, 1] range."""
    print("\n[LangGraph] Node: normalization_layer — starting")

    def clamp(v: float) -> float:
        return round(max(0.0, min(float(v), 1.0)), 4)

    competition_score = clamp(state.get("competition_score", 0))
    demand_score = clamp(state.get("demand_score", 0))
    funding_score = clamp(state.get("funding_score", 0))
    survival_rate = clamp(state.get("survival_rate", 0))

    print(
        f"[LangGraph] Node: normalization_layer — "
        f"competition={competition_score}, demand={demand_score}, "
        f"funding={funding_score}, survival={survival_rate}"
    )

    return {
        "competition_score": competition_score,
        "demand_score": demand_score,
        "funding_score": funding_score,
        "survival_rate": survival_rate,
    }


# ─── Node 5: Scoring Agent ─────────────────────────────────────────────────


def scoring_agent(state: PipelineState) -> dict:
    """
    Computes the final feasibility score using the enhanced opportunity–risk model.
    Now includes trend_score and macro adjustments.
    """
    print("\n[LangGraph] Node: scoring_agent — starting")
    start = time.time()

    competition_score = state.get("competition_score", 0)
    demand_score = state.get("demand_score", 0)
    funding_score = state.get("funding_score", 0)
    survival_rate = state.get("survival_rate", 0)
    similar_startups = state.get("similar_startups", [])
    keywords = state.get("keywords", [])
    product_hunt_trends = state.get("product_hunt_trends", [])
    macro_context = state.get("macro_context", {})

    # Compute trend score
    trend_score = compute_trend_score(keywords, product_hunt_trends)

    # Unicorn proximity from similar startups
    unicorns = [s for s in similar_startups if s.get("valuation", 0) >= 1e9 or s.get("outcome") == "unicorn"]
    total = len(similar_startups)
    unicorn_proximity = len(unicorns) / total if total > 0 else 0.0

    # ── Enhanced Score ───────────────────────────────────────────────────
    opportunity = (
        WEIGHT_DEMAND * demand_score
        + WEIGHT_FUNDING * funding_score
        + WEIGHT_TREND * trend_score
        + WEIGHT_UNICORN * unicorn_proximity
    )
    risk_value = (
        WEIGHT_SURVIVAL * (1.0 - survival_rate)
        + WEIGHT_COMPETITION * (competition_score ** 1.5)
    )

    raw_score = opportunity - risk_value
    normalized = (raw_score + 1.0) / 2.0
    final_score = round(normalized * 100, 2)

    # Macro adjustment
    final_score, macro_reasoning = apply_macro_adjustment(final_score, macro_context)

    # Risk Classification
    if final_score >= RISK_LOW_THRESHOLD:
        risk_label = "Low"
    elif final_score >= RISK_MEDIUM_THRESHOLD:
        risk_label = "Medium"
    else:
        risk_label = "High"

    # Confidence
    confidence = round(min(len(similar_startups) / CONFIDENCE_DENOMINATOR, 1.0), 4)

    elapsed = round(time.time() - start, 2)
    print(
        f"[LangGraph] Node: scoring_agent — "
        f"score={final_score}/100, risk={risk_label}, "
        f"trend={trend_score}, confidence={confidence} ({elapsed}s)"
    )

    return {
        "score": final_score,
        "risk": risk_label,
        "confidence": confidence,
        "trend_score": trend_score,
    }


# ─── Node 6: Insight Generator ──────────────────────────────────────────────


def insight_generator(state: PipelineState) -> dict:
    """
    Generates qualitative insights and actionable recommendations.
    Uses Gemini AI for rich, context-aware analysis with deterministic fallback.
    """
    print("\n[LangGraph] Node: insight_generator — starting")
    start = time.time()

    competition_score = state.get("competition_score", 0)
    demand_score = state.get("demand_score", 0)
    funding_score = state.get("funding_score", 0)
    survival_rate = state.get("survival_rate", 0)
    score = state.get("score", 0)
    risk = state.get("risk", "Unknown")
    confidence = state.get("confidence", 0)
    trend_score = state.get("trend_score", 0)
    idea_data = state.get("idea_data", {})
    similar_startups = state.get("similar_startups", [])
    raw_competitors = state.get("raw_competitors", [])
    source_breakdown = state.get("source_breakdown", {})
    macro_context = state.get("macro_context", {})
    keywords = state.get("keywords", [])

    # Build metrics dict for generate_ai_insights()
    total = len(similar_startups)
    active_count = sum(1 for s in similar_startups if s.get("status", "").lower() in ACTIVE_STATUSES)
    failed_count = sum(1 for s in similar_startups if s.get("status", "").lower() in {"closed", "shutdown"})
    total_funding = sum(s.get("funding_total_usd", 0) for s in similar_startups)
    avg_funding = total_funding / total if total > 0 else 0.0

    unicorns = [s for s in similar_startups if s.get("valuation", 0) >= 1e9 or s.get("outcome") == "unicorn"]
    unicorn_proximity = len(unicorns) / total if total > 0 else 0.0

    metrics = {
        "total_startups": total,
        "active_count": active_count,
        "failed_count": failed_count,
        "total_funding": round(total_funding, 2),
        "avg_funding": round(avg_funding, 2),
        "survival_rate": survival_rate,
        "competition_normalized": competition_score,
        "demand_score": demand_score,
        "funding_score": funding_score,
        "unicorn_proximity": round(unicorn_proximity, 4),
        "source_count": len(source_breakdown),
        "sources": list(source_breakdown.keys()) if source_breakdown else [],
    }

    # ── Call Gemini for AI-powered insights ───────────────────────────────
    ai_result = generate_ai_insights(
        metrics=metrics,
        idea_description=state.get("idea_description", ""),
        startup_name=idea_data.get("startup_name", state.get("startup_name", "Unknown")),
        industry=idea_data.get("industry", "Unknown"),
        target_market=idea_data.get("target_market", state.get("target_market", "")),
        keywords=keywords,
        trend_score=trend_score,
        macro_context=macro_context,
        score=score,
        risk=risk,
    )

    insights = ai_result.get("insights", {})
    recommendations = ai_result.get("recommendations", [])
    risk_factors = ai_result.get("risk_factors", [])
    opportunity_signals = ai_result.get("opportunity_signals", [])
    market_reasoning = ai_result.get("market_reasoning", "")
    risk_reasoning = ai_result.get("risk_reasoning", "")

    # Ensure data_sources_used is populated
    insights.setdefault("data_sources_used", list(source_breakdown.keys()) if source_breakdown else [])

    # Extract values for logging
    competition_level = insights.get("competition_level", "Unknown")
    market_health = insights.get("market_health", "Unknown")
    trend_assessment = insights.get("trend_assessment", "No data")
    unicorn_potential = insights.get("unicorn_potential", "Unknown")

    # Add low-data-confidence warning
    if len(similar_startups) < 3:
        recommendations.insert(0,
            "⚠ Only a small number of comparable startups were found. "
            "Results should be interpreted with caution."
        )

    if not similar_startups:
        recommendations.append(
            "No comparable startups found. Consider manual market research."
        )

    # ── Assemble final result ────────────────────────────────────────────
    # Use raw_competitors (original data from ChromaDB with competitor_name, market,
    # similarity_distance) for the API response, not the preprocessed similar_startups
    # which renames fields for internal scoring use.
    final_result = {
        # Idea data
        "startup_name": idea_data.get("startup_name", state.get("startup_name", "Unknown")),
        "industry_detected": idea_data.get("industry", "Unknown"),
        "target_market": idea_data.get("target_market", state.get("target_market", "")),
        "core_proposition": idea_data.get("core_proposition", ""),
        "revenue_model": idea_data.get("revenue_model", state.get("revenue_model", "")),
        "keywords": idea_data.get("keywords", []),

        # Competitors — use raw data so frontend gets competitor_name, market, similarity_distance
        "competition_score": round(competition_score * 10, 1),
        "competitors": raw_competitors if raw_competitors else similar_startups,

        # Core scores
        "feasibility_score": score,
        "risk_level": risk,
        "market_score": round(demand_score * 10, 1),

        # Reasoning — now from Gemini AI
        "market_reasoning": market_reasoning or (
            f"Market health is {market_health}. "
            f"Competition level is {competition_level}. "
            f"Trend: {trend_assessment}."
        ),
        "risk_reasoning": risk_reasoning or "; ".join(recommendations),

        # Overall
        "overall_validation_score": round(score / 10, 2),

        # Enriched data
        "trend_score": trend_score,
        "trend_assessment": trend_assessment,
        "unicorn_potential": unicorn_potential,
        "data_sources_used": list(source_breakdown.keys()) if source_breakdown else [],
        "macro_context": macro_context if macro_context else {},

        # Structured scoring report — now includes risk_factors and opportunity_signals
        "scoring_report": {
            "score": score,
            "risk": risk,
            "confidence": "high" if confidence >= 0.7 else "moderate" if confidence >= 0.3 else "low",
            "trend_score": trend_score,
            "metrics": metrics,
            "insights": insights,
            "recommendations": recommendations,
            "risk_factors": risk_factors,
            "opportunity_signals": opportunity_signals,
        },

        # Top-level spec fields
        "score": score,
        "risk": risk,
        "confidence": confidence,
        "metrics": {
            "survival_rate": survival_rate,
            "competition_score": competition_score,
            "demand_score": demand_score,
            "funding_score": funding_score,
        },
        "insights": insights,
        "recommendations": recommendations,
    }

    elapsed = round(time.time() - start, 2)
    print(
        f"[LangGraph] Node: insight_generator — "
        f"competition={competition_level}, market={market_health}, "
        f"trend={trend_assessment}, {len(recommendations)} recommendations, "
        f"{len(risk_factors)} risks, {len(opportunity_signals)} opportunities ({elapsed}s)"
    )

    return {
        "insights": insights,
        "recommendations": recommendations,
        "final_result": final_result,
    }

