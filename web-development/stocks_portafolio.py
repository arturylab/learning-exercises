import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace with your Alpha Vantage API key
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# List of stocks in the portfolio
stocks = ["AMZN", "AAPL", "MSFT", "META", "GOOG", "V", "WMT", "KO", "MU", "NVDA"]

# Dictionary to store stock data
portfolio_changes = {}

# Function to fetch the latest and previous closing prices
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            dates = list(data["Time Series (Daily)"].keys())  # Get available dates
            latest_date = dates[0]  # Most recent trading day
            previous_date = dates[1]  # Previous trading day

            latest_close = float(data["Time Series (Daily)"][latest_date]["4. close"])
            previous_close = float(data["Time Series (Daily)"][previous_date]["4. close"])

            return latest_close, previous_close
        else:
            return None, None  # Data not available
    else:
        return None, None  # API Error

# Fetch stock prices while respecting API limits
for i, stock in enumerate(stocks):
    if i > 0 and i % 5 == 0:  # Wait after every 5 requests to avoid rate limits
        print("Waiting to respect API limits...")
        time.sleep(60)  # Wait 1 minute

    latest_price, previous_price = get_stock_data(stock)

    if latest_price is not None and previous_price is not None:
        price_change = latest_price - previous_price
        percentage_change = (price_change / previous_price) * 100
        portfolio_changes[stock] = {
            "Latest Price": latest_price,
            "Price Change": round(price_change, 2),
            "Percentage Change": round(percentage_change, 2)
        }
    else:
        portfolio_changes[stock] = {
            "Latest Price": "Error",
            "Price Change": "Error",
            "Percentage Change": "Error"
        }

# Print stock performance
print("\n📈 Portfolio Stock Changes:")
print(f"{'Stock':<6} {'Latest Price':<12} {'Change ($)':<12} {'Change (%)':<12}")
print("-" * 44)
for stock, data in portfolio_changes.items():
    print(f"{stock:<6} ${data['Latest Price']:<12} {data['Price Change']:<12} {data['Percentage Change']}%")
