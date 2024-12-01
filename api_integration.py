import requests
from dotenv import load_dotenv
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load environment variables from the .env file
load_dotenv()

# Fetch the API key from environment variables
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

BASE_URL = "https://www.alphavantage.co/query"

def fetch_market_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY",  # You can change this to other functions like TIME_SERIES_INTRADAY
        "symbol": symbol,
        "apikey": API_KEY
    }
    
    # Making the request to Alpha Vantage API
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error fetching data from API.")
        return None

def plot_stock_trends(data, symbol):
    # Extracting the time series data for plotting
    time_series = data.get('Time Series (Daily)', {})
    dates = list(time_series.keys())
    close_prices = [float(time_series[date]['4. close']) for date in dates]
    
    # Create the plot
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(
        go.Scatter(x=dates, y=close_prices, mode='lines', name=f'{symbol} Closing Prices'),
        row=1, col=1
    )
    
    fig.update_layout(
        title=f"{symbol} Stock Price Trend",
        xaxis_title="Date",
        yaxis_title="Closing Price (USD)",
        xaxis_rangeslider_visible=True,
        template="plotly_dark"
    )
    
    fig.show()

# Example usage
if __name__ == "__main__":
    symbol = "AAPL"  # Example: Fetch Apple stock data
    market_data = fetch_market_data(symbol)
    
    if market_data:
        print(f"Fetched data for {symbol}. Now displaying the trends...")
        plot_stock_trends(market_data, symbol)
    else:
        print(f"Failed to fetch data for {symbol}.")
