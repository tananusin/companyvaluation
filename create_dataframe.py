# create_dataframe.py

import pandas as pd
from asset_data import CompanyFinancials
from typing import Dict, Optional


def calculate_ratios(financials: CompanyFinancials) -> Dict[str, Dict[int, Optional[float]]]:
    years = sorted(financials.ebit.keys())

    return {
        "Quick Ratio": {y: financials.quick_ratio(y) for y in years},
        "Current Ratio": {y: financials.current_ratio(y) for y in years},
        "ICR": {y: financials.icr(y) for y in years},
        "Cash Coverage": {y: financials.cash_coverage(y) for y in years},
        "ROE": {y: financials.roe(y) for y in years},
        "DE Ratio": {y: financials.de_ratio(y) for y in years},
    }


def get_financials_df(financials: CompanyFinancials) -> pd.DataFrame:
    ratios = calculate_ratios(financials)

    data = {
        "EBIT": financials.ebit,
        "Interest": financials.interest,
        "Net Profit": financials.net_profit,
        "OCF": financials.ocf,
        "Net CF": financials.net_cf,
        "Cash": financials.cash,
        "Inventory": financials.inventory,
        "Current Asset": financials.current_asset,
        "Current Debt": financials.current_debt,
        "Credit Rating": financials.credit_rating,
        "Equity": financials.equity,
        "Debt": financials.debt,
        **ratios,
    }

    df = pd.DataFrame(data).T
    df = df.reindex(sorted(df.columns), axis=1)
    return df

