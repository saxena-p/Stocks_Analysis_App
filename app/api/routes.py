from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.api.schemas import StockMetric
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/api", tags=["metrics"])

service = MetricsService()

@router.get("/metrics")
def list_metrics():
    return {
        "metrics": service.available_metrics()
    }

@router.get("/metrics/{metric}/time_windows")
def list_time_windows(metric: str):
    windows = service.available_time_windows(metric)
    if not windows:
        raise HTTPException(
            status_code=404,
            detail=f"No windows found for metric '{metric}'"
        )
    return {"windows": windows}

@router.get("/top", response_model=List[StockMetric])
def top_n_stocks(
    metric: str = Query(..., description="Metric name, e.g. return"),
    window: str = Query(..., description="Time window, e.g. 1mo"),
    n: int = Query(5, ge=1, le=100)
):
    try:
        df = service.top_n(metric, window, n)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return [
        StockMetric(ticker=row["Ticker"], value=row[f"{metric}_{window}"])
        for _, row in df.iterrows()
    ]