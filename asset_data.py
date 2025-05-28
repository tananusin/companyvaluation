# asset_data.py
from dataclasses import dataclass
from typing import Optional  # If User Leave Input Empty

@dataclass
class AssetData:
    # Google Sheet Variables
    name: str
    symbol: str
    
    pe_ratio: Optional[float] = None           # Trailing P/E ratio
    pe_25: Optional[float] = None              # 25th percentile P/E
    pe_75: Optional[float] = None              # 75th percentile P/E
