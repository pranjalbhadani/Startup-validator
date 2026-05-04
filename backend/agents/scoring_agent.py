"""
Agent 3: Scoring Engine
=======================
Takes a list of similar startups (from Agent 2 – Competitor Agent)
and computes a feasibility score, risk classification, market insights,
and actionable recommendations.

Enhanced with:
  - Unicorn proximity scoring (how close sector is to unicorn valuations)
  - Product Hunt trend scoring (market traction signals)
  - Macroeconomic context (interest rates, CPI affect risk)
  - Multi-source data awareness

Design Principles:
  - Fully explainable (no black-box ML)
  - Robust against messy data (nulls, missing fields)
  - Modular helper functions for testability
  - Clean JSON output for frontend consumption
"""

from typing import Any
import os
import json

from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini client for AI-powered insights
_gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
_gemini_config = types.GenerateContentConfig(response_mime_type="application/json")


# ─── Constants ────────────────────────────────────────────────────────────────

ACTIVE_STATUSES = {"active", "operating", "ipo"}
FAILED_STATUSES = {"closed", "shutdown"}

# Scoring weights (must sum to 1.0)
WEIGHT_SURVIVAL = 0.25
WEIGHT_COMPETITION = 0.15
WEIGHT_DEMAND = 0.20
WEIGHT_FUNDING = 0.15
WEIGHT_TREND = 0.15
WEIGHT_UNICORN = 0.10

# Normalization caps
MAX_COMPETITION_FOR_NORM = 50
MAX_TOTAL_FUNDING_FOR_DEMAND = 1e9
MAX_AVG_FUNDING_FOR_SCORE = 1e7

# Risk thresholds
RISK_LOW_THRESHOLD = 70
RISK_MEDIUM_THRESHOLD = 40


# ─── Preprocessing ───────────────────────────────────────────────────────────

def _preprocess_startups(startups: list[dict]) -> list[dict]:
    
    cleaned = []
    for s in startups:
        status = str(s.get("status", "unknown")).strip().lower()
        name = str(s.get("name", s.get("competitor_name", "Unknown"))).strip()

        funding_raw = s.get("funding_total_usd", s.get("funding_usd", s.get("funding", 0)))
        try:
            funding = float(str(funding_raw).replace(",", "").strip())
        except (ValueError, TypeError):
            funding = 0.0

        try:
            valuation = float(str(s.get("valuation", 0)).replace(",", "").strip())
        except (ValueError, TypeError):
            valuation = 0.0

        try:
            team_size = int(s.get("team_size", 0))
        except (ValueError, TypeError):
            team_size = 0

        try:
            market_size = float(s.get("market_size_billion", 0))
        except (ValueError, TypeError):
            market_size = 0.0

        cleaned.append({
            "name": name,
            "status": status,
            "funding_total_usd": max(funding, 0.0),
            "valuation": max(valuation, 0.0),
            "team_size": max(team_size, 0),
            "market_size_billion": max(market_size, 0.0),
            "source": str(s.get("source", "unknown")),
            "outcome": str(s.get("outcome", "")),
        })
    return cleaned


# ─── Core Metrics ─────────────────────────────────────────────────────────────

def _compute_metrics(startups: list[dict]) -> dict:
    
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

    # Unicorn proximity: what fraction of similar startups reached unicorn-level valuation
    unicorns = [s for s in startups if s["valuation"] >= 1e9 or s.get("outcome") == "unicorn"]
    unicorn_proximity = len(unicorns) / total if total > 0 else 0.0

    # Source diversity: how many different data sources are represented
    sources = set(s["source"] for s in startups if s["source"] != "unknown")
    source_count = len(sources)

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
        "unicorn_proximity": round(unicorn_proximity, 4),
        "source_count": source_count,
        "sources": list(sources),
    }


# ─── Trend Score ──────────────────────────────────────────────────────────────

