import boto3
import pandas as pd
import streamlit as st

# Initialize a session using Amazon Forecast
session = boto3.Session(
    aws_access_key_id='AKIA47CRXULRB2H562MZ',
    aws_secret_access_key='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',
    region_name='ap-south-1'
)

# Create a Forecast client
forecast = session.client('forecast')
forecast_query = session.client('forecastquery')

def filter_weekends(df):
    df['Date'] = pd.to_datetime(df['Timestamp'])
    df = df[~df['Date'].dt.dayofweek.isin([5, 6])]
    df = df.drop(columns=['Date'])
    return df

def get_forecast(forecast_arn, item_id):
    # Query the forecast
    forecast_response = forecast_query.query_forecast(
        ForecastArn=forecast_arn,
        Filters={"item_id": item_id}
    )

    # Extract the forecast data
    forecast_data = forecast_response['Forecast']['Predictions']

    # Check if 'p50' key exists in the predictions
    if 'p50' in forecast_data:
        # Convert to DataFrame
        df_forecast = pd.DataFrame(forecast_data['p50'])
        # Filter out weekends
        df_forecast = filter_weekends(df_forecast)
        return df_forecast
    else:
        st.write(f"No predictions found for item_id: {item_id}")
        return pd.DataFrame()

# Streamlit UI
st.title("Forecast Dashboard")

item_id = st.text_input("Enter Stock Name", "Britannia")
forecast_type = st.selectbox("Select Forecast Type", ["Short Term", "Long Term"])

if st.button("Get Forecast"):
    if forecast_type == "Short Term":
        forecast_arn = 'arn:aws:forecast:ap-south-1:891377132258:forecast/FP2Forecast'
    else:
        forecast_arn = 'arn:aws:forecast:ap-south-1:891377132258:forecast/FP2Forecast2'
    
    df_forecast = get_forecast(forecast_arn, item_id)
    if not df_forecast.empty:
        st.write(f"{forecast_type} Forecast for {item_id}")
        st.dataframe(df_forecast)
        st.download_button(
            label="Download data as CSV",
            data=df_forecast.to_csv().encode('utf-8'),
            file_name=f'{forecast_type}_forecast_{item_id}.csv',
            mime='text/csv',
        )

# This part is not needed for Streamlit; you run the app using the command line
# if __name__ == "__main__":
#     st.run()
