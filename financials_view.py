#financials_view.py

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from asset_data import CompanyFinancials
from typing import List

def get_financials_df(financials: CompanyFinancials) -> pd.DataFrame:
    # Organize each metric as a row
    data = {
        "EBIT": financials.ebit,
        "Interest": financials.interest,
        "Net Profit": financials.net_profit,
        "OCF": financials.ocf,
        "Net CF": financials.net_cf,
        "Cash": financials.cash,
        "Inventory": financials.inventory,
        "Current Asset": financials.current_asset,
        "Current Debt": financials.current_debt,
        "Credit Rating": financials.credit_rating,
        "Equity": financials.equity,
        "Debt": financials.debt,
    }

    # Convert to DataFrame (metrics as rows, years as columns)
    df = pd.DataFrame(data).T
    df = df.reindex(sorted(df.columns), axis=1)  # sort years
    return df

def show_income_statement_table(df: pd.DataFrame):
    st.markdown("Income Statement")
    rows_to_show = [      
        "EBIT",
        "Interest",
        "Net Profit",
    ]

    # Filter DataFrame
    df_filtered = df.loc[[row for row in rows_to_show if row in df.index]]

    # Format values
    def format_val(val):
        if isinstance(val, (int, float)):
            return f"{val:,.0f}"
        return val if val else "-"

    # Display in Streamlit
    st.dataframe(df_filtered.style.format(format_val))

def show_cf_statement_table(df: pd.DataFrame):
    st.markdown("Cash Flow Statement")
    rows_to_show = [
        "OCF",
        "Net CF",
    ]

    # Filter DataFrame
    df_filtered = df.loc[[row for row in rows_to_show if row in df.index]]

    # Format values
    def format_val(val):
        if isinstance(val, (int, float)):
            return f"{val:,.0f}"
        return val if val else "-"

    # Display in Streamlit
    st.dataframe(df_filtered.style.format(format_val))

def show_balance_sheet_table(df: pd.DataFrame):
    st.markdown("Balance Sheet")
    rows_to_show = [
        "Cash",
        "Inventory",
        "Current Asset",
        "Current Debt",        
        "Equity",
        "Debt",
    ]

    # Filter DataFrame
    df_filtered = df.loc[[row for row in rows_to_show if row in df.index]]

    # Format values
    def format_val(val):
        if isinstance(val, (int, float)):
            return f"{val:,.0f}"
        return val if val else "-"

    # Display in Streamlit
    st.dataframe(df_filtered.style.format(format_val))


