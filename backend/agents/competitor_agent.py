"""
Agent 2: Competitor Similarity Agent
Searches a local ChromaDB vector database (built from cleaned CSV data)
to find similar startups. Returns a list of competitors and a competition_score.
"""

import os
import sys
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

# ─── Paths (relative to this file → backend/agents/) ───
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(AGENT_DIR, "..")
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))

# Store the VectorDB inside the data/ directory
DB_PATH = os.path.join(PROJECT_ROOT, "data", "startup_vectordb")

# Path to the CLEANED CSV (output of utilities/data_cleaning.py)
CLEANED_CSV_PATH = os.path.join(
    PROJECT_ROOT, "data", "processed", "cleaned_investments_sent.csv"
)


def _get_collection():
    """
    Create or retrieve the ChromaDB collection.
    Wrapped in a function to avoid hanging on import if the DB
    directory doesn't exist yet.
    """
    os.makedirs(DB_PATH, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()
    collection = chroma_client.get_or_create_collection(
        name="crunchbase_startups", embedding_function=sentence_transformer_ef
    )
    return collection


def load_csv_to_database(csv_file_path: str = None):
    """
    Load the cleaned CSV into ChromaDB vector database.
    Uses the cleaned CSV by default (from data/processed/cleaned_investments_sent.csv).
    Run this ONCE to populate the database.
    """
    if csv_file_path is None:
        csv_file_path = CLEANED_CSV_PATH

    print(f"[Competitor Agent] DB_PATH:  {DB_PATH}")
    print(f"[Competitor Agent] CSV_PATH: {csv_file_path}")

    if not os.path.exists(csv_file_path):
        print(f"[Competitor Agent] ERROR: CSV not found at {csv_file_path}")
        print("[Competitor Agent] Run 'python utilities/data_cleaning.py' first.")
        return

    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        print(f"[Competitor Agent] Error reading CSV: {e}")
        return

    df = df.dropna(subset=["name", "market", "status"])

    print(f"[Competitor Agent] Loaded {len(df)} startups from cleaned dataset.")

    collection = _get_collection()

    # Check if data is already fully loaded
    existing_count = collection.count()
    if existing_count >= len(df) * 0.9:
        print(f"[Competitor Agent] Database already contains {existing_count} records (CSV has {len(df)}).")
        print("[Competitor Agent] Skipping load. Delete data/startup_vectordb/ to reload.")
        return
    elif existing_count > 0:
        print(f"[Competitor Agent] Partial load detected: {existing_count} of {len(df)} records.")
        print("[Competitor Agent] Resuming load using upsert...")

    # Create rich searchable documents combining name, market, and funding info
    documents = []
    metadatas = []
    ids = []

    for idx, row in df.iterrows():
        name = str(row["name"]).strip()
        market = str(row["market"]).strip()
        status = str(row["status"]).strip()
        funding_raw = str(row.get("funding_total_usd", "0")).replace(",", "").strip()
        try:
            funding = int(float(funding_raw))
        except (ValueError, TypeError):
            funding = 0

        # Build a descriptive document for better semantic search
        doc = f"{name} is a {status} startup in the {market} industry."
        if funding > 0:
            doc += f" Total funding: ${funding:,}."

        documents.append(doc)
        metadatas.append(
            {"name": name, "status": status, "market": market, "funding": str(funding)}
        )
        ids.append(f"startup_{idx}")

    # Use smaller batches to avoid memory issues with embedding generation
    batch_size = 500
    total_added = 0
    total_batches = (len(documents) + batch_size - 1) // batch_size

    print(f"[Competitor Agent] Starting embedding + insertion ({total_batches} batches of {batch_size})...")
    sys.stdout.flush()

    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i : i + batch_size]
        batch_meta = metadatas[i : i + batch_size]
        batch_ids = ids[i : i + batch_size]

        try:
            collection.upsert(documents=batch_docs, metadatas=batch_meta, ids=batch_ids)
            total_added += len(batch_docs)
            batch_num = i // batch_size + 1
            print(
                f"[Competitor Agent] Batch {batch_num}/{total_batches}: "
                f"{total_added}/{len(documents)} startups added"
            )
            sys.stdout.flush()
        except Exception as e:
            print(f"[Competitor Agent] ERROR on batch {i // batch_size + 1}: {e}")
            sys.stdout.flush()

    print(
        f"[Competitor Agent] Successfully loaded {total_added} startups into the Vector Database!"
    )


