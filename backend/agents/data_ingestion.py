"""
Unified Data Ingestion Module
==============================
Loads, normalizes, and indexes all datasets into ChromaDB.

Datasets handled:
  1. Crunchbase (cleaned_investments_sent.csv)      — 44K startups
  2. Indian Startup Funding 2020-2025                — 1.1K entries
  3. Unicorn Companies                               — 1K companies
  4. Product Hunt 2023 + 2024                        — 76K posts → aggregated trends
  5. Macroeconomics (ie_data.csv)                    — time-series → latest context dict
  6. YC Startups Directory                           — 688 companies
  7. Startup Success Dataset                         — 100K entries (sampled)

Design:
  - All startup-level data goes into ONE ChromaDB collection ("unified_startups")
  - Product Hunt data is aggregated into topic-level trends (saved as CSV + in-memory)
  - Macro data is extracted as a context dict (latest values only)
"""

import os
import sys
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

# ─── Paths ───────────────────────────────────────────────────────────────────
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(AGENT_DIR, "..")
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))

RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "startup_vectordb")

# Dataset file paths
PATHS = {
    "crunchbase": os.path.join(PROCESSED_DIR, "cleaned_investments_sent.csv"),
    "indian_funding": os.path.join(RAW_DIR, "indian startup funding 20-25", "indian_startup_funding_2020_2025_sample.csv"),
    "unicorn": os.path.join(RAW_DIR, "unicorn high growth startup data", "Unicorn_Companies.csv"),
    "ph_2023": os.path.join(RAW_DIR, "product launch trend data product hunt", "posts_2023.csv"),
    "ph_2024": os.path.join(RAW_DIR, "product launch trend data product hunt", "posts_2024.csv"),
    "macro": os.path.join(RAW_DIR, "macroeconomics data", "ie_data.csv"),
    "yc": os.path.join(RAW_DIR, "Startups directory yc.csv"),
    "success": os.path.join(RAW_DIR, "startup_success_dataset.csv"),
}

# Maximum rows to sample from very large datasets
SUCCESS_SAMPLE_SIZE = 10000


# ═══════════════════════════════════════════════════════════════════════════════
# LOADERS — each returns a list of dicts with the unified schema
# ═══════════════════════════════════════════════════════════════════════════════

def _load_crunchbase() -> list[dict]:
    """Load existing cleaned Crunchbase/Kaggle VC dataset."""
    path = PATHS["crunchbase"]
    if not os.path.exists(path):
        print(f"[Ingestion] SKIP crunchbase — file not found: {path}")
        return []

    df = pd.read_csv(path, encoding="latin-1")
    df = df.dropna(subset=["name", "market", "status"])

    records = []
    for _, row in df.iterrows():
        funding_raw = str(row.get("funding_total_usd", "0")).replace(",", "").strip()
        try:
            funding = float(funding_raw)
        except (ValueError, TypeError):
            funding = 0.0

        records.append({
            "name": str(row["name"]).strip(),
            "source": "crunchbase",
            "industry": str(row["market"]).strip().lower(),
            "status": str(row["status"]).strip().lower(),
            "funding_usd": max(funding, 0.0),
            "city": "",
            "country": "",
            "description": "",
            "investors": "",
            "year_founded": 0,
            "valuation": 0.0,
            "topics": "",
            "outcome": "",
            "team_size": 0,
            "market_size_billion": 0.0,
        })

    print(f"[Ingestion] crunchbase: {len(records)} records loaded")
    return records


def _load_indian_funding() -> list[dict]:
    """Load Indian Startup Funding 2020-2025 dataset."""
    path = PATHS["indian_funding"]
    if not os.path.exists(path):
        print(f"[Ingestion] SKIP indian_funding — file not found: {path}")
        return []

    df = pd.read_csv(path)
    df = df.dropna(subset=["Startup", "Industry"])

    records = []
    for _, row in df.iterrows():
        try:
            funding = float(str(row.get("InvestmentAmount_USD", "0")).replace(",", "").strip())
        except (ValueError, TypeError):
            funding = 0.0

        records.append({
            "name": str(row["Startup"]).strip(),
            "source": "indian_funding",
            "industry": str(row.get("Industry", "")).strip().lower(),
            "status": "operating",  # dataset only has funded startups
            "funding_usd": max(funding, 0.0),
            "city": str(row.get("City", "")).strip(),
            "country": "India",
            "description": f"{row.get('SubVertical', '')} startup in {row.get('Industry', '')}",
            "investors": str(row.get("Investors", "")).strip(),
            "year_founded": 0,
            "valuation": 0.0,
            "topics": str(row.get("SubVertical", "")).strip().lower(),
            "outcome": str(row.get("InvestmentType", "")).strip().lower(),
            "team_size": 0,
            "market_size_billion": 0.0,
        })

    print(f"[Ingestion] indian_funding: {len(records)} records loaded")
    return records


