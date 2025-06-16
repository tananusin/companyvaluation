#default_risk.py

import streamlit as st
import pandas as pd

import pandas as pd
import streamlit as st

def show_supplier_debt_table(df: pd.DataFrame):
    st.markdown("📦 Supplier Payment")
    rows_to_show = [
        "Current Debt",
        "Inventory",
        "Current Asset",
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

    # Conditional coloring
    def highlight_ratio(val, row_name):
        if row_name == "Current Ratio":
            if val >= 1.5:
                return "color: green"
            else:
                return "color: red"
        elif row_name == "Quick Ratio":
            if val >= 1.0:
                return "color: green"
            else:
                return "color: red"
        return ""

    # Apply conditional formatting
    def apply_color_formatting(df_style):
        return df_style.apply(
            lambda row: [highlight_ratio(v, row.name) for v in row],
            axis=1
        )

    st.dataframe(
        df_filtered.style
            .format(format_val)
            .pipe(apply_color_formatting)
    )

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

    # Format numbers
    def format_val(val):
        if isinstance(val, (int, float)):
            return f"{val:,.2f}"
        return val if val else "-"

    # Conditional font color logic
    def highlight_ratio(val, row_name):
        if row_name == "ICR":
            if val >= 2:
                return "color: green"
            elif val < 1.5:
                return "color: red"
        elif row_name == "CF Coverage":
            if val >= 1:
                return "color: green"
            else:
                return "color: red"
        return ""

    # Apply style based on row and value
    def apply_color_formatting(df_style):
        return df_style.apply(
            lambda row: [highlight_ratio(v, row.name) for v in row],
            axis=1
        )

    # Display styled DataFrame
    st.dataframe(
        df_filtered.style
            .format(format_val)
            .pipe(apply_color_formatting)
    )

def show_debt_structure_table(df: pd.DataFrame):
    st.markdown("⛓️ Long-term Debt Structure")
    rows_to_show = [
        "Equity",
        "Debt",
        "ROE",
        "DE Ratio",
    ]

    # Filter DataFrame
    df_filtered = df.loc[[row for row in rows_to_show if row in df.index]]

    # Custom formatting function
    def format_val(val, row_name):
        if isinstance(val, (int, float)):
            if row_name == "ROE":
                return f"{val * 100:.2f}%"
            else:
                return f"{val:,.2f}"
        return val if val else "-"

    # Wrapper for pandas Styler to apply formatting per row
    def format_dataframe(df):
        return df.style.format(lambda val, row=row: format_val(val, row), axis=0)

    # Apply formatting and display
    st.dataframe(format_dataframe(df_filtered))

def show_cash_level_table(df: pd.DataFrame):
    st.markdown("💵 Cash Level")
    rows_to_show = [
        "Net CF",
        "Cash",
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
    show_cash_level_table(df)

