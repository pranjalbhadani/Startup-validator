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
)

from graph.state import PipelineState


# ─── Constants (from spec) ───────────────────────────────────────────────────

MAX_COMPETITION_FOR_NORM = 50       # 50+ startups → competition_score = 1.0
MAX_TOTAL_FUNDING_FOR_DEMAND = 1e9  # $1B total funding cap for demand
MAX_AVG_FUNDING_FOR_SCORE = 1e7     # $10M avg funding cap
CONFIDENCE_DENOMINATOR = 20         # min(n/20, 1) for confidence

# Risk thresholds
RISK_LOW_THRESHOLD = 70
RISK_MEDIUM_THRESHOLD = 40


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
    Retrieves similar startups from the ChromaDB vector database
    using the existing Competitor Similarity Agent (Agent 2).

    If a LlamaIndex query_engine is added later, integrate it here.

    Outputs: similar_startups (list of dicts with status + funding)
    """
    print("\n[LangGraph] Node: retrieval_agent — starting")
    start = time.time()

    idea_data = state.get("idea_data", {})

    # Reuse existing ChromaDB retrieval
    result = find_competitors(idea_data)
    raw_competitors = result.get("competitors", [])

    # Normalize into a clean format for downstream agents
    similar_startups = _preprocess_startups(raw_competitors)

    elapsed = round(time.time() - start, 2)
    print(
        f"[LangGraph] Node: retrieval_agent — retrieved "
        f"{len(similar_startups)} similar startups ({elapsed}s)"
    )

    return {"similar_startups": similar_startups}


# ─── Node 3a: Competitor Agent (parallel) ────────────────────────────────────


def competitor_agent(state: PipelineState) -> dict:
    """
    Computes competition_score from the number of similar startups.

    Formula (from spec):
      competition_score = min(number_of_startups / 50, 1)

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
        f"startups={competition}, competition_score={round(competition_score, 4)} "
        f"({elapsed}s)"
    )

    return {"competition_score": round(competition_score, 4)}


# ─── Node 3b: Market Agent (parallel) ───────────────────────────────────────


