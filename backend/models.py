"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional, List


class StartupInput(BaseModel):
    """Input model for the /validate endpoint."""

    startup_name: str
    idea_description: str
    target_market: str
    revenue_model: Optional[str] = None


class CompetitorInfo(BaseModel):
    """Schema for a single competitor entry."""

    competitor_name: str
    market: str
    status: str
    similarity_distance: float


# ─── Scoring Engine Models (Agent 3) ─────────────────────────────────────────


class ScoringMetrics(BaseModel):
    """Core evaluation metrics from the scoring engine."""

    total_startups: int
    active_count: int
    failed_count: int
    total_funding: float
    avg_funding: float
    survival_rate: float
    competition_normalized: float
    demand_score: float
    funding_score: float


class ScoringInsights(BaseModel):
    """Qualitative insights derived from metrics."""

    competition_level: str
    market_health: str
    total_startups_analyzed: int
    active_startups: int
    avg_funding_usd: float


class ScoringReport(BaseModel):
    """Full output from Agent 3 — Scoring Engine."""

    score: float
    risk: str
    metrics: ScoringMetrics
    insights: ScoringInsights
    recommendations: List[str]
    confidence: str


# ─── Combined Pipeline Output ────────────────────────────────────────────────


class ValidationResult(BaseModel):
    """Output model for the /validate endpoint."""

    startup_name: str
    industry_detected: str
    target_market: str
    core_proposition: str
    revenue_model: str
    keywords: List[str]
    competition_score: int
    competitors: List[CompetitorInfo]
    feasibility_score: float
    risk_level: str
    market_score: float
    market_reasoning: str
    risk_reasoning: str
    overall_validation_score: float
    scoring_report: Optional[ScoringReport] = None
