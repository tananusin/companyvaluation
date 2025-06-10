# load_assets.py
import pandas as pd
import streamlit as st
from asset_data import CompanyFinancials
from typing import Optional

def clean_numeric(value: Optional[str]) -> Optional[float]:
    """Converts strings like '1,234,567' to float, or returns None."""
    try:
        return float(str(value).replace(",", "").strip()) if pd.notnull(value) else None
    except ValueError:
        return None

def load_financials_from_google_sheet(sheet_url: str) -> CompanyFinancials:
    # Adjust URL for CSV export
    sheet_url = sheet_url.replace('/edit#gid=', '/gviz/tq?tqx=out:csv&gid=')

    # Load and clean data
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip().str.lower()
    except Exception as e:
        st.error(f"❌ Failed to load Google Sheet: {e}")
        st.stop()

    # Convert year columns to integers (assumes columns like '2020', '2021', etc.)
    year_cols = [int(col) for col in df.columns[1:]]

    # ✅ Initialize the dataclass object
    financials = CompanyFinancials()

    for _, row in df.iterrows():
        metric = str(row[df.columns[0]]).strip().lower()
        if not metric:
            continue  # Skip blank rows

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