def compute_trend_score(keywords: list[str], trend_data: list[dict] = None) -> float:
    """
    Compute a trend score (0–1) based on Product Hunt topic trends
    matching the startup's keywords.

    Higher votes + more posts for matching topics → higher trend score.
    """
    if not trend_data or not keywords:
        return 0.0

    keywords_lower = [k.lower().strip() for k in keywords]

    matching_trends = []
    for t in trend_data:
        topic = str(t.get("topic", "")).lower()
        if any(kw in topic or topic in kw for kw in keywords_lower):
            matching_trends.append(t)

    if not matching_trends:
        return 0.0

    total_votes = sum(t.get("total_votes", 0) for t in matching_trends)
    total_posts = sum(t.get("total_posts", 0) for t in matching_trends)

    # Normalize: 10K+ total votes across matching topics → 1.0
    vote_signal = min(total_votes / 10000, 1.0)
    # 100+ posts → 1.0
    post_signal = min(total_posts / 100, 1.0)

    trend_score = 0.6 * vote_signal + 0.4 * post_signal
    return round(min(trend_score, 1.0), 4)


# ─── Macro Context ────────────────────────────────────────────────────────────

def apply_macro_adjustment(score: float, macro_context: dict = None) -> tuple[float, str]:
   
    if not macro_context:
        return score, ""

    adjustment = 0.0
    reasons = []

    interest_rate = macro_context.get("interest_rate")
    if interest_rate is not None:
        try:
            rate = float(interest_rate)
            if rate > 5.0:
                adjustment -= 2.0
                reasons.append(f"High interest rates ({rate:.1f}%) increase funding difficulty")
            elif rate < 2.0:
                adjustment += 1.5
                reasons.append(f"Low interest rates ({rate:.1f}%) favor startup funding")
        except (ValueError, TypeError):
            pass

    cpi = macro_context.get("cpi")
    if cpi is not None:
        try:
            cpi_val = float(cpi)
            if cpi_val > 300:  # historical CPI, high = inflationary
                adjustment -= 1.0
                reasons.append("Elevated inflation increases operational costs")
        except (ValueError, TypeError):
            pass

    adjusted = max(0, min(100, score + adjustment))
    reasoning = ". ".join(reasons) if reasons else ""

    return round(adjusted, 2), reasoning


# ─── Scoring ──────────────────────────────────────────────────────────────────

def _calculate_score(metrics: dict, trend_score: float = 0.0) -> float:
    """
    Weighted composite score (0–100).

    Enhanced formula incorporating trend and unicorn signals.
    """
    raw = (
        WEIGHT_SURVIVAL * metrics["survival_rate"]
        + WEIGHT_COMPETITION * (1.0 - metrics["competition_normalized"])
        + WEIGHT_DEMAND * metrics["demand_score"]
        + WEIGHT_FUNDING * metrics["funding_score"]
        + WEIGHT_TREND * trend_score
        + WEIGHT_UNICORN * metrics["unicorn_proximity"]
    )
    return round(raw * 100, 2)


# ─── Risk Classification ─────────────────────────────────────────────────────

def _classify_risk(score: float) -> str:
    if score >= RISK_LOW_THRESHOLD:
        return "Low"
    elif score >= RISK_MEDIUM_THRESHOLD:
        return "Medium"
    return "High"


# ─── Insights ─────────────────────────────────────────────────────────────────

