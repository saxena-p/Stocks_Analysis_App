import pandas as pd
import yfinance as yf
from universe import high_cap

ftse100 = pd.read_csv('ftse100.csv', index_col=0)
ftse100['Ticker (on LSE)'] = ftse100['Ticker (on LSE)'] + '.L'
stocks_list = ftse100['Ticker (on LSE)'].tolist()

print("Fetching data for all stocks in ftse100.csv from Yahoo! Finance.")
print("Total stocks to fetch:", len(stocks_list))

def fetch_stock_data(tickers = stocks_list):
    data = []
    for ticker in tickers:
        df = yf.download(ticker, period="5y", auto_adjust=True)
        data.append(df)
    
    full_data = pd.concat(data, axis = 1)
    full_data.to_csv("stock_data.csv")
    print("Data fetched and saved to stock_data.csv")
    

if __name__ == "__main__":
    fetch_stock_data()
    