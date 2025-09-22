# Seattle Mariners Player Analytics

Analytical toolkit to evaluate Seattle Mariners player performance over multiple seasons using public baseball data.
The repository includes repeatable pipelines for data collection (`pybaseball`), cleaning, feature generation, and
reporting (dashboards and notebooks).

## Objectives
- Build a reproducible pipeline to pull Mariners player stats across seasons.
- Clean and standardize datasets for hitters and pitchers.
- Engineer value/impact metrics (e.g., WAR components, plate discipline, run prevention indicators).
- Create dashboards and reports for roster decisions and player development insights.

## Contents
```
seattle-mariners-player-analytics/
├─ data/                # Do NOT commit large raw data; .gitignore protects this folder
├─ notebooks/           # Exploratory & reporting notebooks
├─ src/                 # Library code (ETL, features, viz, models)
├─ scripts/             # CLI entry points to run pipelines locally
├─ dashboards/          # Power BI / Tableau workbooks
├─ reports/             # Generated figures/tables for write-ups
└─ tests/               # Unit tests for core transformations
```

## Data Sources
- [`pybaseball`](https://github.com/jldbc/pybaseball) for MLB statistics and Statcast data.
- Lahman and FanGraphs-derived metrics where license allows (user pulls locally).

## Quickstart

### 1) Environment
```bash
# Option A: pip
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Option B: conda (optional)
conda env create -f environment.yml
conda activate mariners
```

### 2) Pull Mariners data
```bash
# Example: 2019–2024, team 'SEA'
python scripts/pull_data.py --start 2019 --end 2024 --team SEA
```

### 3) Build features and tables
```bash
python scripts/build_features.py
```

### 4) Generate figures
```bash
python scripts/make_figures.py
```

### 5) Open notebooks
Use the templates in `notebooks/` for EDA and reporting.

## Project Conventions
- Python >= 3.10
- Black + Ruff for formatting/linting
- Unit tests with pytest
- Data files larger than ~50MB remain local; do not push them to Git.

## License
MIT © 2025


## End-to-End Pipeline

```bash
# Pull, build, figures, and value tables
python scripts/run_pipeline.py --start 2019 --end 2024 --team SEA
```

Outputs:
- Processed features → `data/processed/`
- Figures → `reports/figures/`
- Tables (rankings) → `reports/tables/`

## Statcast (Optional)

A helper is provided at `src/data/statcast_loader.py` to fetch Statcast pitch-level data by season window and filter to Mariners home/away games. This is heavier data; keep files local (in `data/raw/`) and avoid committing them.