def _generate_insights(metrics: dict, trend_score: float = 0.0, macro_context: dict = None) -> dict:
    
    comp_norm = metrics["competition_normalized"]
    if comp_norm >= 0.7:
        competition_level = "High"
    elif comp_norm >= 0.3:
        competition_level = "Moderate"
    else:
        competition_level = "Low"

    survival = metrics["survival_rate"]
    if survival >= 0.6:
        market_health = "Strong"
    elif survival >= 0.3:
        market_health = "Moderate"
    else:
        market_health = "Weak"

    # Trend assessment
    if trend_score >= 0.6:
        trend_assessment = "Hot — strong Product Hunt traction"
    elif trend_score >= 0.3:
        trend_assessment = "Warm — moderate market interest"
    else:
        trend_assessment = "Cool — limited recent traction signals"

    # Unicorn potential
    up = metrics["unicorn_proximity"]
    if up >= 0.3:
        unicorn_potential = "High — sector has produced unicorns"
    elif up >= 0.1:
        unicorn_potential = "Moderate — some unicorn activity in sector"
    else:
        unicorn_potential = "Low — sector has few/no unicorns"

    insights = {
        "competition_level": competition_level,
        "market_health": market_health,
        "total_startups_analyzed": metrics["total_startups"],
        "active_startups": metrics["active_count"],
        "avg_funding_usd": metrics["avg_funding"],
        "trend_assessment": trend_assessment,
        "unicorn_potential": unicorn_potential,
        "data_sources_used": metrics.get("sources", []),
    }

    # Add macro context if available
    if macro_context:
        ir = macro_context.get("interest_rate")
        if ir is not None:
            insights["macro_interest_rate"] = ir
        cpi = macro_context.get("cpi")
        if cpi is not None:
            insights["macro_cpi"] = cpi

    return insights


# ─── Recommendations ─────────────────────────────────────────────────────────

def _generate_recommendations(metrics: dict, score: float, trend_score: float = 0.0, macro_reasoning: str = "") -> list[str]:
    """Generate dynamic, actionable recommendations based on metric signals."""
    recommendations: list[str] = []

    if metrics["competition_normalized"] >= 0.7:
        recommendations.append(
            "The market is highly competitive. Focus on a strong unique value "
            "proposition and niche targeting to differentiate from existing players."
        )

    if metrics["survival_rate"] < 0.4:
        recommendations.append(
            "Survival rate among similar startups is low. Validate demand "
            "thoroughly before committing significant resources. Consider "
            "lean experimentation to de-risk early."
        )

    if metrics["demand_score"] >= 0.6:
        recommendations.append(
            "Market demand signals are strong. This is a good opportunity "
            "window — move fast and aim for early traction to capture share."
        )

    if metrics["funding_score"] < 0.3:
        recommendations.append(
            "Average funding in this space is relatively low, suggesting "
            "cautious investor sentiment. Prepare a compelling pitch and "
            "consider bootstrapping or alternative funding sources."
        )

    if metrics["funding_score"] >= 0.7:
        recommendations.append(
            "Investor confidence in this sector is high. Leverage this by "
            "pursuing venture funding to accelerate growth."
        )

    if metrics["competition_normalized"] < 0.2:
        recommendations.append(
            "Competition is minimal. Validate that this reflects genuine "
            "opportunity rather than lack of market demand."
        )

    # Trend-based recommendations
    if trend_score >= 0.6:
        recommendations.append(
            "Product Hunt trends show strong traction in related topics. "
            "Consider launching on Product Hunt for initial visibility."
        )
    elif trend_score < 0.1 and metrics["demand_score"] < 0.4:
        recommendations.append(
            "Both market data and Product Hunt trends show limited activity. "
            "Validate that real demand exists before building."
        )

    # Unicorn-based recommendations
    if metrics["unicorn_proximity"] >= 0.2:
        recommendations.append(
            "This sector has produced unicorn-level companies. Study their "
            "growth trajectories and identify gaps they haven't addressed."
        )

    # Macro-based recommendations
    if macro_reasoning:
        recommendations.append(f"Macro environment: {macro_reasoning}")

    if not recommendations:
        recommendations.append(
            "The market shows balanced signals. Continue with standard "
            "validation — customer interviews, prototyping, and iterative testing."
        )

    return recommendations


# ─── Risk Factors ─────────────────────────────────────────────────────────────

