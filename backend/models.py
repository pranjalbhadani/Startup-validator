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


class ValidationResult(BaseModel):
    """Output model for the /validate endpoint."""

    startup_name: str
    industry_detected: str
    keywords: List[str]
    core_proposition: str
    market_score: int
    market_reasoning: str
    competition_score: int
    competitors: List[CompetitorInfo]
    feasibility_score: int
    risk_level: str
    risk_reasoning: str
    overall_validation_score: float
