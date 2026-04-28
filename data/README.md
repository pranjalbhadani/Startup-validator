# Startup Validator Data Repository

## Overview
This repository contains the structured datasets and processing logic for the Venture Validator pipeline. It is designed to accommodate multiple startup-related data sources, providing a scalable structure for ingestion, cleaning, and downstream machine learning and evaluation processes.

## Folder Structure

```
data/
├── raw/               # Original untouched datasets
│   ├── angellist/
│   ├── cb_insights/
│   ├── crunchbase/
│   ├── github/
│   ├── kaggle/
│   ├── macro/
│   ├── pitchbook/
│   ├── product_hunt/
│   └── ycombinator/
├── external/          # Third-party structured datasets
├── interim/           # Cleaned but not fully processed data
├── processed/         # Final datasets ready for modeling
├── schemas/           # Data schemas and field mappings
├── notebooks/         # Exploratory analysis
├── scripts/           # Ingestion and preprocessing scripts
├── logs/              # Pipeline logs
└── tests/             # Data validation tests
```

## Data Source Categories (raw/)
- **crunchbase/**: Startups, funding rounds, and investor data from Crunchbase.
- **pitchbook/**: Deep-dive financial and VC deal data.
- **cb_insights/**: Trend data and tech market intelligence.
- **angellist/**: Early-stage startup listings and job-related data.
- **ycombinator/**: Data on YC alumni companies.
- **kaggle/**: Community-sourced datasets (e.g., general VC investments).
- **github/**: Repositories and developer activity related to startups.
- **product_hunt/**: Launch data, upvotes, and product reception.
- **macro/**: World Bank, economic, and industry-level datasets.

## Data Flow
1. **Raw**: Downloaded files are placed directly in their respective subfolders within `raw/` (e.g., `raw/kaggle/`). These files are *never* modified.
2. **Interim**: Scripts clean the raw data (handling nulls, standardizing formats, etc.) and save the intermediate results to `interim/`.
3. **Processed**: The interim data is transformed into final, model-ready features (e.g., sentiment scores, normalized vectors) and stored in `processed/`.

## Instructions for Adding New Datasets
1. Determine the source of the dataset and place the untouched file in `data/raw/<source_name>/`.
2. Ensure the filename uses lowercase and underscores (e.g., `yc_companies_2023.csv`).
3. If necessary, create a schema mapping in `schemas/`.
4. Write or update a preprocessing script in `scripts/` to handle the data transformation.
5. Save the cleaned output to `interim/` and the final feature-ready dataset to `processed/`.

## Naming Conventions
- Use `lowercase` and `underscores` for all folder and file names (e.g., `market_trends_2023.csv`).
- Include timestamps or version numbers where appropriate (e.g., `v1`, `202310`).
- Ensure names are descriptive enough to immediately indicate the file's content and source.
