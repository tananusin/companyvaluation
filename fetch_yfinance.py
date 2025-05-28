# fetch_yfinance.py
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def can_fetch_data(test_symbol: str = "AAPL") -> bool:
    """Test if live data can be fetched successfully (e.g., not rate-limited or offline)."""
    try:
        ticker = yf.Ticker(test_symbol)
        price = ticker.info.get("regularMarketPrice", None)
        return price is not None
    except Exception:
        return False

def get_trailing_pe(symbol: str) -> float | None:
    """Fetches the trailing P/E ratio for the asset symbol."""
    try:
        ticker = yf.Ticker(symbol.strip().upper())
        pe_ratio = ticker.info.get("trailingPE")
        
        # Set P/E to 0.0 if None or not available
        if pe_ratio is None:
            return 0.0
        
        return round(pe_ratio, 2) if pe_ratio else None
    except Exception:
        return None

def get_pe_percentiles(symbol: str, months: int):
    try:
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

