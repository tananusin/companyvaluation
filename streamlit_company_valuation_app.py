import streamlit as st
import pandas as pd

from asset_data import AssetData
from user_preferences import get_user_preferences, UserPreference
from fetch_yfinance import can_fetch_data
from pe_percentile import display_pe_percentiles

# --- Streamlit Page Config ---
st.set_page_config(page_title="Company Valuation", layout="centered")
st.title("🗂️ Company Valuation")

# --- User Preferences ---
user_pref = get_user_preferences()

symbol = st.text_input("Enter stock symbol (e.g., AAPL)", value="AAPL")

# --- Check Password and Fetch Data ---
if user_pref.password == st.secrets["credentials"]["app_password"]:
    st.success("🔓 Password Correct! Checking live data availability...")
    if can_fetch_data():  # ✅ Check fetch readiness
        with st.spinner("Fetching data OK"):
            pe_p25, pe_p75 = display_pe_percentiles(symbol)
    else:
        st.error("❌ Unable to fetch live data. Falling back to static data.")
else:
    st.warning("🔒 Offline Mode: Using static data from Google Sheet.")

