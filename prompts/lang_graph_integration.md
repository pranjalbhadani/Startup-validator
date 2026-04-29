You are a senior AI systems engineer integrating LangGraph into an EXISTING Python codebase.

Your task is to EXTEND the current project — NOT rebuild it.

---

## 🎯 OBJECTIVE

Implement a LangGraph-based agent workflow for a "Startup Idea Validator" inside the existing project.

Pipeline (FIXED — DO NOT CHANGE):
Input → Input Agent → Retrieval Agent → (parallel)
→ Competitor Agent + Market/Failure Agent → Scoring Agent → Output

---

## ⚠️ CRITICAL RULE: UNDERSTAND BEFORE BUILD

You MUST follow this sequence:

### STEP 1 — CODEBASE ANALYSIS

* Read and analyze the provided codebase

* Identify:

  * existing modules and folder structure
  * data flow
  * services (APIs, retrieval, utils, etc.)
  * any existing AI/LLM usage
  * data models and schemas

* Output a structured summary:

```json
{
  "architecture": "...",
  "key_modules": [],
  "data_flow": "...",
  "reusable_components": [],
  "integration_points": []
}
```

DO NOT SKIP THIS STEP.

---

### STEP 2 — INTEGRATION PLAN

Based ONLY on the existing codebase:

* Decide:

  * where LangGraph should live
  * which files to modify
  * which new files to create

* Prefer:

  * reusing existing services
  * extending current logic
  * minimal disruption

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

Now implement LangGraph with these constraints:

---

## ⚙️ IMPLEMENTATION REQUIREMENTS

### 1. DO NOT BREAK EXISTING CODE

* Preserve current functionality
* Do not rename or delete existing modules unless necessary

---

### 2. USE EXISTING COMPONENTS

* If a retrieval system exists → reuse it
* If schemas exist → extend them
* If API layer exists → integrate there

Avoid duplication.

---

### 3. LANGGRAPH SETUP

You MUST:

* Define a shared State (reuse existing schema if possible)

* Implement nodes:

  * input_agent
  * retrieval_agent
  * competitor_agent
  * market_failure_agent
  * scoring_agent

* Build graph using StateGraph

* Add:

  * entry node
  * parallel execution
  * merge into scoring node

---

### 4. AGENT DESIGN

Each agent:

* accepts `state`
* returns partial updates only
* uses structured JSON outputs
* uses minimal, efficient prompts

---

### 5. LLAMAINDEX / RETRIEVAL

* If retrieval already exists → CALL it
* Otherwise → integrate query_engine cleanly
* Do NOT rebuild retrieval if already present

---

### 6. OUTPUT FORMAT

Final result:

{
"score": int,
"verdict": "strong | moderate | weak",
"reasons": [],
"opportunities": []
}

---

## 📦 DELIVERABLE FORMAT (STRICT)

You MUST respond in this order:

### 1. Codebase Analysis

### 2. Integration Plan

### 3. File Changes

For each file:

* If NEW → full code
* If MODIFIED → show diff-style or full updated file

---

## 🚫 WHAT NOT TO DO

* Do NOT create a new project from scratch
* Do NOT ignore existing code
* Do NOT duplicate functionality
* Do NOT write placeholder code
* Do NOT overengineer abstractions

---

## 🧠 ENGINEERING MINDSET

* Think like you're joining a real startup codebase
* Be conservative with changes
* Optimize for maintainability
* Keep it clean and minimal

---

## 🚀 START

First analyze the codebase, then proceed step-by-step.
