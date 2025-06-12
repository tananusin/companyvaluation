#default_risk.py

import streamlit as st
import pandas as pd

def show_supplier_debt_table(df: pd.DataFrame):
    st.markdown("📦 Supplier Debt")
    rows_to_show = [
        "Inventory",
        "Current Asset",
        "Current Debt",
        "Current Ratio",
        "Quick Ratio",
    ]

    # Filter DataFrame
    df_filtered = df.loc[[row for row in rows_to_show if row in df.index]]

    # Format values
    def format_val(val):
        if isinstance(val, (int, float)):
            return f"{val:,.2f}"
        return val if val else "-"

    # Display in Streamlit
    st.dataframe(df_filtered.style.format(format_val))

def show_financier_debt_table(df: pd.DataFrame):
    st.markdown("🏦 Financier Debt")
    rows_to_show = [
        "EBIT",
        "Interest",
        "OCF",
        "ICR",
        "CF Coverage",
    ]

    # Filter DataFrame
    df_filtered = df.loc[[row for row in rows_to_show if row in df.index]]

    # Format values
    def format_val(val):
        if isinstance(val, (int, float)):
            return f"{val:,.2f}"
        return val if val else "-"

    # Display in Streamlit
    st.dataframe(df_filtered.style.format(format_val))

def show_debt_structure_table(df: pd.DataFrame):
    st.markdown("⛓️ Long-term Debt Structure")
    rows_to_show = [
        "Net CF",
        "Cash",
        "Equity",
        "Debt",
        "ROE",
        "DE Ratio",
    ]

    # Filter DataFrame
    df_filtered = df.loc[[row for row in rows_to_show if row in df.index]]

    # Format values
    def format_val(val):
        if isinstance(val, (int, float)):
            return f"{val:,.2f}"
        return val if val else "-"

    # Display in Streamlit
    st.dataframe(df_filtered.style.format(format_val))

def show_default_risk_tables(df: pd.DataFrame):
    show_supplier_debt_table(df)
    show_financier_debt_table(df)
    show_debt_structure_table(df)

