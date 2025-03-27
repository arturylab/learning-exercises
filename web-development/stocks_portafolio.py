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
def get_stock_data(symbol: str) -> float:
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues (4xx, 5xx)
        data = response.json()

        # Detect API limit exceeded
        if "Note" in data:
            print(f"⚠️ API limit reached: {data['Note']}")
            return None, None, "API Limit Exceeded"

        # Detect general API errors
        if "Error Message" in data:
            print(f"❌ API Error for {symbol}: {data['Error Message']}")
            return None, None, "API Error"

        # Validate response format
        if "Time Series (Daily)" in data:
            dates = list(data["Time Series (Daily)"].keys())
            latest_date = dates[0]  # Most recent trading day
            previous_date = dates[1]  # Previous trading day

            latest_close = float(data["Time Series (Daily)"][latest_date]["4. close"])
            previous_close = float(data["Time Series (Daily)"][previous_date]["4. close"])

            return latest_close, previous_close, None  # No error

        print(f"❌ Unexpected data format for {symbol}: {data}")
        return None, None, "Unexpected Data Format"

    except requests.exceptions.RequestException as e:
        print(f"🚨 Request error for {symbol}: {e}")
        return None, None, "Request Error"
    except (KeyError, ValueError) as e:
        print(f"⚠️ Data parsing error for {symbol}: {e}")
        return None, None, "Data Parsing Error"

# Fetch stock prices while respecting API limits
for i, stock in enumerate(stocks):
    # if i > 0 and i % 5 == 0:  # Wait after every 5 requests to avoid rate limits
    #     print("⏳ Waiting to respect API limits...")
    #     time.sleep(60)  # Wait 1 minute

    latest_price, previous_price, error = get_stock_data(stock)

    if latest_price is not None and previous_price is not None:
        price_change = latest_price - previous_price
        percentage_change = (price_change / previous_price) * 100
        portfolio_changes[stock] = {
            "Latest Price": latest_price,
            "Price Change": round(price_change, 2),
            "Percentage Change": round(percentage_change, 2),
            "Error": None
        }
    else:
        portfolio_changes[stock] = {
            "Latest Price": "Error",
            "Price Change": "Error",
            "Percentage Change": "Error",
            "Error": error
        }

# Print stock performance
print("\n📈 Portfolio Stock Changes:")
print(f"{'Stock':<6} {'Latest Price':<12} {'Change ($)':<12} {'Change (%)':<12} {'Error':<20}")
print("-" * 64)
for stock, data in portfolio_changes.items():
    print(f"{stock:<6} ${data['Latest Price']:<12} {data['Price Change']:<12} {data['Percentage Change']:<12} {data['Error']}")
