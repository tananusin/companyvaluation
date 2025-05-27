import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.title("P/E Ratio Percentile (Custom Month Range with Valuation Classification)")

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
