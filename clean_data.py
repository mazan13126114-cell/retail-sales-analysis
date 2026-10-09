"""
Retail Sales Analysis - data cleaning pipeline
-----------------------------------------------
Reads the raw "Online Retail II" dataset, cleans and transforms it with
pandas, prints a few summary KPIs, and writes a dashboard-ready CSV that
Power BI connects to.

Dataset: "Online Retail II" (UCI Machine Learning Repository / Kaggle)
~1,000,000 transactions from a UK-based online retailer (2009-2011).

Usage:
    1. Download the dataset (Excel or CSV) into ./data/
    2. Set RAW_FILE below to the file name you downloaded.
    3. python clean_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

# --- Config ----------------------------------------------------------------
DATA_DIR = Path(__file__).parent / "data"
RAW_FILE = DATA_DIR / "online_retail_II.xlsx"   # change if you downloaded a CSV
CLEAN_FILE = DATA_DIR / "online_retail_clean.csv"

# Column names used below. The UCI Excel file uses these headers:
#   Invoice, StockCode, Description, Quantity, InvoiceDate, Price,
#   Customer ID, Country
# If your download uses slightly different names (e.g. "UnitPrice",
# "CustomerID", "InvoiceNo"), adjust RENAME_MAP accordingly.
RENAME_MAP = {
    "InvoiceNo": "Invoice",
    "UnitPrice": "Price",
    "CustomerID": "Customer ID",
}


def load_raw(path: Path) -> pd.DataFrame:
    """Load the raw file (Excel with multiple year sheets, or CSV)."""
    if not path.exists():
        raise FileNotFoundError(
            f"Raw data not found at {path}.\n"
            "Download 'Online Retail II' from the UCI ML Repository or Kaggle "
            "and place it in the ./data/ folder."
        )

    if path.suffix.lower() in {".xlsx", ".xls"}:
        # The Excel version ships two sheets (2009-2010, 2010-2011).
        sheets = pd.read_excel(path, sheet_name=None)       # dict of DataFrames
        df = pd.concat(sheets.values(), ignore_index=True)
    else:
        df = pd.read_csv(path, encoding="ISO-8859-1")

    return df.rename(columns=RENAME_MAP)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform the raw transactions into a KPI-ready table."""
    rows_start = len(df)

    # 1. Drop rows missing a customer or product description.
    df = df.dropna(subset=["Customer ID", "Description"])

    # 2. Remove cancelled orders (invoice numbers starting with "C").
    df = df[~df["Invoice"].astype(str).str.startswith("C")]

    # 3. Keep only real sales: positive quantity and price.
    df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

    # 4. Drop exact duplicate rows.
    df = df.drop_duplicates()

    # 5. Parse dates and derive time columns for trend analysis.
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.month
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["Weekday"] = df["InvoiceDate"].dt.day_name()

    # 6. Revenue per line item (the core KPI measure).
    df["Revenue"] = df["Quantity"] * df["Price"]

    # 7. Standardise text fields.
    df["Description"] = df["Description"].str.strip()
    df["Country"] = df["Country"].str.strip()

    # 8. Tidy types.
    df["Customer ID"] = df["Customer ID"].astype(np.int64)

    rows_end = len(df)
    print(f"Rows: {rows_start:,} -> {rows_end:,} "
          f"({rows_start - rows_end:,} removed during cleaning)")
    return df


def summary(df: pd.DataFrame) -> None:
    """Print the headline KPIs so you can sanity-check the output."""
    print("\n--- KPIs ---------------------------------------------")
    print(f"Total revenue       : {df['Revenue'].sum():,.0f}")
    print(f"Total orders        : {df['Invoice'].nunique():,}")
    print(f"Unique customers    : {df['Customer ID'].nunique():,}")
    print(f"Avg order value     : "
          f"{df.groupby('Invoice')['Revenue'].sum().mean():,.2f}")
    print(f"Date range          : "
          f"{df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}")
    print("\nTop 5 countries by revenue:")
    print(df.groupby('Country')['Revenue'].sum()
            .sort_values(ascending=False).head(5).round(0).to_string())


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    df = load_raw(RAW_FILE)
    df = clean(df)
    summary(df)
    df.to_csv(CLEAN_FILE, index=False)
    print(f"\nClean dataset written to {CLEAN_FILE}  ({len(df):,} rows)")


if __name__ == "__main__":
    main()