def _load_unicorns() -> list[dict]:
    """Load Unicorn Companies dataset."""
    path = PATHS["unicorn"]
    if not os.path.exists(path):
        print(f"[Ingestion] SKIP unicorn — file not found: {path}")
        return []

    df = pd.read_csv(path)
    df = df.dropna(subset=["Company", "Industry"])

    records = []
    for _, row in df.iterrows():
        # Parse valuation like "$180B" or "$95B"
        val_str = str(row.get("Valuation", "$0")).replace("$", "").replace(",", "").strip()
        try:
            if val_str.upper().endswith("B"):
                valuation = float(val_str[:-1]) * 1e9
            elif val_str.upper().endswith("M"):
                valuation = float(val_str[:-1]) * 1e6
            else:
                valuation = float(val_str)
        except (ValueError, TypeError):
            valuation = 0.0

        # Parse funding
        fund_str = str(row.get("Funding", "$0")).replace("$", "").replace(",", "").strip()
        try:
            if fund_str.upper().endswith("B"):
                funding = float(fund_str[:-1]) * 1e9
            elif fund_str.upper().endswith("M"):
                funding = float(fund_str[:-1]) * 1e6
            else:
                funding = float(fund_str)
        except (ValueError, TypeError):
            funding = 0.0

        try:
            year_founded = int(row.get("Year Founded", 0))
        except (ValueError, TypeError):
            year_founded = 0

        records.append({
            "name": str(row["Company"]).strip(),
            "source": "unicorn",
            "industry": str(row.get("Industry", "")).strip().lower(),
            "status": "operating",
            "funding_usd": max(funding, 0.0),
            "city": str(row.get("City", "")).strip(),
            "country": str(row.get("Country", "")).strip(),
            "description": f"Unicorn company in {row.get('Industry', '')} valued at {row.get('Valuation', 'N/A')}",
            "investors": str(row.get("Select Investors", "")).strip(),
            "year_founded": year_founded,
            "valuation": max(valuation, 0.0),
            "topics": str(row.get("Industry", "")).strip().lower(),
            "outcome": "unicorn",
            "team_size": 0,
            "market_size_billion": 0.0,
        })

    print(f"[Ingestion] unicorn: {len(records)} records loaded")
    return records


def _load_yc() -> list[dict]:
    """Load YC Startups Directory."""
    path = PATHS["yc"]
    if not os.path.exists(path):
        print(f"[Ingestion] SKIP yc — file not found: {path}")
        return []

    df = pd.read_csv(path, encoding="latin-1")
    df = df.dropna(subset=["Company"])

    records = []
    for _, row in df.iterrows():
        status_raw = str(row.get("Satus", "Unknown")).strip().lower()
        status = "operating" if status_raw in ("operating", "") else status_raw.replace("exited", "acquired")

        # Parse funding amounts (comma-separated list like "$1200000, undisclosed amount")
        amounts_str = str(row.get("Amounts raised in different funding rounds", "0"))
        total_funding = 0.0
        for amt in amounts_str.split(","):
            cleaned = amt.replace("$", "").replace(",", "").strip()
            if cleaned and cleaned != "undisclosed amount" and cleaned != "nan":
                try:
                    total_funding += float(cleaned)
                except (ValueError, TypeError):
                    pass

        try:
            year_founded = int(row.get("Year Founded", 0))
        except (ValueError, TypeError):
            year_founded = 0

        records.append({
            "name": str(row["Company"]).strip(),
            "source": "yc",
            "industry": str(row.get("Categories", "")).strip().lower(),
            "status": status,
            "funding_usd": max(total_funding, 0.0),
            "city": str(row.get("Headquarters (City)", "")).strip(),
            "country": str(row.get("Headquarters (Country)", "")).strip(),
            "description": str(row.get("Description", "")).strip(),
            "investors": str(row.get("Investors", "")).strip(),
            "year_founded": year_founded,
            "valuation": 0.0,
            "topics": str(row.get("Categories", "")).strip().lower(),
            "outcome": status,
            "team_size": 0,
            "market_size_billion": 0.0,
        })

    print(f"[Ingestion] yc: {len(records)} records loaded")
    return records


