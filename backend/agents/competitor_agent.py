"""
Agent 2: Competitor Similarity Agent
=====================================
Searches the unified ChromaDB vector database (built from multiple datasets)
to find similar startups. Returns a list of competitors and a competition_score.

Data sources searched:
  - Crunchbase VC investments (44K)
  - Indian Startup Funding 2020-2025 (1.1K)
  - Unicorn Companies (1K)
  - YC Startups Directory (688)
  - Startup Success Dataset (10K sampled)
"""

import os
import sys
import chromadb
from chromadb.utils import embedding_functions

# ─── Paths ───
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(AGENT_DIR, "..")
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "startup_vectordb")

# Legacy collection name (for backward compatibility)
LEGACY_COLLECTION = "crunchbase_startups"
# New unified collection name
UNIFIED_COLLECTION = "unified_startups"


def _get_collection():
    """
    Get the ChromaDB collection. Prefers the unified collection,
    falls back to the legacy crunchbase collection.
    """
    os.makedirs(DB_PATH, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    ef = embedding_functions.DefaultEmbeddingFunction()

    # Try unified first
    try:
        collection = chroma_client.get_collection(
            name=UNIFIED_COLLECTION, embedding_function=ef
        )
        if collection.count() > 0:
            return collection
    except Exception:
        pass

    # Fall back to legacy
    try:
        collection = chroma_client.get_collection(
            name=LEGACY_COLLECTION, embedding_function=ef
        )
        if collection.count() > 0:
            print("[Competitor Agent] Using legacy collection. Run data_ingestion.ingest_all() for enriched results.")
            return collection
    except Exception:
        pass

    # Create empty unified collection as last resort
    return chroma_client.get_or_create_collection(
        name=UNIFIED_COLLECTION, embedding_function=ef
    )


def load_csv_to_database():
    """
    Load all datasets into ChromaDB using the unified ingestion module.
    This replaces the old single-CSV loader.
    """
    from agents.data_ingestion import ingest_all
    ingest_all()


def find_competitors(idea_data: dict, n_results: int = 10, source_filter: str = None) -> dict:
    """
    Takes structured output from Agent 1 (Idea Agent).
    Searches the unified vector database for similar startups across ALL sources.

    Args:
        idea_data:     Structured dict with industry, target_market, core_proposition, keywords
        n_results:     Number of results to return (default 10 for richer data)
        source_filter: Optional — filter by source (e.g., "unicorn", "yc", "crunchbase")

    Returns:
      - competitors: list of matching startups with enriched details
      - competition_score: 0-10 based on similarity and status
      - source_breakdown: count of results per data source
    """
    print("[Agent 2 - Competitor Agent] Searching unified database...")

    collection = _get_collection()

    # Build a rich search query from the idea data
    industry = idea_data.get("industry", "").strip()
    target_market = idea_data.get("target_market", "").strip()
    proposition = idea_data.get("core_proposition", "").strip()
    keywords = idea_data.get("keywords", [])
    keyword_str = ", ".join(keywords) if keywords else ""

    search_query = (
        f"{industry} startup targeting {target_market}. "
        f"{proposition} "
        f"Keywords: {keyword_str}"
    )

    # Check if the collection has any data
    count = collection.count()
    if count == 0:
        print("[Agent 2 - Competitor Agent] WARNING: Database is empty!")
        print("[Agent 2 - Competitor Agent] Run: python -c \"from agents.data_ingestion import ingest_all; ingest_all()\"")
        return {"competitors": [], "competition_score": 0, "source_breakdown": {}}

    # Build metadata filter if source specified
    where_filter = None
    if source_filter:
        where_filter = {"source": source_filter}

    # Search the database
    query_kwargs = {
        "query_texts": [search_query],
        "n_results": min(n_results, count),
    }
    if where_filter:
        query_kwargs["where"] = where_filter

    results = collection.query(**query_kwargs)

    # Extract competitor data with enriched fields
    competitors = []
    source_breakdown = {}

    if results["documents"] and results["documents"][0]:
        for i in range(len(results["documents"][0])):
            meta = results["metadatas"][0][i]
            distance = results["distances"][0][i]

            source = meta.get("source", "unknown")
            source_breakdown[source] = source_breakdown.get(source, 0) + 1

            # Parse numeric metadata (stored as strings in ChromaDB)
            try:
                funding = float(meta.get("funding_usd", "0"))
            except (ValueError, TypeError):
                funding = 0.0

            try:
                valuation = float(meta.get("valuation", "0"))
            except (ValueError, TypeError):
                valuation = 0.0

            competitors.append({
                "competitor_name": meta.get("name", "Unknown"),
                "market": meta.get("industry", "unknown"),
                "status": meta.get("status", "unknown"),
                "funding": str(int(funding)) if funding > 0 else "0",
                "similarity_distance": round(distance, 4),
                # Enriched fields from unified data
                "source": source,
                "country": meta.get("country", ""),
                "valuation": valuation,
                "investors": meta.get("investors", "")[:200] if meta.get("investors") else "",
                "year_founded": meta.get("year_founded", "0"),
                "outcome": meta.get("outcome", ""),
            })

    # ─── Calculate Competition Score ───
    if competitors:
        avg_distance = sum(c["similarity_distance"] for c in competitors) / len(competitors)

        operating_count = sum(
            1 for c in competitors if c["status"] in ["operating", "active", "ipo"]
        )
        operating_ratio = operating_count / len(competitors)

        # Base score from similarity
        similarity_score = max(0, min(10, round(10 - (avg_distance * 4))))

        # Adjust based on active competitors
        competition_score = round(similarity_score * (0.5 + 0.5 * operating_ratio))
        competition_score = max(0, min(10, competition_score))
    else:
        competition_score = 0

    print(
        f"[Agent 2 - Competitor Agent] Found {len(competitors)} competitors "
        f"from {len(source_breakdown)} sources. Competition Score: {competition_score}/10"
    )
    print(f"[Agent 2 - Competitor Agent] Source breakdown: {source_breakdown}")

    return {
        "competitors": competitors,
        "competition_score": competition_score,
        "source_breakdown": source_breakdown,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("COMPETITOR AGENT — UNIFIED DATABASE TEST")
    print("=" * 60)

    # Load all data
    load_csv_to_database()

    # Test search
    fake_idea = {
        "industry": "HealthTech",
        "target_market": "Elderly patients in rural areas",
        "core_proposition": "Telemedicine video calls connecting rural patients with city doctors.",
        "keywords": ["telemedicine", "healthcare", "rural", "video consultation"],
    }

    result = find_competitors(fake_idea)
    print("\n--- COMPETITORS FOUND ---")
    for match in result["competitors"]:
        print(
            f"  [{match['source']}] {match['competitor_name']} | "
            f"Market: {match['market']} | Status: {match['status']} | "
            f"Distance: {match['similarity_distance']}"
        )
    print(f"\nCompetition Score: {result['competition_score']}/10")
    print(f"Source Breakdown: {result['source_breakdown']}")
