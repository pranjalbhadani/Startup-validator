"""
Agent 3: Scoring Engine
=======================
Takes a list of similar startups (from Agent 2 – Competitor Agent)
and computes a feasibility score, risk classification, market insights,
and actionable recommendations.

Design Principles:
  - Fully explainable (no black-box ML)
  - Robust against messy data (nulls, missing fields)
  - Modular helper functions for testability
  - Clean JSON output for frontend consumption
"""

from typing import Any


# ─── Constants ────────────────────────────────────────────────────────────────

ACTIVE_STATUSES = {"active", "operating", "ipo"}
FAILED_STATUSES = {"closed", "shutdown"}

# Scoring weights (must sum to 1.0)
WEIGHT_SURVIVAL = 0.35
WEIGHT_COMPETITION = 0.20
WEIGHT_DEMAND = 0.25
WEIGHT_FUNDING = 0.20

# Normalization caps
MAX_COMPETITION_FOR_NORM = 50       # 50+ competitors → fully saturated
MAX_TOTAL_FUNDING_FOR_DEMAND = 1e9  # $1B total funding → max demand signal
MAX_AVG_FUNDING_FOR_SCORE = 1e7     # $10M average → max funding score

# Risk thresholds
RISK_LOW_THRESHOLD = 70
RISK_MEDIUM_THRESHOLD = 40


# ─── Preprocessing ───────────────────────────────────────────────────────────

def _preprocess_startups(startups: list[dict]) -> list[dict]:
    """
    Normalize and sanitize the raw startup list.
      - Lowercase status values
      - Default missing funding to 0
      - Strip whitespace from string fields
    """
    cleaned = []
    for s in startups:
        status = str(s.get("status", "unknown")).strip().lower()
        name = str(s.get("name", s.get("competitor_name", "Unknown"))).strip()

        funding_raw = s.get("funding_total_usd", s.get("funding", 0))
        try:
            funding = float(str(funding_raw).replace(",", "").strip())
        except (ValueError, TypeError):
            funding = 0.0

        cleaned.append({
            "name": name,
            "status": status,
            "funding_total_usd": max(funding, 0.0),
        })
    return cleaned


# ─── Core Metrics ─────────────────────────────────────────────────────────────

def _compute_metrics(startups: list[dict]) -> dict:
    """
    Compute all core evaluation metrics from the preprocessed startup list.

    Returns a dict with:
      total_startups, active_count, failed_count, total_funding,
      avg_funding, survival_rate, competition_normalized,
      demand_score, funding_score
    """
    total = len(startups)
    active_count = sum(1 for s in startups if s["status"] in ACTIVE_STATUSES)
    failed_count = sum(1 for s in startups if s["status"] in FAILED_STATUSES)
    total_funding = sum(s["funding_total_usd"] for s in startups)
    avg_funding = total_funding / total if total > 0 else 0.0

    survival_rate = active_count / total if total > 0 else 0.0
    competition_normalized = min(total / MAX_COMPETITION_FOR_NORM, 1.0)

    demand_score = min(
        0.4 * (total / MAX_COMPETITION_FOR_NORM)
        + 0.4 * (total_funding / MAX_TOTAL_FUNDING_FOR_DEMAND)
        + 0.2 * survival_rate,
        1.0,
    )

    funding_score = min(avg_funding / MAX_AVG_FUNDING_FOR_SCORE, 1.0)

    return {
        "total_startups": total,
        "active_count": active_count,
        "failed_count": failed_count,
        "total_funding": round(total_funding, 2),
        "avg_funding": round(avg_funding, 2),
        "survival_rate": round(survival_rate, 4),
        "competition_normalized": round(competition_normalized, 4),
        "demand_score": round(demand_score, 4),
        "funding_score": round(funding_score, 4),
    }


# ─── Scoring ──────────────────────────────────────────────────────────────────

def _calculate_score(metrics: dict) -> float:
    """
    Weighted composite score (0–100).

    Formula:
      score = (
          0.35 × survival_rate
        + 0.20 × (1 − competition_normalized)
        + 0.25 × demand_score
        + 0.20 × funding_score
      ) × 100
    """
    raw = (
        WEIGHT_SURVIVAL * metrics["survival_rate"]
        + WEIGHT_COMPETITION * (1.0 - metrics["competition_normalized"])
        + WEIGHT_DEMAND * metrics["demand_score"]
        + WEIGHT_FUNDING * metrics["funding_score"]
    )
    return round(raw * 100, 2)


