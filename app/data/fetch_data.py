import pandas as pd
import yfinance as yf
from universe import high_cap

print ("Fetching data for high cap stocks:", high_cap)

def fetch_stock_data(tickers = high_cap):
    data = []
    for ticker in tickers:
        df = yf.download(ticker, period="6mo", auto_adjust=True)
        data.append(df)
    
    full_data = pd.concat(data, axis = 1)
    full_data.to_csv("stock_data.csv")
    print("Data fetched and saved to stock_data.csv")
    

if __name__ == "__main__":
    fetch_stock_data()
    