def _load_success_dataset() -> list[dict]:
    """Load Startup Success/Failure dataset (sampled)."""
    path = PATHS["success"]
    if not os.path.exists(path):
        print(f"[Ingestion] SKIP success — file not found: {path}")
        return []

    df = pd.read_csv(path)

    # Sample to keep ingestion fast
    if len(df) > SUCCESS_SAMPLE_SIZE:
        df = df.sample(n=SUCCESS_SAMPLE_SIZE, random_state=42)

    records = []
    for _, row in df.iterrows():
        outcome = str(row.get("outcome", "")).strip()
        status_map = {"IPO": "ipo", "Acquisition": "acquired", "Failure": "closed", "Success": "operating"}
        status = status_map.get(outcome, "unknown")

        try:
            funding = float(row.get("revenue_million", 0)) * 1e6  # rough proxy
        except (ValueError, TypeError):
            funding = 0.0

        try:
            team_size = int(row.get("team_size", 0))
        except (ValueError, TypeError):
            team_size = 0

        try:
            market_size = float(row.get("market_size_billion", 0))
        except (ValueError, TypeError):
            market_size = 0.0

        sector = str(row.get("sector", "unknown")).strip().lower()

        records.append({
            "name": f"{sector}_startup_{_}",
            "source": "success_dataset",
            "industry": sector,
            "status": status,
            "funding_usd": max(funding, 0.0),
            "city": "",
            "country": "",
            "description": f"{sector} startup with {team_size} team, {row.get('funding_rounds', 0)} funding rounds, outcome: {outcome}",
            "investors": str(row.get("investor_type", "")).strip(),
            "year_founded": 0,
            "valuation": 0.0,
            "topics": sector,
            "outcome": outcome.lower() if outcome else "",
            "team_size": team_size,
            "market_size_billion": market_size,
        })

    print(f"[Ingestion] success_dataset: {len(records)} records loaded (sampled from 100K)")
    return records


# ═══════════════════════════════════════════════════════════════════════════════
# PRODUCT HUNT — Aggregated topic-level trend summaries
# ═══════════════════════════════════════════════════════════════════════════════

def load_product_hunt_trends() -> list[dict]:
    """
    Aggregate Product Hunt 2023+2024 data into topic-level trend summaries.

    Returns a list of dicts:
      { topic, total_posts, total_votes, avg_votes, year, top_products }
    """
    frames = []
    for key, year in [("ph_2023", 2023), ("ph_2024", 2024)]:
        path = PATHS[key]
        if not os.path.exists(path):
            print(f"[Ingestion] SKIP {key} — file not found: {path}")
            continue
        df = pd.read_csv(path)
        df["year"] = year
        frames.append(df)

    if not frames:
        return []

    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(subset=["topics"])

    # Explode topics (comma-separated) into individual rows
    df["topics_list"] = df["topics"].str.split(",")
    exploded = df.explode("topics_list")
    exploded["topic"] = exploded["topics_list"].str.strip().str.lower()
    exploded = exploded[exploded["topic"] != ""]

    # Aggregate by topic + year
    trends = exploded.groupby(["topic", "year"]).agg(
        total_posts=("name", "count"),
        total_votes=("votesCount", "sum"),
        avg_votes=("votesCount", "mean"),
    ).reset_index()

    trends["avg_votes"] = trends["avg_votes"].round(1)

    # Get top 3 products per topic (by votes)
    top_products = (
        exploded.sort_values("votesCount", ascending=False)
        .groupby(["topic", "year"])
        .head(3)
        .groupby(["topic", "year"])["name"]
        .apply(lambda x: "; ".join(x.tolist()))
        .reset_index()
        .rename(columns={"name": "top_products"})
    )

    trends = trends.merge(top_products, on=["topic", "year"], how="left")

    records = trends.to_dict("records")
    print(f"[Ingestion] product_hunt_trends: {len(records)} topic-year aggregations")

    # Save to processed/
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    trends.to_csv(os.path.join(PROCESSED_DIR, "product_hunt_trends.csv"), index=False)

    return records


