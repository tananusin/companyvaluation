#pe_percentile.py
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_pe_percentiles(symbol: str):
    try:
        st.subheader("📋 P/E Ratio Percentiles")
        
        months = st.number_input("How many months?", min_value=6, max_value=120, value=6, step=6)
        
        end_date = datetime.today()
        start_date = end_date - timedelta(days=months * 30)

        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date.strftime('%Y-%m-%d'),
                              end=end_date.strftime('%Y-%m-%d'),
                              interval='1mo')

        info = ticker.info
        trailing_eps = info.get('trailingEps')

        if hist.empty:
            return None, None
        if trailing_eps in [None, 0]:
            return None, None

        hist = hist[hist['Close'] > 0]
        hist['PE'] = hist['Close'] / trailing_eps
        hist = hist[hist['PE'] < 1000]  # filter extreme outliers

        pe_series = hist['PE']
        percentiles = np.percentile(pe_series, [25, 75])
        return float(percentiles[0]), float(percentiles[1])

    except Exception:
        return None, None
