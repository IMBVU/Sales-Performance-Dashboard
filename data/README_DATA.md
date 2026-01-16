# Data

This project uses the **Tableau Sample - Superstore** dataset (CSV).

- Place the raw file at: `data/raw/superstore.csv`
- Generate cleaned data by running:\n\n```bash\npython etl/clean_superstore.py --input data/raw/superstore.csv --outdir data/processed\n```\n\n- Tableau/Dash should connect to: `data/processed/superstore_cleaned.csv`