# ═══════════════════════════════════════════════════════════════════════════════
# MACRO INDICATORS — Latest values as context dict
# ═══════════════════════════════════════════════════════════════════════════════

def load_macro_context() -> dict:
    """
    Extract latest macroeconomic indicators from ie_data.csv.

    Returns a dict with:
      { date, sp500, cpi, interest_rate, cape_ratio }
    """
    path = PATHS["macro"]
    if not os.path.exists(path):
        print(f"[Ingestion] SKIP macro — file not found: {path}")
        return {}

    df = pd.read_csv(path, header=0)
    # The CSV has the header in row 0, then some empty rows, then data starting around row 7
    # Columns: Date, S&P Comp., Dividend, Earnings, Consumer Price Index CPI, ..., Long Interest Rate GS10, ...
    # Rename to clean names
    col_map = {}
    for c in df.columns:
        cl = c.strip().lower()
        if cl == "date":
            col_map[c] = "date"
        elif "s&p" in cl or "s&p" in cl:
            col_map[c] = "sp500"
        elif "consumer price" in cl or "cpi" in cl:
            col_map[c] = "cpi"
        elif "long interest" in cl or "gs10" in cl:
            col_map[c] = "interest_rate"
        elif "cape" in cl and "total return" not in cl and "excess" not in cl:
            col_map[c] = "cape_ratio"

    df = df.rename(columns=col_map)

    # Keep only the columns we care about
    keep = [c for c in ["date", "sp500", "cpi", "interest_rate", "cape_ratio"] if c in df.columns]
    if not keep:
        print("[Ingestion] macro: could not identify columns")
        return {}

    df = df[keep].dropna(subset=["date"])
    df = df[df["date"].apply(lambda x: str(x).replace(".", "").replace(" ", "").isdigit() or "." in str(x))]

    # Convert to numeric
    for c in keep:
        if c != "date":
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(how="all", subset=[c for c in keep if c != "date"])

    if df.empty:
        print("[Ingestion] macro: no valid data rows found")
        return {}

    # Get the latest row
    latest = df.iloc[-1].to_dict()

    # Clean up
    context = {}
    for k, v in latest.items():
        if pd.notna(v):
            context[k] = round(float(v), 4) if k != "date" else str(v)

    # Save to processed/
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df.to_csv(os.path.join(PROCESSED_DIR, "macro_indicators.csv"), index=False)

    print(f"[Ingestion] macro_context: {context}")
    return context


# ═══════════════════════════════════════════════════════════════════════════════
# UNIFIED STARTUP INGESTION — Merge all startup-level datasets
# ═══════════════════════════════════════════════════════════════════════════════

def _load_all_startups() -> list[dict]:
    """Load and merge all startup-level datasets."""
    all_records = []

    loaders = [
        _load_crunchbase,
        _load_indian_funding,
        _load_unicorns,
        _load_yc,
        _load_success_dataset,
    ]

    for loader in loaders:
        try:
            records = loader()
            all_records.extend(records)
        except Exception as e:
            print(f"[Ingestion] ERROR in {loader.__name__}: {e}")

    print(f"[Ingestion] Total unified startup records: {len(all_records)}")

    # Save unified CSV
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df = pd.DataFrame(all_records)
    df.to_csv(os.path.join(PROCESSED_DIR, "unified_startups.csv"), index=False)
    print(f"[Ingestion] Saved unified_startups.csv to {PROCESSED_DIR}")

    return all_records


