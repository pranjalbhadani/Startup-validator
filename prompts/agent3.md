AI AGENT BUILDER PROMPT – IMPLEMENT AGENT 3 (SCORING ENGINE)
You are a senior AI software engineer. Your task is to design and implement a production-ready “Agent 3 – Scoring Engine” for a startup evaluation system called Venture Validator.
The system already has:
Agent 1: Extracts keywords from startup idea (LLM-based)
Agent 2: Retrieves similar startups (vector database like ChromaDB)
You are responsible ONLY for Agent 3.

OBJECTIVE
Build a robust, modular, and explainable scoring engine that:
Takes similar startups as input
Computes evaluation metrics
Generates a feasibility score
Classifies risk
Produces insights and recommendations
Returns clean JSON output for frontend use

INPUT FORMAT
Your function will receive:
List of startup objects:
[
{
"name": string,
"status": string,
"funding_total_usd": number
}
]

TECH REQUIREMENTS
Language: Python
Framework compatibility: FastAPI
Code should be modular and reusable
Handle real-world messy data (nulls, missing fields)

IMPLEMENTATION TASKS
1. Preprocessing
Normalize status values (lowercase)
Handle missing funding values (default = 0)
Define:
Active statuses = ["active", "operating", "ipo"]
Failed statuses = ["closed", "shutdown"]

2. Compute Core Metrics
Implement:
survival_rate = active_count / total_startups
competition = total_startups
competition_normalized = min(competition / 50, 1)
demand_score using:
demand_score = min(
0.4 * (competition / 50) +
0.4 * (total_funding / 1e9) +
0.2 * (active_count / total_startups),
1
)
funding_score:
avg_funding = total_funding / total_startups
funding_score = min(avg_funding / 1e7, 1)

3. Scoring Model
Use weighted formula:
score = (
0.35 * survival_rate +
0.20 * (1 - competition_normalized) +
0.25 * demand_score +
0.20 * funding_score
)
final_score = score * 100

4. Risk Classification
≥ 70 → Low Risk
≥ 40 → Medium Risk
else → High Risk

5. Insights Generation
Generate:
competition_level:
High / Moderate / Low
market_health:
Strong / Moderate / Weak

6. Recommendations
Generate dynamic recommendations based on:
High competition → suggest differentiation
Low survival → warn risk
High demand → highlight opportunity
Low funding → warn weak investor confidence

7. Edge Case Handling
If no startups:
return default response with warning
If very small dataset (<3):
return moderate confidence result

OUTPUT FORMAT
Return:
{
"score": number,
"risk": string,
"metrics": {...},
"insights": {...},
"recommendations": [...]
}

DELIVERABLES
You must generate:
Clean Python function (agent3)
Helper functions (modular design)
FastAPI-compatible structure
Example input + output
Brief explanation of logic

CONSTRAINTS
Avoid redundant metrics (do not use both failure rate and survival rate)
Keep model explainable (no black-box ML)
Ensure normalization of all metrics
Keep code clean and readable

GOAL
Produce a fully functional, production-ready scoring engine that is:
Explainable
Robust
Easy to integrate
Suitable for academic + real-world use
