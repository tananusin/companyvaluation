# load_assets.py
import pandas as pd
from asset_data import CompanyFinancials
from typing import Optional

def clean_numeric(value: Optional[str]) -> Optional[float]:
    """Converts strings like '1,234,567' to float, or returns None."""
    try:
        return float(str(value).replace(",", "").strip()) if pd.notnull(value) else None
    except ValueError:
        return None

def load_financials_from_csv(csv_path: str) -> CompanyFinancials:
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    # Convert year columns to integers (assumes columns like '2020', '2021', etc.)
    year_cols = [int(col) for col in df.columns[1:]]

    # ✅ Initialize the dataclass object
    financials = CompanyFinancials()

    for _, row in df.iterrows():
        metric = str(row[df.columns[0]]).strip().lower()
        for year in year_cols:
            raw_value = row[str(year)] if str(year) in row else None

            if metric == "credit rating":
                financials.credit_rating[year] = raw_value.strip() if pd.notnull(raw_value) else None
            elif metric == "inventory":
                financials.inventory[year] = clean_numeric(raw_value)
            elif metric == "current asset":
                financials.current_asset[year] = clean_numeric(raw_value)
            elif metric == "current debt":
                financials.current_debt[year] = clean_numeric(raw_value)
            elif metric == "ebit":
                financials.ebit[year] = clean_numeric(raw_value)
            elif metric == "interest":
                financials.interest[year] = clean_numeric(raw_value)
            elif metric == "net profit":
                financials.net_profit[year] = clean_numeric(raw_value)
            elif metric == "ocf":
                financials.ocf[year] = clean_numeric(raw_value)
            elif metric == "net cf":
                financials.net_cf[year] = clean_numeric(raw_value)
            elif metric == "cash":
                financials.cash[year] = clean_numeric(raw_value)

    return financials