def load_to_chromadb(records: list[dict] = None, force_reload: bool = False):
    """
    Load unified startup records into ChromaDB.

    Uses a single collection 'unified_startups' with rich metadata
    for filtering by source, industry, status, etc.
    """
    if records is None:
        records = _load_all_startups()

    if not records:
        print("[Ingestion] No records to load into ChromaDB.")
        return

    os.makedirs(DB_PATH, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    ef = embedding_functions.DefaultEmbeddingFunction()

    collection_name = "unified_startups"

    if force_reload:
        try:
            chroma_client.delete_collection(collection_name)
            print(f"[Ingestion] Deleted existing collection '{collection_name}'")
        except Exception:
            pass

    collection = chroma_client.get_or_create_collection(
        name=collection_name, embedding_function=ef
    )

    existing_count = collection.count()
    if existing_count >= len(records) * 0.9 and not force_reload:
        print(
            f"[Ingestion] Collection already has {existing_count} records "
            f"(target: {len(records)}). Skipping. Use force_reload=True to reload."
        )
        return

    print(f"[Ingestion] Loading {len(records)} records into ChromaDB...")
    sys.stdout.flush()

    documents = []
    metadatas = []
    ids = []

    for idx, rec in enumerate(records):
        # Build a rich searchable document
        parts = [rec["name"]]
        if rec.get("industry"):
            parts.append(f"industry: {rec['industry']}")
        if rec.get("description"):
            parts.append(rec["description"])
        if rec.get("topics"):
            parts.append(f"topics: {rec['topics']}")
        if rec.get("investors"):
            parts.append(f"investors: {rec['investors'][:200]}")

        doc = ". ".join(p for p in parts if p and p != "nan")

        # Metadata for filtering
        meta = {
            "name": str(rec.get("name", "Unknown"))[:500],
            "source": str(rec.get("source", "unknown")),
            "industry": str(rec.get("industry", ""))[:200],
            "status": str(rec.get("status", "unknown")),
            "funding_usd": str(rec.get("funding_usd", 0)),
            "country": str(rec.get("country", "")),
            "year_founded": str(rec.get("year_founded", 0)),
            "valuation": str(rec.get("valuation", 0)),
            "outcome": str(rec.get("outcome", "")),
        }

        documents.append(doc[:2000])  # ChromaDB doc length limit
        metadatas.append(meta)
        ids.append(f"unified_{idx}")

    # Batch upsert
    batch_size = 500
    total_batches = (len(documents) + batch_size - 1) // batch_size

    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i: i + batch_size]
        batch_meta = metadatas[i: i + batch_size]
        batch_ids = ids[i: i + batch_size]

        try:
            collection.upsert(documents=batch_docs, metadatas=batch_meta, ids=batch_ids)
            batch_num = i // batch_size + 1
            print(f"[Ingestion] Batch {batch_num}/{total_batches}: {min(i + batch_size, len(documents))}/{len(documents)}")
            sys.stdout.flush()
        except Exception as e:
            print(f"[Ingestion] ERROR on batch {i // batch_size + 1}: {e}")

    print(f"[Ingestion] Successfully loaded {len(documents)} records into ChromaDB!")


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

def ingest_all(force_reload: bool = False):
    """
    Run the full ingestion pipeline:
      1. Load and merge all startup datasets
      2. Load into ChromaDB
      3. Aggregate Product Hunt trends
      4. Extract macro context
    """
    print("=" * 60)
    print("UNIFIED DATA INGESTION — STARTING")
    print("=" * 60)

    # 1. Startup data → ChromaDB
    records = _load_all_startups()
    load_to_chromadb(records, force_reload=force_reload)

    # 2. Product Hunt trends
    trends = load_product_hunt_trends()

    # 3. Macro context
    macro = load_macro_context()

    print("\n" + "=" * 60)
    print("UNIFIED DATA INGESTION — COMPLETE")
    print(f"  Startups loaded: {len(records)}")
    print(f"  PH trend topics: {len(trends)}")
    print(f"  Macro context:   {len(macro)} indicators")
    print("=" * 60)

    return {"records": len(records), "trends": len(trends), "macro": macro}


def verify_ingestion():
    """Verify that ChromaDB has data from all expected sources."""
    os.makedirs(DB_PATH, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    ef = embedding_functions.DefaultEmbeddingFunction()

    try:
        collection = chroma_client.get_collection(
            name="unified_startups", embedding_function=ef
        )
    except Exception:
        print("[Verify] Collection 'unified_startups' not found. Run ingest_all() first.")
        return

    total = collection.count()
    print(f"[Verify] Total records in ChromaDB: {total}")

    # Check source distribution
    for source in ["crunchbase", "indian_funding", "unicorn", "yc", "success_dataset"]:
        try:
            result = collection.get(where={"source": source}, limit=1)
            count_msg = f"present (sample: {result['metadatas'][0]['name'] if result['metadatas'] else 'N/A'})"
        except Exception:
            count_msg = "NOT FOUND"
        print(f"  {source}: {count_msg}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Unified Data Ingestion")
    parser.add_argument("--force", action="store_true", help="Force reload (delete existing ChromaDB data)")
    parser.add_argument("--verify", action="store_true", help="Verify ingestion only")
    args = parser.parse_args()

    if args.verify:
        verify_ingestion()
    else:
        ingest_all(force_reload=args.force)