def _derive_risk_factors(metrics: dict, trend_score: float = 0.0, macro_context: dict = None) -> list[dict]:
    """Derive structured risk factors from existing metrics."""
    factors: list[dict] = []

    comp = metrics["competition_normalized"]
    if comp >= 0.7:
        factors.append({"factor": "High Competition", "severity": "High",
            "detail": f"Market is crowded with {metrics['total_startups']} similar startups (normalized: {comp:.0%})."})
    elif comp >= 0.4:
        factors.append({"factor": "Moderate Competition", "severity": "Medium",
            "detail": f"{metrics['total_startups']} competitors detected (normalized: {comp:.0%})."})

    survival = metrics["survival_rate"]
    if survival < 0.3:
        factors.append({"factor": "Low Survival Rate", "severity": "High",
            "detail": f"Only {survival:.0%} of similar startups are still active."})
    elif survival < 0.5:
        factors.append({"factor": "Below-Average Survival", "severity": "Medium",
            "detail": f"{survival:.0%} survival rate among comparable startups."})

    funding = metrics["funding_score"]
    if funding < 0.2:
        factors.append({"factor": "Weak Funding Environment", "severity": "High",
            "detail": "Average funding in this space is very low, indicating cautious investors."})
    elif funding < 0.4:
        factors.append({"factor": "Limited Funding", "severity": "Medium",
            "detail": "Moderate investor interest — may need alternative funding strategies."})

    if trend_score < 0.15:
        factors.append({"factor": "Low Market Traction", "severity": "Medium",
            "detail": "Product Hunt trend signals are weak for related topics."})

    if macro_context:
        ir = macro_context.get("interest_rate")
        if ir is not None and float(ir) > 5.0:
            factors.append({"factor": "High Interest Rates", "severity": "Medium",
                "detail": f"Current rate ({float(ir):.1f}%) increases cost of capital."})
        cpi = macro_context.get("cpi")
        if cpi is not None and float(cpi) > 300:
            factors.append({"factor": "Inflationary Pressure", "severity": "Low",
                "detail": "Elevated CPI increases operational costs."})

    return factors


# ─── Opportunity Signals ──────────────────────────────────────────────────────

def _derive_opportunity_signals(metrics: dict, trend_score: float = 0.0) -> list[dict]:
    """Derive structured opportunity signals from existing metrics."""
    signals: list[dict] = []

    demand = metrics["demand_score"]
    if demand >= 0.7:
        signals.append({"signal": "Strong Market Demand", "strength": "Strong",
            "detail": "High demand score indicates significant unmet market needs."})
    elif demand >= 0.4:
        signals.append({"signal": "Moderate Demand", "strength": "Moderate",
            "detail": "Demand signals are encouraging but not overwhelming."})

    comp = metrics["competition_normalized"]
    if comp < 0.2:
        signals.append({"signal": "Low Competition", "strength": "Strong",
            "detail": "Very few competitors — potential blue ocean opportunity."})
    elif comp < 0.4:
        signals.append({"signal": "Manageable Competition", "strength": "Moderate",
            "detail": "Competition exists but the market is not saturated."})

    funding = metrics["funding_score"]
    if funding >= 0.6:
        signals.append({"signal": "High Investor Confidence", "strength": "Strong",
            "detail": "Strong average funding suggests active investor interest in this sector."})

    if trend_score >= 0.5:
        signals.append({"signal": "Trending Market", "strength": "Strong",
            "detail": "Product Hunt data shows strong recent traction in related topics."})
    elif trend_score >= 0.25:
        signals.append({"signal": "Growing Interest", "strength": "Moderate",
            "detail": "Moderate trend signals suggest building momentum."})

    up = metrics["unicorn_proximity"]
    if up >= 0.2:
        signals.append({"signal": "Unicorn Sector", "strength": "Strong",
            "detail": "This sector has produced unicorn-level companies."})

    if metrics["survival_rate"] >= 0.6:
        signals.append({"signal": "High Survivability", "strength": "Strong",
            "detail": f"{metrics['survival_rate']:.0%} of similar startups are still active."})

    return signals


