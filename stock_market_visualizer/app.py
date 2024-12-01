import requests
from dotenv import load_dotenv
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import hashlib

# Step 1: Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment variables
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
BASE_URL = "https://www.alphavantage.co/query"

# Function to securely hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to handle user registration
def register():
    st.subheader("Register")
    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")

    if st.button("Register", key="register_button"):
        if not username or not email or not password:
            st.warning("Please fill in all the fields.")
        elif username in st.session_state['user_data']:
            st.warning("Username already exists!")
        elif password != confirm_password:
            st.warning("Passwords do not match!")
        else:
            st.session_state['user_data'][username] = {
                "email": email,
                "password": hash_password(password),
            }
            st.success("Registration successful! You can now log in.")

# Function to handle user login
def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        hashed_password = hash_password(password)
        if username in st.session_state['user_data'] and st.session_state['user_data'][username]["password"] == hashed_password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome, {username}")
        else:
            st.error("Invalid username or password")

# Function to handle user logout
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.info("You have logged out.")

# Function to fetch market data
def fetch_market_data(symbol):
    """Fetch market data for the provided stock symbol."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Error fetching data from API.")
        return None

# Function to plot stock trends
def plot_stock_trends(data, symbol):
    """Plot stock price trends using Plotly."""
    # Extracting the time series data for plotting
    time_series = data.get('Time Series (Daily)', {})
    dates = list(time_series.keys())
    close_prices = [float(time_series[date]['4. close']) for date in dates]
    high_prices = [float(time_series[date]['2. high']) for date in dates]
    low_prices = [float(time_series[date]['3. low']) for date in dates]
    open_prices = [float(time_series[date]['1. open']) for date in dates]

    # Create the plot
    fig = make_subplots(rows=1, cols=1)
    
    # Plot the closing prices
    fig.add_trace(
        go.Scatter(x=dates, y=close_prices, mode='lines', name=f'{symbol} Closing Prices'),
        row=1, col=1
    )

    # Plot the high prices
    fig.add_trace(
        go.Scatter(x=dates, y=high_prices, mode='lines', name=f'{symbol} High Prices', line=dict(dash='dot')),
        row=1, col=1
    )

    # Plot the low prices
    fig.add_trace(
        go.Scatter(x=dates, y=low_prices, mode='lines', name=f'{symbol} Low Prices', line=dict(dash='dash')),
        row=1, col=1
    )

    # Plot the opening prices
    fig.add_trace(
        go.Scatter(x=dates, y=open_prices, mode='lines', name=f'{symbol} Opening Prices', line=dict(dash='solid')),
        row=1, col=1
    )

    # Update the layout of the graph
    fig.update_layout(
        title=f"{symbol} Stock Price Trend",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=True,
        template="plotly_dark"
    )

    # Show the plot in the Streamlit app
    st.plotly_chart(fig)

# Step 2: Streamlit UI and interactivity
st.title('Stock Price Trends Visualizer')

# Initialize session state variables for login status and user data
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

# Navigation logic based on whether the user is logged in or not
if not st.session_state['logged_in']:
    # Show the registration or login option in the sidebar
    st.sidebar.title("Menu")
    option = st.sidebar.radio("Choose an option:", ("Register", "Login"))

    if option == "Register":
        register()
    elif option == "Login":
        login()
else:
    # Once logged in, allow access to stock price trends
    st.success(f"Logged in as {st.session_state['username']}")
    
    # Allow the user to enter a stock symbol
    symbol = st.text_input("Enter Stock Symbol", "AAPL")

    if symbol:
        # Fetch and plot the market data
        market_data = fetch_market_data(symbol)
        if market_data:
            plot_stock_trends(market_data, symbol)
        else:
            st.error(f"Failed to fetch data for {symbol}.")
    
    # Logout button
    if st.button("Logout", key="logout_button"):
        logout()
