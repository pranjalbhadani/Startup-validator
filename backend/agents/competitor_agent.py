"""
Agent 3: Competitor Similarity Agent
Searches a local ChromaDB vector database (built from cleaned CSV data)
to find similar startups. Returns a list of competitors and a competition_score.
"""

import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

# ─── Paths (relative to this file → MVP/agents/) ───
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
MVP_DIR = os.path.join(AGENT_DIR, "..")
DB_PATH = os.path.join(MVP_DIR, "startup_vectordb")

# Path to the CLEANED CSV (output of utilities/data_cleaning.py)
CLEANED_CSV_PATH = os.path.join(
    MVP_DIR, "..", "data", "datasets", "cleaned_investments_sent.csv"
)

# Initialize the local ChromaDB vector database
chroma_client = chromadb.PersistentClient(path=DB_PATH)
sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()

# Create or open the database collection
collection = chroma_client.get_or_create_collection(
    name="crunchbase_startups", embedding_function=sentence_transformer_ef
)


def load_csv_to_database(csv_file_path: str = None):
    """
    Load the cleaned CSV into ChromaDB vector database.
    Uses the cleaned CSV by default (from data/datasets/cleaned_investments.csv).
    Run this ONCE to populate the database.
    """
    if csv_file_path is None:
        csv_file_path = CLEANED_CSV_PATH

    print(f"[Competitor Agent] Loading cleaned CSV from: {csv_file_path}")

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
        ids.append(str(idx))

    batch_size = 5000
    total_added = 0

    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i : i + batch_size]
        batch_meta = metadatas[i : i + batch_size]
        batch_ids = ids[i : i + batch_size]

        collection.add(documents=batch_docs, metadatas=batch_meta, ids=batch_ids)
        total_added += len(batch_docs)
        print(
            f"[Competitor Agent] Added batch {i // batch_size + 1}: {total_added}/{len(documents)} startups"
        )

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
    print("[Agent 3 - Competitor Agent] Searching local database...")

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
        print("[Agent 3 - Competitor Agent] WARNING: Database is empty!")
        print(
            "[Agent 3 - Competitor Agent] Run 'python agents/competitor_agent.py' to load data."
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
        f"[Agent 3 - Competitor Agent] Found {len(competitors)} competitors. "
        f"Competition Score: {competition_score}/10"
    )

    return {"competitors": competitors, "competition_score": competition_score}


if __name__ == "__main__":
    # ─── Standalone: Load cleaned CSV and run a test search ───
    print("=" * 60)
    print("COMPETITOR AGENT - DATABASE SETUP & TEST")
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
