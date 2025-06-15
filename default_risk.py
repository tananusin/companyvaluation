#default_risk.py

import streamlit as st
import pandas as pd

def show_supplier_debt_table(df: pd.DataFrame):
    st.markdown("📦 Supplier Payment")
    rows = [
        "Current Debt",
        "Inventory",
        "Current Asset",
        "Current Ratio",
        "Quick Ratio",
        "ICR",
        "Cash Coverage",
    ]
    df = df.loc[[r for r in rows if r in df.index]]

    # Format numbers
    def format_val(v):
        return f"{v:,.2f}" if isinstance(v, (int, float)) else v or "-"

    # Conditional coloring
    def highlight_key_ratios(val, row_name):
        if not isinstance(val, (int, float)):
            return ""
        if row_name == "ICR":
            if val > 2:
                return "color: green"
            elif val < 1.5:
                return "color: red"
        if row_name == "Cash Coverage":
            if val > 1:
                return "color: green"
            elif val < 1:
                return "color: red"
        return ""

    # Apply coloring
    def apply_highlight(df):
        styled = pd.DataFrame("", index=df.index, columns=df.columns)
        for row in df.index:
            for col in df.columns:
                styled.loc[row, col] = highlight_key_ratios(df.loc[row, col], row)
        return styled

    styled_df = df.style.format(format_val).apply(apply_highlight, axis=None)

    st.dataframe(styled_df)

def show_financier_debt_table(df: pd.DataFrame):
    st.markdown("🏦 Financier Interest Payment")
    rows_to_show = [
        "Interest",
        "EBIT",
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

