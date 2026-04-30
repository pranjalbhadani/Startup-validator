ROLE: Senior Frontend Engineer (React)

OBJECTIVE
Understand the existing frontend codebase and refactor it to align with the Venture Validator UI architecture while preserving reusable components, styles, and logic.

---

## ⚠️ SCOPE CONSTRAINT (STRICT)

* ONLY make changes inside the **frontend/** folder
* DO NOT modify backend, scripts, configs outside frontend
* DO NOT move files outside frontend
* All new files must be created inside frontend/src

---

## ⚠️ EXECUTION FLOW (MANDATORY)

### STEP 1 — CODEBASE ANALYSIS

Analyze the frontend/ directory and identify:

* Folder structure
* Routing setup
* Existing pages and components
* API/service layer
* State management
* Styling approach

Output:

{
"architecture": "...",
"pages": [],
"components": [],
"state_management": "...",
"api_layer": "...",
"reusable_components": [],
"problems": []
}

DO NOT skip this step.

---

### STEP 2 — MAPPING TO TARGET STRUCTURE

Target Structure (inside frontend/src):

* app/: App.jsx, routes.jsx
* pages/: Home.jsx, Result.jsx
* components/: IdeaInput, ScoreCard, MetricsPanel, InsightsPanel, Recommendations, Loader
* features/validator/: validatorAPI.js, hooks.js
* services/: apiClient.js
* utils/, styles/

Map existing files:

{
"reuse": [],
"refactor": [],
"remove": [],
"new_files": []
}

---

### STEP 3 — REFACTORING RULES

* DO NOT rebuild from scratch
* DO NOT duplicate components
* Prefer refactoring existing components
* Preserve styling and UI
* Keep logic intact unless necessary
* Keep changes minimal

---

## 🎯 FUNCTIONAL REQUIREMENTS

### Routing

* "/" → Home
* "/result" → Result

---

### Home Page

* IdeaInput
* Accept idea
* Call API
* Navigate to Result

---

### Result Page

Render:

* ScoreCard
* MetricsPanel
* InsightsPanel
* Recommendations

---

### API

POST /validate

Request:
{ "idea": string }

Response:
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
"recommendations": []
}

---

### State Management

* loading
* data
* error

Prefer custom hook: useValidator

---

### Components

* IdeaInput → input + submit
* ScoreCard → score, risk, confidence
* MetricsPanel → metrics
* InsightsPanel → insights
* Recommendations → list
* Loader → loading

---

### Data Flow

Input → API → Store → Navigate → Render

---

## 📦 DELIVERABLES

1. Codebase Analysis
2. Mapping Plan
3. File Changes

* NEW → full code
* MODIFIED → updated code or diff

---

## 🚫 CONSTRAINTS

* Only modify frontend/
* Do not break existing features
* Do not duplicate logic
* Do not hardcode data
* Handle loading/empty states

---

## 🚀 GOAL

Refactor the frontend into a clean, scalable structure aligned with Venture Validator while maximizing reuse and limiting changes strictly to the frontend folder.

---

START with analysis.
