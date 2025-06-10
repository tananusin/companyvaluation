# load_assets.py
import pandas as pd
from asset_data import CompanyFinancials
from typing import Optional

def clean_numeric(value: Optional[str]) -> Optional[float]:
    """Converts strings like '1,234,567' to float."""
    try:
        return float(str(value).replace(",", "").strip()) if pd.notnull(value) else None
    except ValueError:
        return None

def load_financials_from_csv(csv_path: str) -> CompanyFinancials:
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    # Convert year columns to int
    year_cols = [int(col) for col in df.columns[1:]]

    for _, row in df.iterrows():
        metric = str(row[df.columns[0]]).strip().lower()
        if metric == "credit rating":
            for year in year_cols:
                value = row[str(year)].strip() if pd.notnull(row[str(year)]) else None
                financials.credit_rating[year] = value
        elif metric == "inventory":
            for year in year_cols:
                financials.inventory[year] = clean_numeric(row[str(year)])
        elif metric == "current asset":
            for year in year_cols:
                financials.current_asset[year] = clean_numeric(row[str(year)])
        elif metric == "current debt":
            for year in year_cols:
                financials.current_debt[year] = clean_numeric(row[str(year)])
        elif metric == "ebit":
            for year in year_cols:
                financials.ebit[year] = clean_numeric(row[str(year)])
        elif metric == "interest":
            for year in year_cols:
                financials.interest[year] = clean_numeric(row[str(year)])
        elif metric == "net profit":
            for year in year_cols:
                financials.net_profit[year] = clean_numeric(row[str(year)])
        elif metric == "ocf":
            for year in year_cols:
                financials.ocf[year] = clean_numeric(row[str(year)])
        elif metric == "net cf":
            for year in year_cols:
                financials.net_cf[year] = clean_numeric(row[str(year)])
        elif metric == "cash":
            for year in year_cols:
                financials.cash[year] = clean_numeric(row[str(year)])
        # Add more mappings here if needed

    return financials