# ─── AI-Powered Insight Generation ────────────────────────────────────


def generate_ai_insights(
    metrics: dict,
    idea_description: str = "",
    startup_name: str = "",
    industry: str = "",
    target_market: str = "",
    keywords: list[str] = None,
    trend_score: float = 0.0,
    macro_context: dict = None,
    score: float = 0.0,
    risk: str = "Unknown",
) -> dict:
    """
    Call Gemini to produce rich, context-aware insights instead of hard-coded templates.

    Returns a dict with keys:
      - insights: {competition_level, market_health, trend_assessment, unicorn_potential, ...}
      - recommendations: [str, ...]
      - risk_factors: [{factor, severity, detail}, ...]
      - opportunity_signals: [{signal, strength, detail}, ...]
      - market_reasoning: str
      - risk_reasoning: str

    Falls back to the deterministic helpers on any failure.
    """
    prompt = f"""You are a senior venture-capital analyst. Given the scoring metrics and context below,
produce a structured JSON analysis of this startup idea.

## Context
- Startup Name: {startup_name}
- Industry: {industry}
- Target Market: {target_market}
- Keywords: {', '.join(keywords or [])}
- Idea: {idea_description[:500]}

## Computed Metrics (0–1 normalized unless noted)
- Total similar startups found: {metrics.get('total_startups', 0)}
- Active/operating startups: {metrics.get('active_count', 0)}
- Failed startups: {metrics.get('failed_count', 0)}
- Survival rate: {metrics.get('survival_rate', 0):.2%}
- Competition (normalized): {metrics.get('competition_normalized', 0):.2%}
- Demand score: {metrics.get('demand_score', 0):.2%}
- Funding score: {metrics.get('funding_score', 0):.2%}
- Avg funding: ${metrics.get('avg_funding', 0):,.0f}
- Unicorn proximity: {metrics.get('unicorn_proximity', 0):.2%}
- Trend score: {trend_score:.2%}
- Feasibility score: {score}/100
- Risk classification: {risk}
- Macro interest rate: {macro_context.get('interest_rate', 'N/A') if macro_context else 'N/A'}
- Macro CPI: {macro_context.get('cpi', 'N/A') if macro_context else 'N/A'}

## Instructions
Return ONLY valid JSON matching this exact schema:

{{
  "insights": {{
    "competition_level": "High | Moderate | Low",
    "market_health": "Strong | Moderate | Weak",
    "trend_assessment": "<1-2 sentence assessment of market trends>",
    "unicorn_potential": "<1-2 sentence assessment of unicorn potential>",
    "avg_funding_usd": <number>,
    "data_sources_used": []
  }},
  "recommendations": [
    "<3-5 actionable, specific recommendations tailored to THIS startup>"
  ],
  "risk_factors": [
    {{
      "factor": "<short risk name>",
      "severity": "Low | Medium | High",
      "detail": "<1-2 sentence explanation specific to the startup>"
    }}
  ],
  "opportunity_signals": [
    {{
      "signal": "<short opportunity name>",
      "strength": "Weak | Moderate | Strong",
      "detail": "<1-2 sentence explanation specific to the startup>"
    }}
  ],
  "market_reasoning": "<a rich paragraph explaining the market dynamics, competition landscape, and demand signals for this startup>",
  "risk_reasoning": "<a rich paragraph with actionable advice combining the risk and opportunity analysis>"
}}

Rules:
- Be specific to the startup's industry and target market, not generic
- Ground assessments in the numeric metrics provided
- Include 2-5 risk_factors and 2-5 opportunity_signals
- Include 3-5 recommendations
- market_reasoning and risk_reasoning should each be 2-4 sentences
- competition_level, market_health must match the enum values exactly
- risk_factors.severity must be one of: Low, Medium, High
- opportunity_signals.strength must be one of: Weak, Moderate, Strong
"""

    try:
        response = _gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=_gemini_config,
        )

        result = json.loads(response.text)
        print("[Agent 3 - Scoring Engine] Gemini AI insights generated successfully.")

        # Validate structure minimally and backfill missing keys
        if "insights" not in result:
            result["insights"] = {}
        if "recommendations" not in result or not result["recommendations"]:
            result["recommendations"] = _generate_recommendations(metrics, score, trend_score)
        if "risk_factors" not in result or not result["risk_factors"]:
            result["risk_factors"] = _derive_risk_factors(metrics, trend_score, macro_context)
        if "opportunity_signals" not in result or not result["opportunity_signals"]:
            result["opportunity_signals"] = _derive_opportunity_signals(metrics, trend_score)

        # Ensure insights has required keys
        insights = result["insights"]
        insights.setdefault("competition_level", "Unknown")
        insights.setdefault("market_health", "Unknown")
        insights.setdefault("trend_assessment", "No data")
        insights.setdefault("unicorn_potential", "Unknown")
        insights.setdefault("avg_funding_usd", metrics.get("avg_funding", 0))
        insights.setdefault("data_sources_used", metrics.get("sources", []))

        # Ensure reasoning fields exist
        result.setdefault("market_reasoning", "")
        result.setdefault("risk_reasoning", "")

        return result

    except Exception as e:
        print(f"[Agent 3 - Scoring Engine] Gemini call failed, using deterministic fallback: {e}")
        # Fall back to existing deterministic functions
        fallback_insights = _generate_insights(metrics, trend_score, macro_context)
        fallback_recommendations = _generate_recommendations(metrics, score, trend_score)
        fallback_risk_factors = _derive_risk_factors(metrics, trend_score, macro_context)
        fallback_opportunities = _derive_opportunity_signals(metrics, trend_score)

        return {
            "insights": fallback_insights,
            "recommendations": fallback_recommendations,
            "risk_factors": fallback_risk_factors,
            "opportunity_signals": fallback_opportunities,
            "market_reasoning": "",
            "risk_reasoning": "; ".join(fallback_recommendations),
        }