# ─── Risk Classification ─────────────────────────────────────────────────────

def _classify_risk(score: float) -> str:
    """
    Classify feasibility risk based on the composite score.
      ≥ 70 → Low Risk
      ≥ 40 → Medium Risk
      else → High Risk
    """
    if score >= RISK_LOW_THRESHOLD:
        return "Low"
    elif score >= RISK_MEDIUM_THRESHOLD:
        return "Medium"
    return "High"


# ─── Insights ─────────────────────────────────────────────────────────────────

def _generate_insights(metrics: dict) -> dict:
    """
    Derive qualitative insights from computed metrics.
    """
    # Competition level
    comp_norm = metrics["competition_normalized"]
    if comp_norm >= 0.7:
        competition_level = "High"
    elif comp_norm >= 0.3:
        competition_level = "Moderate"
    else:
        competition_level = "Low"

    # Market health (based on survival rate)
    survival = metrics["survival_rate"]
    if survival >= 0.6:
        market_health = "Strong"
    elif survival >= 0.3:
        market_health = "Moderate"
    else:
        market_health = "Weak"

    return {
        "competition_level": competition_level,
        "market_health": market_health,
        "total_startups_analyzed": metrics["total_startups"],
        "active_startups": metrics["active_count"],
        "avg_funding_usd": metrics["avg_funding"],
    }


# ─── Recommendations ─────────────────────────────────────────────────────────

def _generate_recommendations(metrics: dict, score: float) -> list[str]:
    """
    Generate dynamic, actionable recommendations based on metric signals.
    """
    recommendations: list[str] = []

    # High competition → differentiation
    if metrics["competition_normalized"] >= 0.7:
        recommendations.append(
            "The market is highly competitive. Focus on a strong unique value "
            "proposition and niche targeting to differentiate from existing players."
        )

    # Low survival rate → risk warning
    if metrics["survival_rate"] < 0.4:
        recommendations.append(
            "Survival rate among similar startups is low. Validate demand "
            "thoroughly before committing significant resources. Consider "
            "lean experimentation to de-risk early."
        )

    # High demand → opportunity
    if metrics["demand_score"] >= 0.6:
        recommendations.append(
            "Market demand signals are strong. This is a good opportunity "
            "window — move fast and aim for early traction to capture share."
        )

    # Low funding → weak investor confidence
    if metrics["funding_score"] < 0.3:
        recommendations.append(
            "Average funding in this space is relatively low, suggesting "
            "cautious investor sentiment. Prepare a compelling pitch and "
            "consider bootstrapping or alternative funding sources."
        )

    # High funding → strong ecosystem
    if metrics["funding_score"] >= 0.7:
        recommendations.append(
            "Investor confidence in this sector is high. Leverage this by "
            "pursuing venture funding to accelerate growth."
        )

    # Low competition → blue ocean
    if metrics["competition_normalized"] < 0.2:
        recommendations.append(
            "Competition is minimal. Validate that this reflects genuine "
            "opportunity rather than lack of market demand."
        )

    # Fallback
    if not recommendations:
        recommendations.append(
            "The market shows balanced signals. Continue with standard "
            "validation — customer interviews, prototyping, and iterative testing."
        )

    return recommendations


# ─── Edge-Case Defaults ──────────────────────────────────────────────────────

def _empty_response() -> dict:
    """Default response when no startup data is available."""
    return {
        "score": 0.0,
        "risk": "High",
        "metrics": {
            "total_startups": 0,
            "active_count": 0,
            "failed_count": 0,
            "total_funding": 0.0,
            "avg_funding": 0.0,
            "survival_rate": 0.0,
            "competition_normalized": 0.0,
            "demand_score": 0.0,
            "funding_score": 0.0,
        },
        "insights": {
            "competition_level": "Unknown",
            "market_health": "Unknown",
            "total_startups_analyzed": 0,
            "active_startups": 0,
            "avg_funding_usd": 0.0,
        },
        "recommendations": [
            "No comparable startups were found in the database. "
            "This could indicate a novel idea or insufficient data. "
            "Consider manual market research to validate demand."
        ],
        "confidence": "none",
    }


