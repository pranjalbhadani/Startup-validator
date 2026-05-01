/**
 * API Service Module
 * Handles all communication with the FastAPI backend server.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Shape of request sent to /validate
 */
export interface ValidateRequest {
  startup_name: string;
  idea_description: string;
  target_market: string;
  revenue_model?: string;
}

/**
 * Shape of a single competitor returned by the backend
 */
export interface CompetitorInfo {
  competitor_name: string;
  market: string;
  status: string;
  similarity_distance: number;
  funding?: string;
  // Enriched fields from unified data
  source?: string;
  country?: string;
  valuation?: number;
  investors?: string;
  year_founded?: string;
  outcome?: string;
}

/**
 * A single risk factor from the scoring engine.
 */
export interface RiskFactor {
  factor: string;
  severity: 'Low' | 'Medium' | 'High';
  detail: string;
}

/**
 * A single opportunity signal from the scoring engine.
 */
export interface OpportunitySignal {
  signal: string;
  strength: 'Weak' | 'Moderate' | 'Strong';
  detail: string;
}

/**
 * Qualitative insights derived from the scoring metrics.
 */
export interface ScoringInsights {
  competition_level: string;
  market_health: string;
  trend_assessment?: string;
  unicorn_potential?: string;
  avg_funding_usd?: number;
}

/**
 * Full scoring report from Agent 3 — Scoring Engine.
 */
export interface ScoringReport {
  score: number;
  risk: string;
  recommendations: string[];
  confidence: string;
  trend_score?: number;
  macro_adjustment?: string;
  risk_factors?: RiskFactor[];
  opportunity_signals?: OpportunitySignal[];
  insights?: ScoringInsights;
}

/**
 * Shape of the response from /validate
 */
export interface ValidationResponse {
  startup_name: string;
  industry_detected: string;
  target_market: string;
  core_proposition: string;
  revenue_model: string;
  keywords?: string[];
  competition_score: number;
  competitors: CompetitorInfo[];
  feasibility_score?: number;
  risk_level?: string;
  market_score?: number;
  market_reasoning?: string;
  risk_reasoning?: string;
  overall_validation_score?: number;
  scoring_report?: ScoringReport;
  // Enriched fields
  trend_score?: number;
  trend_assessment?: string;
  unicorn_potential?: string;
  data_sources_used?: string[];
  macro_context?: Record<string, unknown>;
}

/**
 * Custom error class for API errors
 */
export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * Sends startup data to the backend for validation.
 */
export async function validateStartup(
  data: ValidateRequest
): Promise<ValidationResponse> {
  const response = await fetch(`${API_BASE_URL}/validate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new ApiError(
      `Validation failed: ${errorBody || response.statusText}`,
      response.status
    );
  }

  return response.json();
}

/**
 * Health check to verify the backend is reachable.
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    const data = await response.json();
    return data.status === "running";
  } catch {
    return false;
  }
}
