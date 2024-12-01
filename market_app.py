import streamlit as st
from api_integration import fetch_market_data  # Import the function from the API script

# Streamlit UI for User Input
st.title("Market Data Dashboard")
st.write("Welcome to the market data dashboard. Enter the stock symbol to get real-time data.")

symbol = st.text_input("Enter Stock Symbol", "AAPL")  # Default: AAPL (Apple)

if st.button("Fetch Data"):
    if symbol:
        st.write(f"Fetching data for {symbol}...")
        data = fetch_market_data(symbol)  # Call the API function
        if data:
            st.json(data)  # Display raw JSON data (for now, can format later)
        else:
            st.error("Failed to retrieve data.")
    else:
        st.warning("Please enter a valid stock symbol.")
