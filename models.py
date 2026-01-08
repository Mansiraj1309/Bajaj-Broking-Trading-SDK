from pydantic import BaseModel
from typing import Optional

class Instrument(BaseModel):
    symbol: str
    exchange: str
    instrumentType: str
    lastTradedPrice: float


class OrderRequest(BaseModel):
    symbol: str
    orderType: str       # BUY / SELL
    orderStyle: str      # MARKET / LIMIT
    quantity: int
    price: Optional[float] = None
