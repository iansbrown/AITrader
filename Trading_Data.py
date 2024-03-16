#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 12:55:26 2024

@author: ianbrown
"""
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import pandas as pd

def get_stock_data(ticker_symbols):
    # Alpaca API credentials
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    base_url = 'https://paper-api.alpaca.markets'  # Change to live URL if using live account

    # Initialize Alpaca API
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

    # Calculate start and end dates for querying data (5 years ago from today)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)

    # Convert dates to string in YYYY-MM-DD format
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Create an empty DataFrame to store historical data
    df = pd.DataFrame()

    # Iterate through each ticker symbol and fetch historical data
    for ticker_symbol in ticker_symbols:
        try:
            historical_data = api.get_barset(ticker_symbol, 'minute', limit=None, start=start_date_str, end=end_date_str)
            stock_data = historical_data[ticker_symbol]
            for bar in stock_data:
                df = df.append({
                    'symbol': ticker_symbol,
                    'timestamp': bar.t,
                    'open': bar.o,
                    'high': bar.h,
                    'low': bar.l,
                    'close': bar.c,
                    'volume': bar.v
                }, ignore_index=True)
        except Exception as e:
            print(f"Error fetching data for {ticker_symbol}: {e}")

    return df
'''
Example usage of get_stock_data

ticker_symbols = ['AAPL', 'MSFT', 'GOOGL']  # Replace with any list of stock ticker symbols
stock_data_df = get_stock_data(ticker_symbols)

print(stock_data_df)
'''

def write_dataframe_to_csv(dataframe, filename):
    try:
        dataframe.to_csv(filename, index=False)
        print(f"DataFrame successfully written to {filename}")
    except Exception as e:
        print(f"Error writing DataFrame to CSV file: {e}")
'''
Example usage of write_dataframe_to_csv
output_filename = "stock_data.csv"
write_dataframe_to_csv(stock_data_df, output_filename)
'''