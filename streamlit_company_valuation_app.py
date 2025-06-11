import streamlit as st
import pandas as pd

from asset_data import AssetData
from user_preferences import get_user_preferences, UserPreference
from load_assets import load_financials_from_google_sheet
from create_dataframe import get_financials_df
from financials_view import show_financial_statements_table
from default_risk import show_default_risk_table

# --- Streamlit Page Config ---
st.set_page_config(page_title="Company Valuation", layout="centered")
st.title("🏢 Company Valuation")

# --- User Preferences ---
user_pref = get_user_preferences()

try:
    financials = load_financials_from_google_sheet(user_pref.sheet_url)
except Exception:
    st.error("❌ Failed to load data from the provided Google Sheet. Using default sheet instead.")
    financials = load_financials_from_google_sheet(st.secrets["google_sheet"]["url"])

df_financials = get_financials_df(financials)

tab1, tab2 = st.tabs(["🧾 Financials", "🚫 Default Risk"])

with tab1: # --- Financial Statements Load Asset Data ---
    st.subheader("🧾 Financial Statements")    
    show_financial_statements_table(df_financials)

with tab2: # --- Financial Statements Load Asset Data ---
    st.subheader("🚫 Default Risk")    
    show_default_risk_table(df_financials)






