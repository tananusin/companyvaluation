#default_risk.py

import streamlit as st
import pandas as pd

import pandas as pd
import streamlit as st

def show_credit_rating_table(df: pd.DataFrame):
    st.markdown("⚖️ Official Credit Rating")
    rows_to_show = ["Credit Rating",]

    # Filter DataFrame
    df_filtered = df.loc[[row for row in rows_to_show if row in df.index]]

    # Format values (string fallback for missing values)
    def format_val(val):
        return val if val else "-"

    # Display in Streamlit
    st.dataframe(df_filtered.style.format(format_val))

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
        "Debt",
        "Equity",
        "ROE",
        "DE Ratio",
    ]

    # Filter the DataFrame to required rows
    df_filtered = df.loc[[row for row in rows_to_show if row in df.index]]

    # Format values: ROE as percentage, others as numbers
    def format_values(val, row_name):
        if isinstance(val, (int, float)):
            if row_name == "ROE":
                return f"{val * 100:.2f}%"
            else:
                return f"{val:,.2f}"
        return "-"

    # Build a formatted DataFrame
    def apply_formatting(df: pd.DataFrame):
        styled = df.style

        # Apply formatting row-by-row
        for row in df.index:
            if row == "ROE":
                styled = styled.format({col: lambda v: f"{v * 100:.2f}%" for col in df.columns}, subset=pd.IndexSlice[row, :])
            else:
                styled = styled.format({col: "{:,.2f}" for col in df.columns}, subset=pd.IndexSlice[row, :])

        return styled

    # Apply conditional font color to DE Ratio based on ROE
    def color_de_ratio(val, roe_val):
        if pd.isna(val) or pd.isna(roe_val):
            return ""
        if roe_val > 0.20:
            return "color: red" if val > 2.5 else "color: green"
        elif 0.10 <= roe_val <= 0.20:
            return "color: red" if val > 2 else "color: green"
        else:  # ROE < 10%
            return "color: red" if val > 1 else "color: green"

    # Apply DE Ratio coloring using a custom function
    def apply_de_color(df: pd.DataFrame, styled: pd.io.formats.style.Styler):
        de_row = df.loc["DE Ratio"]
        roe_row = df.loc["ROE"]
        color_df = pd.DataFrame("", index=df.index, columns=df.columns)

        for col in df.columns:
            roe_val = roe_row[col]
            de_val = de_row[col]
            color_df.loc["DE Ratio", col] = color_de_ratio(de_val, roe_val)

        return styled.apply(lambda _: color_df, axis=None)

    # Format values and apply conditional coloring
    styled = apply_formatting(df_filtered)
    styled = apply_de_color(df_filtered, styled)

    # Display in Streamlit
    st.dataframe(styled)

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

    # Conditional red font for negative Net CF
    def color_net_cf(val, row_name):
        if row_name == "Net CF" and isinstance(val, (int, float)) and val < 0:
            return "color: red"
        return ""

    # Apply font color row-wise
    def apply_color_formatting(df_style):
        return df_style.apply(
            lambda row: [color_net_cf(val, row.name) for val in row],
            axis=1
        )

    # Display with formatting
    st.dataframe(
        df_filtered.style
            .format(format_val)
            .pipe(apply_color_formatting)
    )

def show_default_risk_tables(df: pd.DataFrame):
    show_credit_rating_table(df)
    show_supplier_debt_table(df)
    show_financier_debt_table(df)
    show_debt_structure_table(df)
    show_cash_level_table(df)

