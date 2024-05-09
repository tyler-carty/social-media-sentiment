import requests
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

# Set up the Alpha Vantage API key
api_key = "3OXMTNLZ5YL9HJQ2"  # Replace with your actual API key

# Set the stock symbols and date range
stock_symbols = ["GME", "AMC"]
start_date = "2021-01-01"
end_date = "2021-02-28"

# Initialize an empty dictionary to store the stock data
stock_data = {}

# Retrieve stock data for each symbol
for symbol in stock_symbols:
    # Set up the Alpha Vantage API parameters
    ts = TimeSeries(key=api_key, output_format="pandas")

    # Retrieve the daily stock data
    data, _ = ts.get_daily(symbol=symbol, outputsize="full")

    # Convert the index to a DatetimeIndex
    data.index = pd.to_datetime(data.index)

    # Create a new DatetimeIndex with the desired date range
    date_range = pd.date_range(start=start_date, end=end_date)

    # Reindex the data with the new DatetimeIndex and fill missing values
    data = data.reindex(date_range, fill_value=None)

    # Store the stock data in the dictionary
    stock_data[symbol] = data

# Concatenate the stock data into a single DataFrame
all_stock_data = pd.concat(stock_data.values(), keys=stock_data.keys(), axis=1)

# Print the stock data
print(all_stock_data)

# Save the stock data to a CSV file
all_stock_data.to_csv("gme_amc_stock_data.csv")