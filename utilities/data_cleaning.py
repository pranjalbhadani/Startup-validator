"""
Data Cleaning Script
Cleans the raw investments_VC_dataset.csv and saves a cleaned version
for the Competitor Similarity Agent to use.
"""

import os
import pandas as pd

# ─── Paths ───
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..")
RAW_CSV = os.path.join(PROJECT_ROOT, "data", "raw", "kaggle", "investments_VC_dataset.csv")
CLEAN_CSV = os.path.join(PROJECT_ROOT, "data", "processed", "cleaned_investments_sent.csv")

# 1. Load the raw data
print(f"Loading raw data from: {RAW_CSV}")
data = pd.read_csv(RAW_CSV, encoding="latin-1")
print(f"Raw data size: {data.shape}")

# 2. Strip hidden whitespace from column names
data.columns = data.columns.str.strip()

# 3. Select ONLY the columns the validation system needs
columns_to_keep = [
    "permalink",  # Unique ID for the vector database
    "name",  # Startup name
    "market",  # The industry/niche
    "status",  # operating, acquired, closed (crucial for Risk Agent)
    "funding_total_usd",  # Good proxy for traction/scale
]

df_clean = data[columns_to_keep].copy()

# 4. Drop rows where the most critical data is missing
# The system can't compare startups if name or market is blank
df_clean = df_clean.dropna(subset=["name", "market", "status"])

# 5. Remove duplicate startups (keep first occurrence)
df_clean = df_clean.drop_duplicates(subset=["name"], keep="first")

# 6. Standardize the text (makes NLP matching much easier)
df_clean["market"] = df_clean["market"].str.strip().str.lower()
df_clean["name"] = df_clean["name"].str.strip()
df_clean["status"] = df_clean["status"].str.strip().str.lower()

# 7. Clean funding column — convert to numeric, fill missing with 0
df_clean["funding_total_usd"] = (
    pd.to_numeric(df_clean["funding_total_usd"], errors="coerce").fillna(0).astype(int)
)

# 8. Reset index for clean IDs
df_clean = df_clean.reset_index(drop=True)

print("\nData cleaning complete!")
print(df_clean.head(10))
print(f"\nFinal cleaned data size: {df_clean.shape}")
print(f"Unique markets: {df_clean['market'].nunique()}")
print(f"Status distribution:\n{df_clean['status'].value_counts()}")

# 9. Save the cleaned data
df_clean.to_csv(CLEAN_CSV, index=False)
print(f"\nSaved cleaned data to: {CLEAN_CSV}")
