"""
Scoring Engine — Integration Wrapper
=====================================
Provides a unified interface for the pipeline to invoke the scoring logic.
Delegates to agents/scoring_agent.py for the heavy lifting.
"""

from agents.scoring_agent import score_startups


def calculate_overall(
    market_score: int, competition_score: int, feasibility_score: int
) -> float:
    """
    Legacy weighted-average aggregator for backward compatibility.
    Combines individual agent scores into a single 0–10 overall score.

    Weights:
      market       → 35%
      competition  → 30%
      feasibility  → 35%
    """
    overall = (
        0.35 * market_score
        + 0.30 * competition_score
        + 0.35 * feasibility_score
    )
    return round(overall, 2)


def evaluate_competitors(competitors: list[dict]) -> dict:
    """
    Run the Agent 3 scoring engine against a list of competitor startups.

    This is the primary integration point used by the pipeline.
    Accepts the competitor list from Agent 2 and returns the full
    scoring report (score, risk, metrics, insights, recommendations).
    """
    return score_startups(competitors)
