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
    
