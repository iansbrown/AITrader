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


def create_training_dataset(dataframe, percent_difference=5, output_filename="training_dataset.csv"):
    with open(output_filename, 'w') as f:
        f.write("timestamp,open,high,low,close,volume,label\n")
        
        for symbol in dataframe['symbol'].unique():
            symbol_data = dataframe[dataframe['symbol'] == symbol]
            
            # Find daily max value
            daily_max = symbol_data['high'].max()
            daily_max_time = symbol_data.loc[symbol_data['high'].idxmax()]['timestamp']
            
            # Find local minimum ticker value before daily max
            local_min = symbol_data.loc[(symbol_data['timestamp'] < daily_max_time) & 
                                        (symbol_data['timestamp'] >= daily_max_time - timedelta(minutes=30)), 'low'].min()
            
            if (daily_max - local_min) / local_min > percent_difference / 100 and daily_max_time.hour * 60 + daily_max_time.minute > 30:
                local_min_time = symbol_data.loc[(symbol_data['timestamp'] < daily_max_time) & 
                                                 (symbol_data['timestamp'] >= daily_max_time - timedelta(minutes=30)), 'timestamp'].idxmin()
                
                f.write_data(symbol_data.loc[local_min_time - timedelta(minutes=30):local_min_time + timedelta(minutes=10)].to_csv(index=False))
                f.write("buy\n")
            
            # Find daily min value
            daily_min = symbol_data['low'].min()
            daily_min_time = symbol_data.loc[symbol_data['low'].idxmin()]['timestamp']
            
            # Find local maximum ticker value before daily min
            local_max = symbol_data.loc[(symbol_data['timestamp'] < daily_min_time) & 
                                        (symbol_data['timestamp'] >= daily_min_time - timedelta(minutes=30)), 'high'].max()
            
            if (local_max - daily_min) / daily_min > percent_difference / 100 and daily_min_time.hour * 60 + daily_min_time.minute > 30:
                local_max_time = symbol_data.loc[(symbol_data['timestamp'] < daily_min_time) & 
                                                 (symbol_data['timestamp'] >= daily_min_time - timedelta(minutes=30)), 'timestamp'].idxmax()
                
                f.write_data(symbol_data.loc[local_max_time - timedelta(minutes=30):local_max_time + timedelta(minutes=10)].to_csv(index=False))
                f.write("sell\n")
'''
# Example usage
create_training_dataset(stock_data_df)
'''