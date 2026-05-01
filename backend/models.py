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
    # Enriched fields from unified data
    source: Optional[str] = "unknown"
    country: Optional[str] = ""
    valuation: Optional[float] = 0.0
    investors: Optional[str] = ""
    year_founded: Optional[str] = "0"
    outcome: Optional[str] = ""


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
    unicorn_proximity: Optional[float] = 0.0
    source_count: Optional[int] = 0
    sources: Optional[List[str]] = []


class ScoringInsights(BaseModel):
    """Qualitative insights derived from metrics."""

    competition_level: str
    market_health: str
    total_startups_analyzed: Optional[int] = 0
    active_startups: Optional[int] = 0
    avg_funding_usd: Optional[float] = 0.0
    trend_assessment: Optional[str] = "No data"
    unicorn_potential: Optional[str] = "Unknown"
    data_sources_used: Optional[List[str]] = []
    macro_interest_rate: Optional[float] = None
    macro_cpi: Optional[float] = None


class RiskFactor(BaseModel):
    """A single derived risk factor."""
    factor: str
    severity: str  # "Low" | "Medium" | "High"
    detail: str


class OpportunitySignal(BaseModel):
    """A single derived opportunity signal."""
    signal: str
    strength: str  # "Weak" | "Moderate" | "Strong"
    detail: str


class SimilarStartupSummary(BaseModel):
    """Summary of a similar startup included in the report."""
    name: str
    status: str
    funding_total_usd: float
    source: str


class ScoringReport(BaseModel):
    """Full output from Agent 3 — Scoring Engine."""

    score: float
    risk: str
    metrics: ScoringMetrics
    insights: ScoringInsights
    recommendations: List[str]
    confidence: str
    trend_score: Optional[float] = 0.0
    macro_adjustment: Optional[str] = ""
    risk_factors: Optional[List[RiskFactor]] = []
    opportunity_signals: Optional[List[OpportunitySignal]] = []
    similar_startups: Optional[List[SimilarStartupSummary]] = []


# ─── Combined Pipeline Output ────────────────────────────────────────────────


class ValidationResult(BaseModel):
    """Output model for the /validate endpoint."""

    startup_name: str
    industry_detected: str
    target_market: str
    core_proposition: str
    revenue_model: str
    keywords: List[str]
    competition_score: float
    competitors: List[CompetitorInfo]
    feasibility_score: float
    risk_level: str
    market_score: float
    market_reasoning: str
    risk_reasoning: str
    overall_validation_score: float
    scoring_report: Optional[ScoringReport] = None
    # Enriched fields from multi-dataset integration
    trend_score: Optional[float] = 0.0
    trend_assessment: Optional[str] = ""
    unicorn_potential: Optional[str] = ""
    data_sources_used: Optional[List[str]] = []
    macro_context: Optional[dict] = {}
