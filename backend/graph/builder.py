"""
LangGraph Graph Builder
=======================
Constructs the StateGraph with the full pipeline topology:

  START → input_agent → retrieval_agent
    → (parallel) competitor_agent, market_agent, failure_agent
    → normalization_layer → scoring_agent → insight_generator → END

The compiled graph is cached as a module-level singleton.
"""

from langgraph.graph import StateGraph, START, END

from graph.state import PipelineState
from graph.nodes import (
    input_agent,
    retrieval_agent,
    competitor_agent,
    market_agent,
    failure_agent,
    normalization_layer,
    scoring_agent,
    insight_generator,
)


def build_graph() -> StateGraph:
    """
    Build and compile the LangGraph pipeline.

    Graph topology:
      START → input_agent → retrieval_agent
        → [competitor_agent, market_agent, failure_agent]  (parallel)
        → normalization_layer → scoring_agent → insight_generator → END
    """

    graph = StateGraph(PipelineState)

    # ── Register nodes ───────────────────────────────────────────────────
    graph.add_node("input_agent", input_agent)
    graph.add_node("retrieval_agent", retrieval_agent)
    graph.add_node("competitor_agent", competitor_agent)
    graph.add_node("market_agent", market_agent)
    graph.add_node("failure_agent", failure_agent)
    graph.add_node("normalization_layer", normalization_layer)
    graph.add_node("scoring_agent", scoring_agent)
    graph.add_node("insight_generator", insight_generator)

    # ── Sequential: START → input → retrieval ────────────────────────────
    graph.add_edge(START, "input_agent")
    graph.add_edge("input_agent", "retrieval_agent")

    # ── Parallel fan-out: retrieval → 3 agents ───────────────────────────
    graph.add_edge("retrieval_agent", "competitor_agent")
    graph.add_edge("retrieval_agent", "market_agent")
    graph.add_edge("retrieval_agent", "failure_agent")

    # ── Fan-in: all 3 → normalization ────────────────────────────────────
    graph.add_edge("competitor_agent", "normalization_layer")
    graph.add_edge("market_agent", "normalization_layer")
    graph.add_edge("failure_agent", "normalization_layer")

    # ── Sequential: normalization → scoring → insights → END ─────────────
    graph.add_edge("normalization_layer", "scoring_agent")
    graph.add_edge("scoring_agent", "insight_generator")
    graph.add_edge("insight_generator", END)

    # ── Compile ──────────────────────────────────────────────────────────
    compiled = graph.compile()
    print("[LangGraph] Graph compiled successfully.")

    return compiled


# Module-level singleton — compiled once on first import
pipeline_graph = build_graph()
