AI AGENT BUILDER PROMPT – GENERATE FULL AGENTIC PIPELINE CODE (VENTURE VALIDATOR – EXISTING CODEBASE INTEGRATION)

You are a senior AI software engineer. Your task is to integrate and extend an EXISTING codebase by implementing a complete, production-ready agentic AI system for startup idea validation called Venture Validator.

---

OBJECTIVE
Build a modular agent-based pipeline that:

* Accepts a startup idea as input
* Reuses existing project components wherever possible
* Retrieves relevant startup data
* Performs parallel analysis using multiple agents
* Computes a feasibility score using a risk–opportunity model
* Generates structured, explainable output

You MUST extend the current project — NOT rebuild it from scratch.

---

⚠️ CRITICAL EXECUTION FLOW (MANDATORY)

### STEP 1 — CODEBASE ANALYSIS

Analyze the provided codebase and identify:

* Existing folder structure
* Core modules and services
* Data flow and entry points
* Existing retrieval logic (if any)
* Existing schemas / models
* Any LLM or AI-related components

Output:

```json
{
  "architecture": "...",
  "key_modules": [],
  "data_flow": "...",
  "reusable_components": [],
  "integration_points": []
}
```

DO NOT proceed without completing this step.

---

### STEP 2 — INTEGRATION PLAN

Based on the existing system:

* Decide where to integrate LangGraph
* Identify files to:

  * reuse
  * modify
  * create

Prefer minimal and clean integration.

Output:

```json
{
  "new_files": [],
  "modified_files": [],
  "reasoning": "..."
}
```

---

### STEP 3 — IMPLEMENTATION

Implement the system using the architecture below, while preserving and extending the existing code.

---

TECH STACK
Language: Python
Orchestration: LangGraph
Retrieval: LlamaIndex (reuse existing if available, otherwise mock cleanly)
LLM usage: optional placeholder (for future integration)

---

SYSTEM ARCHITECTURE (STRICT — DO NOT CHANGE)

Input → Input Agent → Retrieval Agent →
→ (parallel execution)
Competitor Agent
Market Agent
Failure Agent
→ Normalization Layer → Scoring Agent → Insight Generator → Final Output

---

STATE MANAGEMENT

Define a shared state object using TypedDict.

If a schema already exists, EXTEND it instead of recreating.

Include:

idea
keywords
similar_startups

Agent outputs:
competition_score
demand_score
funding_score
survival_rate

Final outputs:
score
risk
confidence
insights
recommendations

---

AGENT DEFINITIONS

Reuse existing utilities/services wherever possible.

1. Input Agent
   Extract keywords from idea
   Use existing parsing logic if available

2. Retrieval Agent
   Reuse existing retrieval system if present
   Otherwise simulate dataset retrieval
   Return:
   similar_startups (list of dicts with status + funding)

3. Competitor Agent
   Compute:
   competition = number of startups
   competition_score = min(competition / 50, 1)

4. Market Agent
   Compute:
   total_funding = sum of funding
   demand_score = min(
   0.5 * (competition / 50) +
   0.5 * (total_funding / 1e9),
   1
   )
   funding_score = min((avg funding) / 1e7, 1)

5. Failure Agent
   Compute:
   survival_rate based on active statuses:
   ["active", "operating", "ipo"]

6. Normalization Layer
   Ensure all values are in range [0,1]

7. Scoring Agent (CORE LOGIC)

Opportunity:
opportunity = 0.6 * demand_score + 0.4 * funding_score

Risk:
risk = (
0.6 * (1 - survival_rate) +
0.4 * (competition_score ** 1.5)
)

Final Score:
raw_score = opportunity - risk
score = (raw_score + 1) / 2
final_score = score * 100

---

8. Risk Classification

≥ 70 → Low Risk
≥ 40 → Medium Risk
< 40 → High Risk

---

9. Confidence Score

confidence = min(number_of_startups / 20, 1)

---

10. Insight Generator

Generate:

competition_level (High / Moderate / Low)
market_health (Strong / Moderate / Weak)

recommendations based on:
competition
survival
demand
funding

---

GRAPH CONSTRUCTION (LangGraph)

* Use StateGraph

* Define nodes for each agent

* Ensure:

  * Retrieval → parallel agents
  * Parallel agents → normalization → scoring
  * scoring → insight generator

* Integrate graph into existing execution flow (API / CLI / service layer)

---

OUTPUT FORMAT

Return structured JSON:

{
"score": number,
"risk": string,
"confidence": number,
"metrics": {
"survival_rate": number,
"competition_score": number,
"demand_score": number,
"funding_score": number
},
"insights": {
"competition_level": string,
"market_health": string
},
"recommendations": [ ... ]
}

---

DELIVERABLES (STRICT ORDER)

1. Codebase Analysis
2. Integration Plan
3. File Changes

For each file:

* If NEW → full code
* If MODIFIED → updated file or diff

---

CONSTRAINTS

* DO NOT rebuild the project
* DO NOT duplicate existing functionality
* DO NOT break current behavior
* DO NOT introduce unnecessary abstractions
* Prefer extension over replacement
* Handle edge cases (empty or small dataset)
* Keep scoring fully explainable

---

GOAL

Produce a scalable, modular, and explainable agentic AI system that integrates seamlessly into the existing codebase and can be extended with LLMs and vector databases.

---

START with codebase analysis, then proceed step-by-step.
