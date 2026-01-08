from pathlib import Path
import os

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Data paths
DATA_DIR = BASE_DIR / "data"
METRICS_PATH = DATA_DIR / "stock_metrics.csv"

# App settings
APP_NAME = os.getenv("APP_NAME", "Stock Analysis MVP")
APP_ENV = os.getenv("APP_ENV", "local")

# API settings
MAX_TOP_N = int(os.getenv("MAX_TOP_N", 100))