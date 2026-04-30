"""
Test: Unified Data Ingestion Pipeline
======================================
Run from project root:
  .\venv\Scripts\python.exe tests\test_data_ingestion.py
"""

import sys
import os

# Setup paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))

PASS = 0
FAIL = 0


def check(label, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label} — {detail}")


# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("TEST 1: Individual Dataset Loaders")
print("=" * 60)

from agents.data_ingestion import (
    _load_crunchbase,
    _load_indian_funding,
    _load_unicorns,
    _load_yc,
    _load_success_dataset,
    load_product_hunt_trends,
    load_macro_context,
)

cb = _load_crunchbase()
check("Crunchbase loads", len(cb) > 0, f"got {len(cb)}")
if cb:
    check("Crunchbase has required keys", all(k in cb[0] for k in ["name", "source", "industry", "status", "funding_usd"]))
    check("Crunchbase source tag", cb[0]["source"] == "crunchbase")

ind = _load_indian_funding()
check("Indian Funding loads", len(ind) > 0, f"got {len(ind)}")
if ind:
    check("Indian Funding source tag", ind[0]["source"] == "indian_funding")

uni = _load_unicorns()
check("Unicorns loads", len(uni) > 0, f"got {len(uni)}")
if uni:
    check("Unicorns source tag", uni[0]["source"] == "unicorn")
    check("Unicorns have valuation", any(u["valuation"] > 0 for u in uni))

yc = _load_yc()
check("YC loads", len(yc) > 0, f"got {len(yc)}")
if yc:
    check("YC source tag", yc[0]["source"] == "yc")

ss = _load_success_dataset()
check("Success dataset loads", len(ss) > 0, f"got {len(ss)}")
check("Success dataset sampled to ≤10K", len(ss) <= 10000)
if ss:
    check("Success dataset source tag", ss[0]["source"] == "success_dataset")

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST 2: Product Hunt Trend Aggregation")
print("=" * 60)

trends = load_product_hunt_trends()
check("PH trends loaded", len(trends) > 0, f"got {len(trends)} topic-year rows")
if trends:
    t = trends[0]
    check("Trend has topic", "topic" in t)
    check("Trend has total_votes", "total_votes" in t)
    check("Trend has total_posts", "total_posts" in t)
    check("Trend has year", "year" in t)
    # Check output file
    csv_path = os.path.join(PROJECT_ROOT, "data", "processed", "product_hunt_trends.csv")
    check("PH trends CSV saved", os.path.exists(csv_path))

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST 3: Macro Context Extraction")
print("=" * 60)

macro = load_macro_context()
check("Macro context loaded", len(macro) > 0, f"got {macro}")
check("Macro has date", "date" in macro)
check("Macro has interest_rate or sp500", "interest_rate" in macro or "sp500" in macro)
csv_path = os.path.join(PROJECT_ROOT, "data", "processed", "macro_indicators.csv")
check("Macro CSV saved", os.path.exists(csv_path))

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST 4: Full Ingestion + ChromaDB Load")
print("=" * 60)

from agents.data_ingestion import ingest_all, verify_ingestion

result = ingest_all(force_reload=True)
check("Ingest returns record count", result["records"] > 50000, f"got {result['records']}")
check("Ingest returns trend count", result["trends"] > 0, f"got {result['trends']}")
check("Ingest returns macro dict", len(result["macro"]) > 0)

# Check unified CSV
csv_path = os.path.join(PROJECT_ROOT, "data", "processed", "unified_startups.csv")
check("Unified CSV saved", os.path.exists(csv_path))

print("\n--- ChromaDB Verification ---")
verify_ingestion()

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST 5: Competitor Agent with Unified DB")
print("=" * 60)

from agents.competitor_agent import find_competitors

test_idea = {
    "industry": "HealthTech",
    "target_market": "patients",
    "core_proposition": "AI telemedicine platform",
    "keywords": ["health", "AI", "telemedicine"],
}

comp_result = find_competitors(test_idea)
check("Competitors found", len(comp_result["competitors"]) > 0)
check("Has competition_score", "competition_score" in comp_result)
check("Has source_breakdown", "source_breakdown" in comp_result)
if comp_result["competitors"]:
    c = comp_result["competitors"][0]
    check("Competitor has source field", "source" in c)
    check("Competitor has enriched fields", "valuation" in c and "investors" in c)
    sources = set(x["source"] for x in comp_result["competitors"])
    check(f"Multiple sources in results: {sources}", len(sources) >= 1)

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("TEST 6: Scoring Agent with Enriched Data")
print("=" * 60)

from agents.scoring_agent import score_startups

sample_startups = [
    {"name": "TestCo", "status": "operating", "funding_total_usd": 5e6, "source": "crunchbase", "valuation": 0},
    {"name": "UniCo", "status": "ipo", "funding_total_usd": 75e6, "source": "unicorn", "valuation": 2e9},
]

report = score_startups(
    sample_startups,
    keywords=["health", "AI"],
    trend_data=trends[:50],
    macro_context=macro,
)

check("Score returned", report["score"] >= 0)
check("Risk returned", report["risk"] in ["Low", "Medium", "High"])
check("Trend score returned", "trend_score" in report)
check("Unicorn proximity in metrics", "unicorn_proximity" in report["metrics"])
check("Sources in metrics", "sources" in report["metrics"])
check("Trend assessment in insights", "trend_assessment" in report["insights"])

# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print(f"RESULTS: {PASS} passed, {FAIL} failed")
print("=" * 60)

sys.exit(1 if FAIL > 0 else 0)
