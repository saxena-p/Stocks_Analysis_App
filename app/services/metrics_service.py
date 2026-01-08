import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "stock_metrics.csv"

class MetricsService:

    def __init__(self):
        self.metrics_df = self._load_metrics()
    
    def _load_metrics(self):
        df = pd.read_csv(DATA_PATH)
        print(f"Loaded metrics data from {DATA_PATH} with shape {df.shape} and columns {df.columns.tolist()}")
        if "Ticker" not in df.columns:
            raise ValueError("Expected 'Ticker' column in stock_metrics.csv")

        return df
    
    def available_metrics(self):
        """
        Infer available metrics from the columns of the metrics DataFrame.
        """
        return sorted(
            set(
                col.rsplit("_", 1)[0]
                for col in self.metrics_df.columns
                if col != "Ticker"
            )
        )
    
    def available_time_windows(self, metric: str):
        """
        Infer available time windows for a given metric.
        """

        return sorted(
            col.rsplit("_", 1)[1]
            for col in self.metrics_df.columns
            if col.startswith(metric + "_")
        )
    
    def top_n(self, metric: str, time_window: str, n: int):
        """
        Return the top n stocks for a given metric and time window.
        """
        
        col = f"{metric}_{time_window}"
        if col not in self.metrics_df.columns:
            raise ValueError(f"Metric '{col}' not found in metrics data.")
        
        out = (
            self.metrics_df[["Ticker", col]]
            .dropna()
            .sort_values(col, ascending=False)
            .head(n)
        )

        return out
