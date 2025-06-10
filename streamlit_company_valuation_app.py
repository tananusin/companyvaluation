import streamlit as st
import pandas as pd

from asset_data import AssetData
from user_preferences import get_user_preferences, UserPreference
from fetch_yfinance import can_fetch_data
from pe_percentile import display_pe_percentiles
from load_assets import load_financials_from_google_sheet

# --- Streamlit Page Config ---
st.set_page_config(page_title="Company Valuation", layout="centered")
st.title("🗂️ Company Valuation")

# --- User Preferences ---
user_pref = get_user_preferences()

symbol = st.text_input("Enter stock symbol (e.g., AAPL)", value="AAPL")

# --- PE Percentile Check Password and Fetch Data ---
if user_pref.password == st.secrets["credentials"]["app_password"]:
    st.success("🔓 Password Correct! Checking live data availability...")
    if can_fetch_data():  # ✅ Check fetch readiness
        with st.spinner("Fetching data OK"):
            pe_p25, pe_p75 = display_pe_percentiles(symbol)
    else:
        st.error("❌ Unable to fetch live data. Falling back to static data.")
else:
    st.warning("🔒 Offline Mode: Using static data from Google Sheet.")

# ---  ---
st.subheader("📥 Loading Financial Data")

# --- Financial Statements Load Asset Data ---
try:
    financials = load_financials_from_google_sheet(user_pref.sheet_url)
except Exception:
    st.error("❌ Failed to load data from the provided Google Sheet. Using default sheet instead.")
    financials = load_financials_from_google_sheet(st.secrets["google_sheet"]["url"])

# --- Display Financial Metrics ---
st.subheader("📊 Company Financials")

