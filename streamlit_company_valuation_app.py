import streamlit as st
import pandas as pd

from asset_data import AssetData
from user_preferences import get_user_preferences, UserPreference
from fetch_yfinance import can_fetch_data

# --- Streamlit Page Config ---
st.set_page_config(page_title="Company Valuation", layout="centered")
st.title("🗂️ Company Valuation")

# --- User Preferences ---
user_pref = get_user_preferences()

# --- Check Password and Fetch Data ---
if user_pref.password == st.secrets["credentials"]["app_password"]:
    st.success("🔓 Password Correct! Checking live data availability...")
    if can_fetch_data():  # ✅ Check fetch readiness
        with st.spinner("Fetching live prices and FX rates..."):
            pe_p20 = (assets)
    else:
        st.error("❌ Unable to fetch live data. Falling back to static data.")
else:
    st.warning("🔒 Offline Mode: Using static data from Google Sheet.")

st.subheader("📋 P/E Ratio Percentile")



# User input
symbol = st.text_input("Enter stock symbol (e.g., AAPL)", value="AAPL")
months = st.number_input("How many months of history?", min_value=6, max_value=36, value=36, step=6)

if symbol and months:
    try:
        # Define date range
        end_date = datetime.today()
        start_date = end_date - timedelta(days=months * 30)

        # Fetch monthly price history
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date.strftime('%Y-%m-%d'),
                              end=end_date.strftime('%Y-%m-%d'),
                              interval='1mo')

        info = ticker.info
        trailing_eps = info.get('trailingEps')

        if hist.empty:
            st.warning("No historical price data available.")
        elif trailing_eps in [None, 0]:
            st.warning("Trailing EPS data is unavailable or zero.")
        else:
            # Calculate monthly P/E
            hist = hist[hist['Close'] > 0]
            hist['PE'] = hist['Close'] / trailing_eps
            hist = hist[hist['PE'] < 1000]  # Remove extreme outliers

            # Current P/E and percentile rank
            pe_current = hist['PE'].iloc[-1]
            pe_percentile_rank = np.round((hist['PE'] < pe_current).mean() * 100, 2)

            # Calculate percentiles
            percentiles = np.percentile(hist['PE'], [0, 10, 25, 50, 75, 90, 100])
            p25 = percentiles[2]  # 25th percentile
            valuation_label = "Undervalued" if pe_current < p25 else "Fairly or Overvalued"

            # Display
            st.write(f"**Current P/E:** {pe_current:.2f}")
            st.write(f"**Percentile Rank (last {months} months):** {pe_percentile_rank}th")
            st.write(f"**Valuation Classification:** `{valuation_label}`")
            st.line_chart(hist['PE'])

            st.write("**P/E Percentiles:**")
            st.dataframe(pd.DataFrame({
                'Percentile': ['0th', '10th', '25th', '50th (Median)', '75th', '90th', '100th'],
                'P/E': [f"{p:.2f}" for p in percentiles]
            }))

    except Exception as e:
        st.error(f"Error fetching data: {e}")
