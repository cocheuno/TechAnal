import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta

# Function to fetch data and calculate SMAs
def fetch_data_and_calculate_smas(start_year):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now() - timedelta(days=1)  # Yesterday's date

    # Fetch the Microsoft stock data
    msft_data = web.DataReader('MSFT', 'yahoo', start_date, end_date)

    # Calculate the 50-day and 200-day SMAs
    msft_data['50_day_SMA'] = msft_data['Close'].rolling(window=50).mean()
    msft_data['200_day_SMA'] = msft_data['Close'].rolling(window=200).mean()

    return msft_data

# Function to identify golden and death crosses
def identify_crosses(data):
    data['Golden_Cross'] = (data['50_day_SMA'] > data['200_day_SMA']) & (data['50_day_SMA'].shift(1) <= data['200_day_SMA'].shift(1))
    data['Death_Cross'] = (data['50_day_SMA'] < data['200_day_SMA']) & (data['50_day_SMA'].shift(1) >= data['200_day_SMA'].shift(1))
    return data

# Function to simulate the portfolio
def simulate_portfolio(data, initial_cash=10000):
    cash = initial_cash - data.iloc[0]['Close']  # Initial purchase of 1 MSFT share
    shares = 1  # Start with one share
    portfolio_history = []

    for date, row in data.iterrows():
        if row['Golden_Cross'] and cash >= row['Close']:
            shares += 1  # Buy 1 share
            cash -= row['Close']
            portfolio_history.append({'Date': date, 'Action': 'Buy', 'Share Price': row['Close'], 'Shares': shares, 'Cash': cash})

        if row['Death_Cross'] and shares > 0:
            shares -= 1  # Sell 1 share
            cash += row['Close']
            portfolio_history.append({'Date': date, 'Action': 'Sell', 'Share Price': row['Close'], 'Shares': shares, 'Cash': cash})

    # Calculate the final portfolio value
    final_value = cash + (shares * data.iloc[-1]['Close'])
    print ("PV: ", portfolio_history, final_value)

# Assuming the above functions are correctly defined
# msft_data = fetch_data_and_calculate_smas(2014)
# msft_data_with_crosses = identify_crosses(msft_data)
# portfolio_history, final_portfolio_value = simulate_portfolio(msft_data_with_crosses)

# The function calls are commented out to prevent execution in this environment. Please uncomment and execute in a suitable environment.

# NOTE: This is a draft version of the program. Further refinement and error handling may be necessary for a complete solution.