# ─── Edge-Case Defaults ──────────────────────────────────────────────────────

def _empty_response() -> dict:
    """Default response when no startup data is available."""
    return {
        "score": 0.0,
        "risk": "High",
        "metrics": {
            "total_startups": 0, "active_count": 0, "failed_count": 0,
            "total_funding": 0.0, "avg_funding": 0.0, "survival_rate": 0.0,
            "competition_normalized": 0.0, "demand_score": 0.0,
            "funding_score": 0.0, "unicorn_proximity": 0.0,
            "source_count": 0, "sources": [],
        },
        "insights": {
            "competition_level": "Unknown", "market_health": "Unknown",
            "total_startups_analyzed": 0, "active_startups": 0,
            "avg_funding_usd": 0.0, "trend_assessment": "No data",
            "unicorn_potential": "Unknown", "data_sources_used": [],
        },
        "recommendations": [
            "No comparable startups were found in the database. "
            "This could indicate a novel idea or insufficient data. "
            "Consider manual market research to validate demand."
        ],
        "confidence": "none",
        "trend_score": 0.0,
        "macro_adjustment": "",
        "risk_factors": [],
        "opportunity_signals": [],
        "similar_startups": [],
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

def score_startups(
    similar_startups: list[dict[str, Any]],
    keywords: list[str] = None,
    trend_data: list[dict] = None,
    macro_context: dict = None,
) -> dict:
    """
    Agent 3 — Scoring Engine entry point.

    Enhanced to accept trend data and macro context for richer scoring.

    Args:
        similar_startups: List of startup dicts from Agent 2
        keywords:         Keywords from Agent 1 (for trend matching)
        trend_data:       Aggregated Product Hunt trend data
        macro_context:    Latest macro indicators dict

    Returns:
        Full scoring report with score, risk, metrics, insights, recommendations.
    """
    print("[Agent 3 - Scoring Engine] Starting feasibility analysis...")

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
        f"funding={metrics['funding_score']}, "
        f"unicorn_proximity={metrics['unicorn_proximity']}, "
        f"sources={metrics['sources']}"
    )

    # Compute trend score
    trend_score = compute_trend_score(keywords or [], trend_data)
    print(f"[Agent 3 - Scoring Engine] Trend score: {trend_score}")

    # Score
    final_score = _calculate_score(metrics, trend_score)

    # Macro adjustment
    final_score, macro_reasoning = apply_macro_adjustment(final_score, macro_context)
    if macro_reasoning:
        print(f"[Agent 3 - Scoring Engine] Macro adjustment: {macro_reasoning}")

    risk = _classify_risk(final_score)

    # Insights & recommendations
    insights = _generate_insights(metrics, trend_score, macro_context)
    recommendations = _generate_recommendations(metrics, final_score, trend_score, macro_reasoning)

    # Derive risk factors and opportunity signals from existing metrics
    risk_factors = _derive_risk_factors(metrics, trend_score, macro_context)
    opportunity_signals = _derive_opportunity_signals(metrics, trend_score)

    # Summarize similar startups for report (reuse already-cleaned data)
    similar_startups = [
        {
            "name": s["name"],
            "status": s["status"],
            "funding_total_usd": s["funding_total_usd"],
            "source": s["source"],
        }
        for s in cleaned
    ]

    result = {
        "score": final_score,
        "risk": risk,
        "metrics": metrics,
        "insights": insights,
        "recommendations": recommendations,
        "confidence": "high",
        "trend_score": trend_score,
        "macro_adjustment": macro_reasoning,
        "risk_factors": risk_factors,
        "opportunity_signals": opportunity_signals,
        "similar_startups": similar_startups,
    }

    if len(cleaned) < 3:
        result = _low_confidence_wrapper(result)

    print(
        f"[Agent 3 - Scoring Engine] Done. "
        f"Score={final_score}/100, Risk={risk}, Confidence={result['confidence']}"
    )

    return result


