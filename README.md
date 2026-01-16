# Sales Performance Dashboard (Superstore)

This project analyzes real retail order data (Tableau Sample Superstore) to answer business questions about revenue, profitability, growth, regional performance, discount strategy, and shipping impact.

## Repository contents
- `data/raw/superstore.csv` Raw dataset
- `data/processed/superstore_cleaned.csv` Cleaned dataset (Tableau and Dash ready)
- `data/processed/profiling_summary.txt` Basic data profiling output
- `etl/clean_superstore.py` Cleaning + validation script
- `tableau/calculated_fields.txt` Tableau calculated fields (copy/paste)
- `docs/dashboard_spec.md` Dashboard layout and build spec
- `docs/dashboard_wireframe.png` Wireframe reference
- `dash_app/app.py` Interactive dashboard app (Dash/Plotly)

## Run the interactive dashboard (recommended)
1. Open a terminal in this project folder
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python dash_app/app.py
```

4. Open the URL shown in the terminal (usually `http://127.0.0.1:8050/`)

The dashboard includes filters for Region, Segment, Category, and Year. All charts update together.

## Rebuild the cleaned dataset
If you want to regenerate the cleaned dataset from the raw CSV:

```bash
python etl/clean_superstore.py --input data/raw/superstore.csv --outdir data/processed
```

## Build the same dashboard in Tableau
1. Connect Tableau to: `data/processed/superstore_cleaned.csv`
2. Create calculated fields from: `tableau/calculated_fields.txt`
3. Follow the layout in: `docs/dashboard_spec.md`
4. Publish to Tableau Public and link it in your GitHub and LinkedIn

