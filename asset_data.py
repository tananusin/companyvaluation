# asset_data.py
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class AssetData:
    # Google Sheet Variables
    name: str
    symbol: str

    # PE Percentile
    pe_ratio: Optional[float] = None           # Trailing P/E ratio
    pe_25: Optional[float] = None              # 25th percentile P/E
    pe_75: Optional[float] = None              # 75th percentile P/E

@dataclass
class CompanyFinancials:
    # Credit Rating
    credit_rating: Dict[int, Optional[str]] = field(default_factory=dict)

    # Income Statement
    ebit: Dict[int, Optional[float]] = field(default_factory=dict)
    interest: Dict[int, Optional[float]] = field(default_factory=dict)
    net_profit: Dict[int, Optional[float]] = field(default_factory=dict)

    # Cashflow Statement
    ocf: Dict[int, Optional[float]] = field(default_factory=dict)
    net_cf: Dict[int, Optional[float]] = field(default_factory=dict)

    # Balance Sheet
    cash: Dict[int, Optional[float]] = field(default_factory=dict)
    inventory: Dict[int, Optional[float]] = field(default_factory=dict)
    current_asset: Dict[int, Optional[float]] = field(default_factory=dict)
    current_debt: Dict[int, Optional[float]] = field(default_factory=dict)
    equity: Dict[int, Optional[float]] = field(default_factory=dict)
    debt: Dict[int, Optional[float]] = field(default_factory=dict)

    # --- Calculated Ratios ---

    def quick_ratio(self, year: int) -> Optional[float]:
        try:
            ca = self.current_asset.get(year)
            inv = self.inventory.get(year)
            cd = self.current_debt.get(year)
            if ca is not None and inv is not None and cd and cd != 0:
                return (ca - inv) / cd
        except:
            pass
        return None

    def current_ratio(self, year: int) -> Optional[float]:
        try:
            ca = self.current_asset.get(year)
            cd = self.current_debt.get(year)
            if ca is not None and cd and cd != 0:
                return ca / cd
        except:
            pass
        return None

    def icr(self, year: int) -> Optional[float]:
        try:
            e = self.ebit.get(year)
            i = self.interest.get(year)
            if e is not None and i and i != 0:
                return e / i
        except:
            pass
        return None

    def cash_coverage(self, year: int) -> Optional[float]:
        try:
            c = self.cash.get(year)
            i = self.interest.get(year)
            if c is not None and i and i != 0:
                return c / i
        except:
            pass
        return None

    def roe(self, year: int) -> Optional[float]:
        try:
            p = self.net_profit.get(year)
            e = self.equity.get(year)
            if p is not None and e and e != 0:
                return p / e
        except:
            pass
        return None

    def de_ratio(self, year: int) -> Optional[float]:
        try:
            d = self.debt.get(year)
            e = self.equity.get(year)
            if d is not None and e and e != 0:
                return d / e
        except:
            pass
        return None
