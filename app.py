import streamlit as st
import requests
import pandas as pd

ngrok_url = st.text_input("Enter the ngrok public URL for the Flask app", "https://4da0-35-196-87-17.ngrok-free.app/")

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
        df_forecast = pd.read_csv(pd.compat.StringIO(forecast_data))
        st.write(f"{forecast_type} Forecast for {item_id}")
        st.dataframe(df_forecast)
        st.download_button(
            label="Download data as CSV",
            data=df_forecast.to_csv().encode('utf-8'),
            file_name=f'{forecast_type}_forecast_{item_id}.csv',
            mime='text/csv',
        )
    else:
        st.write("Error retrieving forecast data")
