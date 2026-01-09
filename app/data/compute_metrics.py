import pandas as pd
import yfinance as yf
import numpy as np
from datetime import date, timedelta

# Metrics to compute
# 1. Percentage return over a given time window
# 2. Volatility over a given time window
# 3. Latest market capitalization
# 4. Latest P/E ratio

# 1. Percentage return over a given time window

## Refactor all functions to remove start_date and instead take number of days as input

# def compute_percentage_return(data, ticker, start_date, end_date):
#     """
#     Compute the percentage return for a given ticker between start_date and end_date.
    
#     Parameters:
#     data (DataFrame): DataFrame containing stock data with MultiIndex columns (Attribute, Ticker)
#     ticker (str): Stock ticker symbol
#     start_date (str): Start date in 'YYYY-MM-DD' format
#     end_date (str): End date in 'YYYY-MM-DD' format
    
#     Returns:
#     float: Percentage return
#     """
#     start_price = data.loc[start_date, ('Close', ticker)]
#     end_price = data.loc[end_date, ('Close', ticker)]
#     percentage_return = ((end_price - start_price) / start_price) * 100
#     return percentage_return

def compute_percentage_return(data, ticker, num_days):
    """
    Compute the percentage return for a given ticker over the last num_days.
    
    Parameters:
    data (DataFrame): DataFrame containing stock data with MultiIndex columns (Attribute, Ticker)
    ticker (str): Stock ticker symbol
    num_days (int): Number of days to compute the return over
    end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
    float: Percentage return
    """

    end_price = data.iloc[-1][('Close', ticker)]
    start_price = data.iloc[-1-num_days][('Close', ticker)]
    percentage_return = ((end_price - start_price) / start_price) * 100
    return percentage_return


# 2. Volatility over a given time window
# Method: First compute log returns, then compute standard deviation of log returns, then annualize it.

# def compute_volatility(data, ticker, start_date, end_date):
#     """
#     Compute the annualized volatility for a given ticker between start_date and end_date.
    
#     Parameters:
#     data (DataFrame): DataFrame containing stock data with MultiIndex columns (Attribute, Ticker)
#     ticker (str): Stock ticker symbol
#     start_date (str): Start date in 'YYYY-MM-DD' format
#     end_date (str): End date in 'YYYY-MM-DD' format
    
#     Returns:
#     float: Annualized volatility
#     """
#     price_data = data.loc[start_date:end_date, ('Close', ticker)]
#     log_returns = np.log(price_data / price_data.shift(1)).dropna()
#     volatility = log_returns.std() * np.sqrt(252)  # Assuming 252 trading days in a year
#     return volatility

def compute_volatility(data, ticker, num_days):
    """
    Compute the annualized volatility for a given ticker over the last num_days.
    
    Parameters:
    data (DataFrame): DataFrame containing stock data with MultiIndex columns (Attribute, Ticker)
    ticker (str): Stock ticker symbol
    num_days (int): Number of days to compute the volatility over
    end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
    float: Annualized volatility
    """
    price_data = data.iloc[-1-num_days:-1][('Close', ticker)]
    log_returns = np.log(price_data / price_data.shift(1)).dropna()
    volatility = log_returns.std() * np.sqrt(252)  # Assuming 252 trading days in a year
    return volatility

# 3. Latest market capitalization
# def get_latest_market_cap(ticker):
#     """
#     Placeholder function to get the latest market capitalization for a given ticker.
    
#     Parameters:
#     ticker (str): Stock ticker symbol
    
#     Returns:
#     float: Latest market capitalization
#     """
    
#     ticker = yf.Ticker(ticker)
#     market_cap = ticker.fast_info['marketCap']
#     return market_cap

# Rewriting the above function to handle cases where marketCap might not be available
def get_latest_market_cap(ticker):
    """
    Returns market capitalization for a given ticker.

    Parameters:
    ticker (str): Stock ticker symbol
    
    Returns:
    float: Latest market capitalization
    """
    
    ticker = yf.Ticker(ticker)
    try:
        market_cap = ticker.fast_info['marketCap']
    except Exception as e:
        market_cap = None

    return market_cap