def _low_confidence_wrapper(result: dict) -> dict:
    """Mark results from very small datasets (<3 startups) as moderate confidence."""
    result["confidence"] = "moderate"
    result["recommendations"].insert(
        0,
        "⚠ Only a small number of comparable startups were found. "
        "Results should be interpreted with caution."
    )
    return result


# ─── Public API ───────────────────────────────────────────────────────────────

def score_startups(similar_startups: list[dict[str, Any]]) -> dict:
    """
    Agent 3 — Scoring Engine entry point.

    Accepts a list of startup dicts (from Agent 2) and returns a structured
    evaluation report suitable for direct JSON serialization to the frontend.

    Args:
        similar_startups: List of dicts with keys:
            - name (str)
            - status (str)
            - funding_total_usd (number)

    Returns:
        {
            "score": float,         # 0–100
            "risk": str,            # "Low" | "Medium" | "High"
            "metrics": { ... },
            "insights": { ... },
            "recommendations": [ ... ],
            "confidence": str       # "high" | "moderate" | "none"
        }
    """
    print("[Agent 3 - Scoring Engine] Starting feasibility analysis...")

    # Edge case: no data
    if not similar_startups:
        print("[Agent 3 - Scoring Engine] No startups provided. Returning defaults.")
        return _empty_response()

    # Preprocess
    cleaned = _preprocess_startups(similar_startups)

    # Compute metrics
    metrics = _compute_metrics(cleaned)
    print(
        f"[Agent 3 - Scoring Engine] Metrics: "
        f"survival={metrics['survival_rate']}, "
        f"competition={metrics['competition_normalized']}, "
        f"demand={metrics['demand_score']}, "
        f"funding={metrics['funding_score']}"
    )

    # Score
    final_score = _calculate_score(metrics)
    risk = _classify_risk(final_score)

    # Insights & recommendations
    insights = _generate_insights(metrics)
    recommendations = _generate_recommendations(metrics, final_score)

    result = {
        "score": final_score,
        "risk": risk,
        "metrics": metrics,
        "insights": insights,
        "recommendations": recommendations,
        "confidence": "high",
    }

    # Edge case: very small dataset
    if len(cleaned) < 3:
        result = _low_confidence_wrapper(result)

    print(
        f"[Agent 3 - Scoring Engine] Done. "
        f"Score={final_score}/100, Risk={risk}, Confidence={result['confidence']}"
    )

    return result


# ─── Standalone Test ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Example input matching the prompt specification
    sample_startups = [
        {"name": "HealthBot AI", "status": "operating", "funding_total_usd": 5000000},
        {"name": "MedConnect", "status": "operating", "funding_total_usd": 12000000},
        {"name": "DocStream", "status": "closed", "funding_total_usd": 800000},
        {"name": "CareLink", "status": "active", "funding_total_usd": 3500000},
        {"name": "TeleHealth Plus", "status": "ipo", "funding_total_usd": 75000000},
    ]

    print("=" * 60)
    print("AGENT 3 - SCORING ENGINE - STANDALONE TEST")
    print("=" * 60)

    report = score_startups(sample_startups)

    print("\n--- SCORING REPORT ---")
    print(f"  Score:       {report['score']}/100")
    print(f"  Risk:        {report['risk']}")
    print(f"  Confidence:  {report['confidence']}")
    print(f"\n  Metrics:")
    for k, v in report["metrics"].items():
        print(f"    {k}: {v}")
    print(f"\n  Insights:")
    for k, v in report["insights"].items():
        print(f"    {k}: {v}")
    print(f"\n  Recommendations:")
    for i, r in enumerate(report["recommendations"], 1):
        print(f"    {i}. {r}")

    # Edge case test: empty input
    print("\n" + "=" * 60)
    print("EDGE CASE: Empty input")
    print("=" * 60)
    empty_report = score_startups([])
    print(f"  Score: {empty_report['score']}, Risk: {empty_report['risk']}")

    # Edge case test: small dataset
    print("\n" + "=" * 60)
    print("EDGE CASE: Small dataset (2 startups)")
    print("=" * 60)
    small_report = score_startups(sample_startups[:2])
    print(f"  Score: {small_report['score']}, Confidence: {small_report['confidence']}")
