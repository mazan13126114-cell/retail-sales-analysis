# Retail Sales Analysis

End-to-end analysis of ~1,000,000 e-commerce transactions in **Python**:
a pandas cleaning pipeline that turns a messy transaction export into a
KPI-ready dataset, plus a Jupyter notebook with KPIs, charts, and written
insights for non-technical stakeholders.

## Problem

An online retailer wants to understand its sales performance: how much
revenue it generates, how that trends over time, which products and markets
drive the business, and how much comes from repeat customers. The raw
transaction export is messy (cancellations, returns, missing customer IDs,
duplicates), so it must be cleaned before any reliable reporting is possible.

## Data

**Online Retail II** - UCI Machine Learning Repository / Kaggle.
~1M transactions from a UK-based online retailer, Dec 2009 - Dec 2011.

| Column | Description |
|--------|-------------|
| Invoice | Invoice number (prefixed `C` = cancellation) |
| StockCode | Product code |
| Description | Product name |
| Quantity | Units per line item |
| InvoiceDate | Timestamp of the transaction |
| Price | Unit price (GBP) |
| Customer ID | Customer identifier |
| Country | Customer country |

> The raw file is **not** committed (see `.gitignore`). Download it yourself
> into `./data/` before running.

## What's in here

| File | Purpose |
|------|---------|
| `retail_sales_analysis.ipynb` | The full analysis: load, clean, KPIs, charts, insights |
| `clean_data.py` | Standalone version of the cleaning pipeline (CLI script) |
| `requirements.txt` | Python dependencies |

## Analysis workflow (`retail_sales_analysis.ipynb`)

1. **Load** the raw Excel (both year sheets) into one DataFrame.
2. **Clean & transform:** drop missing customer/description rows, remove
   cancellations, keep only positive quantity/price, drop duplicates, parse
   dates, derive `Year`/`Month`/`YearMonth`/`Weekday`, compute `Revenue`.
3. **KPIs:** total revenue, orders, unique customers, average order value.
4. **Visualise (Matplotlib):** monthly revenue trend, top 10 products,
   top export markets, revenue by weekday, repeat vs one-time customers.
5. **Insights:** written conclusions and recommendations for a stakeholder.

## How to run

```bash
pip install -r requirements.txt
# place the raw dataset in ./data/ (see Data section)
jupyter notebook retail_sales_analysis.ipynb
# run all cells top to bottom
```

## Tech

Python · pandas · NumPy · Matplotlib · Jupyter
