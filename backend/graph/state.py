"""
Shared State for LangGraph Pipeline
====================================
Defines the TypedDict that flows through every node in the graph.
Each node reads what it needs and returns only the keys it updates.

Pipeline:
  Input → input_agent → retrieval_agent →
    → (parallel) competitor_agent, market_agent, failure_agent
    → normalization_layer → scoring_agent → insight_generator → END
"""

from typing import TypedDict, Optional


class PipelineState(TypedDict, total=False):
    """
    Shared state passed between LangGraph nodes.

    Keys are added progressively as each agent runs:
      - input_agent         → idea_data (keywords, industry, etc.)
      - retrieval_agent     → similar_startups, source_breakdown, product_hunt_trends, macro_context
      - competitor_agent    → competition_score
      - market_agent        → demand_score, funding_score
      - failure_agent       → survival_rate
      - normalization_layer → normalized flag
      - scoring_agent       → score, risk, confidence
      - insight_generator   → insights, recommendations, final_result
    """

    # ── Raw user inputs ──────────────────────────────────────────────────
    idea_description: str
    startup_name: str
    target_market: str
    revenue_model: str

    # ── Input Agent outputs ──────────────────────────────────────────────
    idea_data: dict          # structured idea data (industry, keywords, etc.)
    keywords: list           # extracted keywords for retrieval

    # ── Retrieval Agent outputs ──────────────────────────────────────────
    similar_startups: list   # list of dicts with status + funding (preprocessed)
    raw_competitors: list    # original competitor data from ChromaDB (with competitor_name, market, similarity_distance)
    source_breakdown: dict   # count of results per data source
    product_hunt_trends: list  # aggregated PH trend data for matching topics
    macro_context: dict      # latest macro indicators (interest_rate, cpi, etc.)

    # ── Competitor Agent outputs (parallel) ──────────────────────────────
    competition_score: float  # normalized [0, 1]

    # ── Market Agent outputs (parallel) ──────────────────────────────────
    demand_score: float       # normalized [0, 1]
    funding_score: float      # normalized [0, 1]

    # ── Failure Agent outputs (parallel) ─────────────────────────────────
    survival_rate: float      # normalized [0, 1]

    # ── Scoring Agent outputs ────────────────────────────────────────────
    score: float              # 0–100 final feasibility score
    risk: str                 # "Low" | "Medium" | "High"
    confidence: float         # [0, 1] confidence based on data quantity
    trend_score: float        # [0, 1] Product Hunt trend signal

    # ── Insight Generator outputs ────────────────────────────────────────
    insights: dict            # competition_level, market_health, trend_assessment, etc.
    recommendations: list     # actionable recommendation strings

    # ── Final assembled result ───────────────────────────────────────────
    final_result: dict        # complete JSON response for the API
