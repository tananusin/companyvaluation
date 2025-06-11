#default_risk.py

import streamlit as st
import pandas as pd

def show_default_risk_table(df: pd.DataFrame):
    rows_to_show = [
        "Quick Ratio",
        "Current Ratio",
        "Cash Coverage",
        "ICR",        
        "Cash Coverage",
        "ROE",
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
