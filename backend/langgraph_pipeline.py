"""
LangGraph Pipeline Controller
==============================
Drop-in replacement for pipeline.py that uses the LangGraph StateGraph
for orchestration. Provides the same run_pipeline() interface so
main.py can switch with a single import change.

Pipeline (LangGraph):
  Input → input_agent → retrieval_agent
    → (parallel) competitor_agent, market_agent, failure_agent
    → normalization_layer → scoring_agent → insight_generator → Output
"""

import sys
import os
import time

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from graph.builder import pipeline_graph


def run_pipeline(
    idea_description: str,
    startup_name: str = "",
    target_market: str = "",
    revenue_model: str = "",
) -> dict:
    """
    Runs the LangGraph-based validation pipeline.

    Same signature and return format as the original pipeline.run_pipeline()
    so main.py / app.py need only change their import.

    Args:
        idea_description: Raw startup idea text from the user.
        startup_name:     Optional startup name.
        target_market:    Optional target-market hint.
        revenue_model:    Optional revenue-model hint.

    Returns:
        A structured validation report dict (matches ValidationResult schema).
    """

    print("=" * 60)
    print("STARTUP VALIDATION PIPELINE (LangGraph) - STARTED")
    print("=" * 60)

    start = time.time()

    # Build the initial state
    initial_state = {
        "idea_description": idea_description,
        "startup_name": startup_name or "My Startup",
        "target_market": target_market or "General",
        "revenue_model": revenue_model or "",
    }

    # Run the compiled graph
    final_state = pipeline_graph.invoke(initial_state)

    elapsed = round(time.time() - start, 2)

    # Extract the assembled result
    result = final_state.get("final_result", {})

    print("\n" + "=" * 60)
    print("STARTUP VALIDATION PIPELINE (LangGraph) - COMPLETE")
    print(f"  Total time:        {elapsed}s")
    print(f"  Startup Name:      {result.get('startup_name', 'Unknown')}")
    print(f"  Industry:          {result.get('industry_detected', 'Unknown')}")
    print(f"  Competitors Found: {len(result.get('competitors', []))}")
    print(f"  Score:             {result.get('score', 0)}/100")
    print(f"  Risk:              {result.get('risk', 'Unknown')}")
    print(f"  Confidence:        {result.get('confidence', 0)}")
    print(f"  Overall (0-10):    {result.get('overall_validation_score', 0)}/10")
    print("=" * 60)

    return result
