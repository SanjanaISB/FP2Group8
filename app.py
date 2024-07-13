import streamlit as st
import pandas as pd
from pyngrok import ngrok

# Set your ngrok authentication token
ngrok.set_auth_token("2i2b7uISHbU7rD56WmdQwTwmo6u_6jnKEvV6HAbk7kNHLCjUB")

# Function to filter out weekends
def filter_weekends(df):
    df['Date'] = pd.to_datetime(df['Timestamp'])
    df = df[~df['Date'].dt.dayofweek.isin([5, 6])]
    df = df.drop(columns=['Date'])
    return df

# Start ngrok tunnel
public_url = ngrok.connect(8501)
st.write(f' * ngrok tunnel "http://127.0.0.1:8501" -> "{public_url}"')

# Streamlit app
st.title("Forecast Dashboard")

# Navigation
pages = ["Home", "Short Term Forecast", "Long Term Forecast"]
selection = st.sidebar.radio("Go to", pages)

if selection == "Home":
    st.header("Home")
    st.markdown("""
        <ul>
            <li><a href="#" onclick="document.querySelector('input[value=Short\\ Term\\ Forecast]').click()">Short Term Forecast</a></li>
            <li><a href="#" onclick="document.querySelector('input[value=Long\\ Term\\ Forecast]').click()">Long Term Forecast</a></li>
        </ul>
    """, unsafe_allow_html=True)

elif selection == "Short Term Forecast":
    st.header("Short Term Forecast")
    df = pd.read_csv('Short_term_forecast_results.csv')
    st.dataframe(df)

elif selection == "Long Term Forecast":
    st.header("Long Term Forecast")
    df = pd.read_csv('Long_term_forecast_results.csv')
    st.dataframe(df)

# Run the Streamlit app
if __name__ == '__main__':
    st.write("Running Streamlit app...")
