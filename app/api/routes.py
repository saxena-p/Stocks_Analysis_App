from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.api.schemas import StockMetric
from app.services.metrics_service import MetricsService
from fastapi.responses import HTMLResponse
import plotly.express as px

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


@router.get("/graph", response_class=HTMLResponse)
def graph(metric: str, 
          window: str = "1y", 
          n: int = 5):
    
    ALLOWED_METRICS = {"Return", "Volatility"}

    if metric not in ALLOWED_METRICS:
        raise HTTPException(400, "Invalid metric")
    
    df = service.top_n(metric, window, n)

    fig = px.bar(
        df,
        x="Ticker",
        y=f"{metric}_{window}",
        title=f"Top {n} stocks by {metric} ({window})",
        labels={
            "Ticker": "Ticker",
            f"{metric}_{window}": metric.capitalize()
        }
    )

    if metric == "volatility":
        fig.update_yaxes(tickformat=".1%")
    elif metric == "return":
        fig.update_yaxes(tickformat=".0%")

    return fig.to_html(
        full_html=True,
        include_plotlyjs="cdn"
    )

# Access the graph at: http://127.0.0.1:8000/api/graph?metric=Return&window=1y&n=5 or
# http://127.0.0.1:8000/api/graph?metric=Volatility&window=1y&n=5
# window and n are optional parameters with default values 1y and 5 respectively.