# 4. Latest P/E ratio
def get_latest_pe_ratio(ticker):
    """
    Placeholder function to get the latest P/E ratio for a given ticker.
    
    Parameters:
    ticker (str): Stock ticker symbol
    
    Returns:
    float: Latest P/E ratio
    """
    
    ticker = yf.Ticker(ticker)
    price = ticker.fast_info.get("lastPrice")
    eps = ticker.info.get("trailingEps")

    if price is not None and eps is not None and eps > 0:
        pe_ratio = price / eps
    else:
        pe_ratio = None

    return pe_ratio

if __name__ == "__main__":

    '''
    This default function calculates key metrics for a the tickers in stock_data.csv and stores output in a CSV.
    '''
    data = pd.read_csv("stock_data.csv", header=[0,1], index_col=0, parse_dates=True)
    tickers = data.columns.levels[1]
    # print("Computing metrics for tickers:", tickers)

    metrics = pd.DataFrame(columns=['Ticker', 'Return_5d', 'Return_1mo', 'Return_3mo', 'Return_1y', 'Volatility_3mo','Volatility_1y', 'Market-Cap', 'PE-Ratio'])
    
    # end_date is the date of last working day
    yesterday = date.today() - timedelta(days=1)
    last_day = yesterday
    if yesterday.weekday() == 5:
        last_day = yesterday - timedelta(days=1)
    elif yesterday.weekday() == 6:
        last_day = yesterday - timedelta(days=2)
    else:
        last_day = yesterday

    # Convert to string format
    end_date = last_day.strftime("%Y-%m-%d") # Yesterday
    start_date_5d = (last_day - timedelta(days=7)).strftime("%Y-%m-%d") # 1 week ago
    start_date_1mo = (last_day - timedelta(days=28)).strftime("%Y-%m-%d") # 4 weeks ago
    start_date_3mo = (last_day - timedelta(days=84)).strftime("%Y-%m-%d") # 12 weeks ago


    # Now compute the metrics for each ticker
    for ticker in tickers:
        ret_5d = compute_percentage_return(data, ticker, 5)
        # print("5D Return for", ticker, "is", ret_5d)

        ret_1mo = compute_percentage_return(data, ticker, 28)
        # print("1M Return for", ticker, "is", ret_1mo)

        ret_3mo = compute_percentage_return(data, ticker, 84)
        # print("3M Return for", ticker, "is", ret_3mo)

        ret_1y = compute_percentage_return(data, ticker, 252)
        # print("1Y Return for", ticker, "is", ret_1y)

        vol_3mo = compute_volatility(data, ticker, 84)
        # print("3M Volatility for", ticker, "is", vol_3mo)

        vol_1y = compute_volatility(data, ticker, 252)
        # print("1Y Volatility for", ticker, "is", vol_1y)

        market_cap = get_latest_market_cap(ticker)
        # print("Market Cap for", ticker, "is", market_cap)

        pe_ratio = get_latest_pe_ratio(ticker)
        # print("P/E Ratio for", ticker, "is", pe_ratio)

        new_row = pd.DataFrame([{
            'Ticker': ticker,
            'Return_5d': ret_5d,
            'Return_1mo': ret_1mo,
            'Return_3mo': ret_3mo,
            'Return_1y': ret_1y,
            'Volatility_3mo': vol_3mo,
            'Volatility_1y': vol_1y,
            'Market-Cap': market_cap,
            'PE-Ratio': pe_ratio
        }])
        # metrics = pd.concat([metrics, new_row], ignore_index=True)
        metrics.loc[len(metrics)] = new_row.iloc[0]
        print("Metrics computed for", ticker)
    
    metrics.to_csv("stock_metrics.csv", index=False)
    print("Metrics computed and saved to stock_metrics.csv")