# ─── Standalone Test ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample_startups = [
        {"name": "HealthBot AI", "status": "operating", "funding_total_usd": 5000000, "source": "crunchbase", "valuation": 0},
        {"name": "MedConnect", "status": "operating", "funding_total_usd": 12000000, "source": "indian_funding", "valuation": 0},
        {"name": "DocStream", "status": "closed", "funding_total_usd": 800000, "source": "yc", "valuation": 0},
        {"name": "CareLink", "status": "active", "funding_total_usd": 3500000, "source": "crunchbase", "valuation": 0},
        {"name": "TeleHealth Plus", "status": "ipo", "funding_total_usd": 75000000, "source": "unicorn", "valuation": 2e9},
    ]

    sample_trends = [
        {"topic": "health", "total_votes": 5000, "total_posts": 50},
        {"topic": "telemedicine", "total_votes": 2000, "total_posts": 20},
    ]

    sample_macro = {"interest_rate": 4.5, "cpi": 310}

    print("=" * 60)
    print("AGENT 3 - SCORING ENGINE - ENHANCED TEST")
    print("=" * 60)

    report = score_startups(
        sample_startups,
        keywords=["health", "telemedicine", "AI"],
        trend_data=sample_trends,
        macro_context=sample_macro,
    )

    print(f"\n  Score:       {report['score']}/100")
    print(f"  Risk:        {report['risk']}")
    print(f"  Trend Score: {report['trend_score']}")
    print(f"  Macro:       {report['macro_adjustment']}")
    print(f"  Confidence:  {report['confidence']}")
    print(f"  Sources:     {report['metrics']['sources']}")
