import streamlit as st
import requests
import pandas as pd
from io import StringIO

# Input ngrok URL from the user
ngrok_url = st.text_input("Enter the ngrok public URL for the Flask app", "http://your-ngrok-url")

st.title("Forecast Dashboard")

item_id = st.text_input("Enter Stock Name", "Britannia")
forecast_type = st.selectbox("Select Forecast Type", ["Short Term", "Long Term"])

if st.button("Get Forecast"):
    data = {
        'item_id': item_id,
        'forecast_type': forecast_type
    }
    response = requests.post(f'{ngrok_url}/get_forecast', data=data)
    
    if response.status_code == 200:
        forecast_data = response.text
        df_forecast = pd.read_csv(StringIO(forecast_data))
        st.write(f"{forecast_type} Forecast for {item_id}")
        st.dataframe(df_forecast)
        st.download_button(
            label="Download data as CSV",
            data=df_forecast.to_csv().encode('utf-8'),
            file_name=f'{forecast_type}_forecast_{item_id}.csv',
            mime='text/csv',
        )
    else:
        st.write("Error retrieving forecast data or no data found.")
        st.write(response.text)
