import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.title("3-Year P/E Ratio Percentile (Monthly Data)")

# User input
symbol = st.text_input("Enter stock symbol (e.g., AAPL)", value="AAPL")

if symbol:
    try:
        # Set date range
        end_date = datetime.today()
        start_date = end_date - timedelta(days=3 * 365)

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
            hist = hist[hist['PE'] < 1000]  # Filter outliers

            # Current P/E and percentile rank
            pe_current = hist['PE'].iloc[-1]
            pe_percentile_rank = np.round((hist['PE'] < pe_current).mean() * 100, 2)

            # Percentile summary
            percentiles = np.percentile(hist['PE'], [0, 10, 25, 50, 75, 90, 100])
            percentile_df = pd.DataFrame({
                'Percentile': ['0th', '10th', '25th', '50th (Median)', '75th', '90th', '100th'],
                'P/E': [f"{p:.2f}" for p in percentiles]
            })

            # Display results
            st.write(f"**Current P/E:** {pe_current:.2f}")
            st.write(f"**Percentile Rank (3 Years):** {pe_percentile_rank}th")
            st.line_chart(hist['PE'])
            st.write("**P/E Percentiles (3 Years):**")
            st.dataframe(percentile_df)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
