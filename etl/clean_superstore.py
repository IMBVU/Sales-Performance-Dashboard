"""Clean and validate the Superstore dataset for Tableau.

Input:  raw Superstore CSV exported from Tableau Sample Superstore or Kaggle mirror.
Output: cleaned CSV + basic profiling summary.

Usage:
  python etl/clean_superstore.py --input data/raw/superstore.csv --outdir data/processed

This script:
- standardizes column names
- parses dates
- removes fully blank rows
- coerces numeric types
- creates a few helper fields useful in Tableau (Ship Days, Discount Bucket)
- writes a profiling summary (row counts, nulls, duplicates, min/max dates)

No external internet calls.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Trim and de-dupe spaces
    df = df.rename(columns={c: " ".join(str(c).strip().split()) for c in df.columns})

    # Common alternate names found in mirrors
    renames = {
        "Order Date": "Order Date",
        "Ship Date": "Ship Date",
        "Order ID": "Order ID",
        "Customer ID": "Customer ID",
        "Customer Name": "Customer Name",
        "Product ID": "Product ID",
        "Product Name": "Product Name",
        "Sub-Category": "Sub-Category",
        "Sub Category": "Sub-Category",
        "Category": "Category",
        "Segment": "Segment",
        "Region": "Region",
        "State": "State",
        "City": "City",
        "Postal Code": "Postal Code",
        "Ship Mode": "Ship Mode",
        "Sales": "Sales",
        "Profit": "Profit",
        "Discount": "Discount",
        "Quantity": "Quantity",
    }

    # Apply only where present
    df = df.rename(columns={c: renames[c] for c in df.columns if c in renames})

    return df


def discount_bucket(x: float) -> str:
    try:
        if pd.isna(x):
            return "Unknown"
        if x == 0:
            return "No Discount"
        if x <= 0.20:
            return "Low (0–20%)"
        if x <= 0.40:
            return "Medium (20–40%)"
        return "High (40%+)"
    except Exception:
        return "Unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to raw Superstore CSV")
    parser.add_argument("--outdir", required=True, help="Output directory")
    args = parser.parse_args()

    in_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(in_path, encoding_errors="ignore")
    df = normalize_columns(df)

    # Drop fully blank rows
    df = df.dropna(how="all").copy()

    # Parse dates (coerce errors to NaT)
    for col in ["Order Date", "Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Coerce numeric columns
    for col in ["Sales", "Profit", "Discount", "Quantity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Standardize Postal Code (some sources store as float)
    if "Postal Code" in df.columns:
        df["Postal Code"] = df["Postal Code"].astype("Int64")

    # Helper fields
    if "Order Date" in df.columns and "Ship Date" in df.columns:
        df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    if "Discount" in df.columns:
        df["Discount Bucket"] = df["Discount"].apply(discount_bucket)

    # Basic profiling
    summary = []
    summary.append(("rows", len(df)))
    summary.append(("columns", df.shape[1]))

    if "Order ID" in df.columns:
        summary.append(("unique_order_ids", df["Order ID"].nunique(dropna=True)))
        summary.append(("duplicate_order_id_rows", int(df.duplicated(subset=["Order ID"]).sum())))

    if "Order Date" in df.columns:
        summary.append(("order_date_min", str(df["Order Date"].min())))
        summary.append(("order_date_max", str(df["Order Date"].max())))

    nulls = df.isna().sum().sort_values(ascending=False)

    cleaned_csv = outdir / "superstore_cleaned.csv"
    profile_txt = outdir / "profiling_summary.txt"

    df.to_csv(cleaned_csv, index=False)

    with open(profile_txt, "w", encoding="utf-8") as f:
        f.write("Superstore Profiling Summary\n")
        f.write("===========================\n\n")
        for k, v in summary:
            f.write(f"{k}: {v}\n")
        f.write("\nNull counts (top 25):\n")
        for k, v in nulls.head(25).items():
            f.write(f"{k}: {int(v)}\n")

    print(f"Wrote: {cleaned_csv}")
    print(f"Wrote: {profile_txt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
