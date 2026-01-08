from pydantic import BaseModel

class StockMetric(BaseModel):
    ticker: str
    value: float