def find_competitors(idea_data: dict, n_results: int = 5) -> dict:
    """
    Takes structured output from Agent 1 (Idea Agent).
    Searches the vector database for similar startups.

    Returns:
      - competitors: list of matching startups with details
      - competition_score: 0-10 based on similarity and status of matches
    """
    print("[Agent 2 - Competitor Agent] Searching local database...")

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
        print(
            "[Agent 2 - Competitor Agent] Run 'python -c \"from backend.agents.competitor_agent import load_csv_to_database; load_csv_to_database()\"' to load data."
        )
        return {"competitors": [], "competition_score": 0}

    # Search the database for similar startups
    results = collection.query(
        query_texts=[search_query], n_results=min(n_results, count)
    )

    # Extract competitor data
    competitors = []
    if results["documents"] and results["documents"][0]:
        for i in range(len(results["documents"][0])):
            meta = results["metadatas"][0][i]
            distance = results["distances"][0][i]

            competitors.append(
                {
                    "competitor_name": meta["name"],
                    "market": meta["market"],
                    "status": meta["status"],
                    "funding": meta.get("funding", "0"),
                    "similarity_distance": round(distance, 4),
                }
            )

    # ─── Calculate Competition Score ───
    # Score is based on:
    #   1. How similar the competitors are (distance)
    #   2. How many are still operating (active competition)
    if competitors:
        avg_distance = sum(c["similarity_distance"] for c in competitors) / len(
            competitors
        )

        # Count how many competitors are still operating
        operating_count = sum(
            1 for c in competitors if c["status"] in ["operating", "active"]
        )
        operating_ratio = operating_count / len(competitors)

        # Base score from similarity: lower distance = higher competition
        # ChromaDB L2 distances typically range from 0.3 (very similar) to 2.0 (very different)
        similarity_score = max(0, min(10, round(10 - (avg_distance * 4))))

        # Adjust based on how many competitors are still active
        # More active competitors = higher competition
        competition_score = round(similarity_score * (0.5 + 0.5 * operating_ratio))
        competition_score = max(0, min(10, competition_score))
    else:
        competition_score = 0

    print(
        f"[Agent 2 - Competitor Agent] Found {len(competitors)} competitors. "
        f"Competition Score: {competition_score}/10"
    )

    return {"competitors": competitors, "competition_score": competition_score}


if __name__ == "__main__":
    # ─── Standalone: Load cleaned CSV and run a test search ───
    print("=" * 60)
    print("COMPETITOR AGENT - DATABASE SETUP & TEST")
    print(f"  PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"  DB_PATH:      {DB_PATH}")
    print(f"  CSV_PATH:     {CLEANED_CSV_PATH}")
    print("=" * 60)

    # Load the cleaned dataset into ChromaDB
    load_csv_to_database()

    # Test with a sample query
    fake_idea_output = {
        "industry": "HealthTech",
        "target_market": "Elderly patients in rural areas",
        "core_proposition": "Telemedicine video calls connecting rural patients with city doctors.",
        "keywords": ["telemedicine", "healthcare", "rural", "video consultation"],
    }

    result = find_competitors(fake_idea_output)
    print("\n--- COMPETITORS FOUND ---")
    for match in result["competitors"]:
        print(
            f"  - {match['competitor_name']} | "
            f"Market: {match['market']} | "
            f"Status: {match['status']} | "
            f"Distance: {match['similarity_distance']}"
        )
    print(f"\nCompetition Score: {result['competition_score']}/10")
