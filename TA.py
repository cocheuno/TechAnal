import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta

# Function to simulate trades and calculate portfolio value
def simulate_trades(data):
    initial_cash = 10000
    cash = initial_cash
    shares = 0
    portfolio_value = initial_cash
    trades = []

    for date, row in data.iterrows():
        if row['Golden_Cross'] and cash >= row['Close']:
            # Buy 1 share
            shares += 1
            cash -= row['Close']
            trades.append({'Date': date, 'Type': 'Buy', 'Price': row['Close']})
        elif row['Death_Cross'] and shares > 0:
            # Sell 1 share
            shares -= 1
            cash += row['Close']
            trades.append({'Date': date, 'Type': 'Sell', 'Price': row['Close']})
        
        # Update portfolio value
        portfolio_value = cash + (shares * row['Close'])
    
    return trades, portfolio_value

# Function to print trades and calculate profit/loss
def print_trades_and_summary(trades, final_portfolio_value):
    annual_profit_loss = {}
    for trade in trades:
        year = trade['Date'].year
        if trade['Type'] == 'Sell':
            profit_loss = trade['Price'] - trades[trades.index(trade) - 1]['Price']
            annual_profit_loss.setdefault(year, 0)
            annual_profit_loss[year] += profit_loss
            print(f"{trade['Date'].date()} - {trade['Type']} at {trade['Price']:.2f}, Profit/Loss: {profit_loss:.2f}")
        else:
            print(f"{trade['Date'].date()} - {trade['Type']} at {trade['Price']:.2f}")

    print("\nAnnual Profit/Loss:")
    for year, pnl in annual_profit_loss.items():
        print(f"{year}: {pnl:.2f}")

    print(f"\nFinal Portfolio Value: {final_portfolio_value:.2f}")

# Assuming the above functions are correctly fetching and processing data
# This block is to simulate trades based on golden and death crosses and print the results
# trades, final_portfolio_value = simulate_trades(msft_data)
# print_trades_and_summary(trades, final_portfolio_value)

# NOTE: The above function calls are commented out to prevent execution in an environment where dependencies might be missing. 
# Please uncomment and run in a suitable environment.
