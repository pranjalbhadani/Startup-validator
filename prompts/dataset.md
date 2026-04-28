You are tasked with setting up a scalable and well-organized data repository for a startup idea validation system.

## Objective

Create a logical folder structure to store multiple startup-related datasets from different sources. The structure must support easy data ingestion, preprocessing, and future expansion.

## Data Sources to Accommodate

The repository should handle datasets similar to those from:

* Crunchbase (or its free alternatives)
* PitchBook (or alternatives)
* CB Insights (or alternatives)
* AngelList (or alternatives)
* Y Combinator datasets
* Kaggle datasets
* GitHub datasets
* Product Hunt datasets
* World Bank Open Data / macro datasets

## Requirements

### 1. Folder Structure

Design a modular folder hierarchy with clear separation of concerns. Include (but do not limit to):

* `data/`

  * `raw/` → original untouched datasets
  * `external/` → third-party structured datasets
  * `interim/` → cleaned but not fully processed data
  * `processed/` → final datasets ready for modeling
* Subfolders inside `raw/` or `external/` grouped by source:

  * `crunchbase/`
  * `pitchbook/`
  * `cb_insights/`
  * `angellist/`
  * `ycombinator/`
  * `kaggle/`
  * `github/`
  * `product_hunt/`
  * `macro/`
* `schemas/` → data schemas and field mappings
* `notebooks/` → exploratory analysis
* `scripts/` → ingestion and preprocessing scripts
* `logs/` → pipeline logs
* `tests/` → data validation tests

### 2. Naming Conventions

* Use lowercase and underscores for folder/file names
* Include timestamps or versioning where appropriate
* Ensure dataset names are descriptive and consistent

### 3. README.md

Generate a comprehensive `README.md` file at the root level that includes:

* Overview of the project
* Explanation of the folder structure
* Description of each data source category
* Data flow explanation (raw → interim → processed)
* Instructions for adding new datasets
* Naming conventions and best practices

### 4. Output Format

* Provide the folder structure as a tree diagram
* Include example placeholder files where helpful
* Provide the full contents of the `README.md`

### 5. Design Principles

* Scalability (easy to add new datasets)
* Clarity (self-explanatory structure)
* Reusability (modular design)
* Compatibility with data pipelines and ML workflows

## Deliverables

1. Complete folder structure (tree format)
2. Example file placements
3. Full `README.md` content

Ensure the structure is practical, not overly complex, and aligned with real-world data engineering practices.
