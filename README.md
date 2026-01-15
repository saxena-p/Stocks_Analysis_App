# Stock Analysis App

A container-ready stock analysis backend that ranks stocks by performance metrics over selectable time windows.     
This MVP is designed to be deployed on Azure and embedded into a personal webpage.



## 🚀 Current Status

**Phase 2 complete**

✔ Data pipeline implemented (CSV-based)  
✔ FastAPI backend implemented  
✔ Metrics validated and exposed via REST API  
✔ Error handling and input validation in place  
✔ Deployed on Azure via a Docker container -  https://stock-analysis-app-unique.azurewebsites.net/


## 📌 Features (MVP)

- Uses **historical stock data (last 5 years)**
- Supports ranking stocks by:
  - Percentage return
  - Volatility
  - P/E ratio
  - Market capitalisation
- User-selectable:
  - Metric
  - Time window (e.g. 3m, 6m, 1y, 3y, 5y)
  - Top-N results
- Clean, discoverable REST API
- Designed for daily scheduled data updates

---

## 🗂 Project Structure

```
project_root/
├── app/
│   ├── init.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # App configuration & paths
│   ├── api/
│   │   ├── init.py
│   │   ├── routes.py        # API endpoints
│   │   └── schemas.py       # Pydantic response models
│   ├── services/
│   │   ├── init.py
│   │   └── metrics_service.py  # Business logic
│   ├── static/
│   │   └── index.html
│   ├── templates/
│   │   └── main.js
│   └── data/
│        └── stock_metrics.csv      # Precomputed metrics (data contract)
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

## 📊 Data Contract

The backend expects a **CSV file** at: app/data/stock_metrics.csv

### Example header and rows in the file
```csv
Ticker,Return_5d,Return_1mo,Return_3mo,Return_1y,Return_3y,Volatility_5d,Volatility_1mo,Volatility_3mo,Volatility_1y,Volatility_3y,Market-Cap,PE-Ratio
AAF.L,-1.2213063969768816,12.916512011387098,60.329010056575896,190.1913684199643,208.6160134124031,0.13650735005880443,0.24256098878705787,0.3770660396642202,0.3364153705502581,0.3016241050754023,1311791222469.5054,3597.9998779296875
AAL.L,4.725415070242656,12.060129825760164,27.32919254658385,35.94085776158907,-8.860444862688402,0.24374065975958314,0.28158378622111235,0.28462986563395953,0.36111470166593335,0.3827888959343813,3496340035188.0,
```

## 🧪 Running Locally

1. Install dependencies
```
pip install -r requirements.txt
```

2. Get updated data for all stocks.

```
cd app/data
python fetch_data.py
python compute_metrics.py
```
This should update the files stock_data.csv and stock_metrics.csv with the latest information.

3. Run from project root
```
uvicorn app.main:app --reload
```

4. Open in Browser
- Visualisation via frontend:         http://127.0.0.1:8000/
- API docs (Swagger):   http://127.0.0.1:8000/docs
<!-- - View results graphically: http://127.0.0.1:8000/api/graph?metric=Return&window=1y&n=5 -->

![Returns](Readme_figs/returns_1y.png)



## ✅ Verification Checklist

The app is working correctly if:

- / returns { "status": "ok" }

- /docs loads without errors

- /api/top returns ranked results

- Invalid metrics/windows return HTTP 400

- Restarting the app produces no schema errors


## 🔜 Next Steps

Planned next phases:

- Azure function for daily data updates (11 PM)
<!-- - Frontend visualisation (Plotly / JavaScript) -->
- ML-based predictions


## 🧠 Design Principles

- Data contract first
- Flat tables for APIs
- Explicit schema validation
- Container- and cloud-first design
- Minimal MVP scope for easy extensions in future

## 👤 Author
Built as a pesonal stock analysis and visualisation project by Prashant Saxena. Designed for public deployment and experimentation.