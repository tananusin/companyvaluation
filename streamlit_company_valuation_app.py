import streamlit as st
import pandas as pd

from asset_data import AssetData
from user_preferences import get_user_preferences, UserPreference
from fetch_yfinance import can_fetch_data
from pe_percentile import display_pe_percentiles
from load_assets import load_financials_from_google_sheet
from financials_view import get_financials_df, show_income_statement_table, show_cf_statement_table, show_balance_sheet_table, show_default_risk_table

# --- Streamlit Page Config ---
st.set_page_config(page_title="Company Valuation", layout="centered")
st.title("🗂️ Company Valuation")

# --- User Preferences ---
user_pref = get_user_preferences()

try:
    financials = load_financials_from_google_sheet(user_pref.sheet_url)
except Exception:
    st.error("❌ Failed to load data from the provided Google Sheet. Using default sheet instead.")
    financials = load_financials_from_google_sheet(st.secrets["google_sheet"]["url"])

df_financials = get_financials_df(financials)

tab1, tab2, tab3 = st.tabs(["📋 PE Percentiles", "📶 Financials", "Default"])

with tab1: # --- PE Percentile Check Password and Fetch Data ---
    st.subheader("📊 PE Percentiles")
    symbol = st.text_input("Enter stock symbol (e.g., AAPL)", value="AAPL")

    if user_pref.password == st.secrets["credentials"]["app_password"]:
        st.success("🔓 Password Correct! Checking live data availability...")
        if can_fetch_data():  # ✅ Check fetch readiness
            with st.spinner("Fetching data OK"):
                pe_p25, pe_p75 = display_pe_percentiles(symbol)
        else:
            st.error("❌ Unable to fetch live data. Falling back to static data.")
    else:
        st.warning("🔒 Offline Mode: Using static data from Google Sheet.")


with tab2: # --- Financial Statements Load Asset Data ---
    st.subheader("📊 Financial Statements")    
    show_income_statement_table(df_financials)
    show_cf_statement_table(df_financials)
    show_balance_sheet_table(df_financials)

with tab3: # --- Financial Statements Load Asset Data ---
    st.subheader("📊 Default Risk")    
    show_default_risk_table(df_financials)