def market_agent(state: PipelineState) -> dict:
    """
    Computes demand_score and funding_score from startup funding data.

    Formulas (from spec):
      total_funding = sum of all funding
      avg_funding   = total_funding / number_of_startups
      demand_score  = min(0.5 * (competition / 50) + 0.5 * (total_funding / 1e9), 1)
      funding_score = min(avg_funding / 1e7, 1)

    Outputs: demand_score (float, [0, 1]), funding_score (float, [0, 1])
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

    Active statuses: ["active", "operating", "ipo"]
    survival_rate = active_count / total_count

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
    """
    Ensures all metric values are clamped to [0, 1] range.

    Reads: competition_score, demand_score, funding_score, survival_rate
    Outputs: the same keys, clamped
    """
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


# ─── Node 5: Scoring Agent (CORE LOGIC) ────────────────────────────────────


def scoring_agent(state: PipelineState) -> dict:
    """
    Computes the final feasibility score using the opportunity–risk model.

    Formulas (from spec):
      opportunity = 0.6 * demand_score + 0.4 * funding_score
      risk        = 0.6 * (1 - survival_rate) + 0.4 * (competition_score ** 1.5)
      raw_score   = opportunity - risk
      score       = (raw_score + 1) / 2
      final_score = score * 100

    Risk classification:
      ≥ 70 → Low Risk
      ≥ 40 → Medium Risk
      < 40 → High Risk

    Confidence:
      confidence = min(number_of_startups / 20, 1)

    Outputs: score, risk, confidence
    """
    print("\n[LangGraph] Node: scoring_agent — starting")
    start = time.time()

    competition_score = state.get("competition_score", 0)
    demand_score = state.get("demand_score", 0)
    funding_score = state.get("funding_score", 0)
    survival_rate = state.get("survival_rate", 0)
    similar_startups = state.get("similar_startups", [])

    # ── Opportunity ──────────────────────────────────────────────────────
    opportunity = 0.6 * demand_score + 0.4 * funding_score

    # ── Risk ─────────────────────────────────────────────────────────────
    risk_value = (
        0.6 * (1.0 - survival_rate)
        + 0.4 * (competition_score ** 1.5)
    )

    # ── Final Score ──────────────────────────────────────────────────────
    raw_score = opportunity - risk_value
    normalized = (raw_score + 1.0) / 2.0
    final_score = round(normalized * 100, 2)

    # ── Risk Classification ──────────────────────────────────────────────
    if final_score >= RISK_LOW_THRESHOLD:
        risk_label = "Low"
    elif final_score >= RISK_MEDIUM_THRESHOLD:
        risk_label = "Medium"
    else:
        risk_label = "High"

    # ── Confidence ───────────────────────────────────────────────────────
    confidence = round(min(len(similar_startups) / CONFIDENCE_DENOMINATOR, 1.0), 4)

    elapsed = round(time.time() - start, 2)
    print(
        f"[LangGraph] Node: scoring_agent — "
        f"opportunity={round(opportunity, 4)}, risk={round(risk_value, 4)}, "
        f"score={final_score}/100, risk_label={risk_label}, "
        f"confidence={confidence} ({elapsed}s)"
    )

    return {
        "score": final_score,
        "risk": risk_label,
        "confidence": confidence,
    }


# ─── Node 6: Insight Generator ──────────────────────────────────────────────


def insight_generator(state: PipelineState) -> dict:
    """
    Generates qualitative insights and actionable recommendations
    from the computed metrics and score.

    Reuses logic patterns from agents/scoring_agent.py but adapted
    to the new pipeline state structure.

    Outputs: insights, recommendations, final_result
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
    idea_data = state.get("idea_data", {})
    similar_startups = state.get("similar_startups", [])

    # ── Competition level ────────────────────────────────────────────────
    if competition_score >= 0.7:
        competition_level = "High"
    elif competition_score >= 0.3:
        competition_level = "Moderate"
    else:
        competition_level = "Low"

    # ── Market health ────────────────────────────────────────────────────
    if survival_rate >= 0.6:
        market_health = "Strong"
    elif survival_rate >= 0.3:
        market_health = "Moderate"
    else:
        market_health = "Weak"

    insights = {
        "competition_level": competition_level,
        "market_health": market_health,
    }

    # ── Recommendations ──────────────────────────────────────────────────
    recommendations: list[str] = []

    # High competition → differentiation
    if competition_score >= 0.7:
        recommendations.append(
            "The market is highly competitive. Focus on a strong unique value "
            "proposition and niche targeting to differentiate from existing players."
        )

    # Low survival rate → risk warning
    if survival_rate < 0.4:
        recommendations.append(
            "Survival rate among similar startups is low. Validate demand "
            "thoroughly before committing significant resources. Consider "
            "lean experimentation to de-risk early."
        )

    # High demand → opportunity window
    if demand_score >= 0.6:
        recommendations.append(
            "Market demand signals are strong. This is a good opportunity "
            "window — move fast and aim for early traction to capture share."
        )

    # Low funding → weak investor confidence
    if funding_score < 0.3:
        recommendations.append(
            "Average funding in this space is relatively low, suggesting "
            "cautious investor sentiment. Prepare a compelling pitch and "
            "consider bootstrapping or alternative funding sources."
        )

    # High funding → strong ecosystem
    if funding_score >= 0.7:
        recommendations.append(
            "Investor confidence in this sector is high. Leverage this by "
            "pursuing venture funding to accelerate growth."
        )

    # Low competition → blue ocean
    if competition_score < 0.2:
        recommendations.append(
            "Competition is minimal. Validate that this reflects genuine "
            "opportunity rather than lack of market demand."
        )

    # Small dataset warning
    if len(similar_startups) < 3:
        recommendations.insert(
            0,
            "⚠ Only a small number of comparable startups were found. "
            "Results should be interpreted with caution."
        )

    # No data
    if not similar_startups:
        recommendations.append(
            "No comparable startups were found in the database. "
            "This could indicate a novel idea or insufficient data. "
            "Consider manual market research to validate demand."
        )

    # Fallback
    if not recommendations:
        recommendations.append(
            "The market shows balanced signals. Continue with standard "
            "validation — customer interviews, prototyping, and iterative testing."
        )

    # ── Assemble final result (matches API output schema) ────────────────
    final_result = {
        # Idea data
        "startup_name": idea_data.get(
            "startup_name", state.get("startup_name", "Unknown")
        ),
        "industry_detected": idea_data.get("industry", "Unknown"),
        "target_market": idea_data.get(
            "target_market", state.get("target_market", "")
        ),
        "core_proposition": idea_data.get("core_proposition", ""),
        "revenue_model": idea_data.get(
            "revenue_model", state.get("revenue_model", "")
        ),
        "keywords": idea_data.get("keywords", []),

        # Competitors
        "competition_score": round(competition_score * 10, 1),  # scale to 0-10 for UI
        "competitors": similar_startups,

        # Core scores
        "feasibility_score": score,
        "risk_level": risk,
        "market_score": round(demand_score * 10, 1),  # scale to 0-10 for UI

        # Reasoning
        "market_reasoning": (
            f"Market health is {market_health}. "
            f"Competition level is {competition_level}."
        ),
        "risk_reasoning": "; ".join(recommendations),

        # Overall
        "overall_validation_score": round(score / 10, 2),  # scale to 0-10 for UI

        # Structured scoring report (spec output format)
        "scoring_report": {
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
        },

        # Top-level spec output fields
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
        f"competition_level={competition_level}, market_health={market_health}, "
        f"{len(recommendations)} recommendations ({elapsed}s)"
    )

    return {
        "insights": insights,
        "recommendations": recommendations,
        "final_result": final_result,
    }
