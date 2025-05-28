#pe_percentile.py
from fetch_yfinance import get_pe_percentiles

def get_pe_percentiles(symbol: str):
    try:
        st.subheader("📋 P/E Ratio Percentiles")
        
        months = st.number_input("How many months?", min_value=6, max_value=120, value=6, step=6)

        pe_25, pe_75=get_pe_percentiles(symbol,months)

        st.write(f"**25th Percentile P/E:** {pe_25:.2f}")
        st.write(f"**75th Percentile P/E:** {pe_75:.2f}")
        
        return pe_25, pe_75

    except Exception:
        return None, None
