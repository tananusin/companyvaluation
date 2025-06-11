#financials_view.py

import streamlit as st
import pandas as pd

def show_income_statement_table(df: pd.DataFrame):
    st.markdown("💰 Income Statement")
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
    st.markdown("💵 Cash Flow Statement")
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
    st.markdown("📄 Balance Sheet")
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

def show_financial_statements_table(df: pd.DataFrame):
    show_income_statement_table(df)
    show_cf_statement_table(df)
    show_balance_sheet_table(df)

