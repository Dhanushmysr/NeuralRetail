import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from prophet import Prophet
import mlflow

print("Loading data...")
df = pd.read_csv(r'C:\Neuralretail\data\processed\clean_data.csv')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Prepare daily sales for Prophet
daily_sales = df.groupby(df['InvoiceDate'].dt.date)['TotalAmount'].sum().reset_index()
daily_sales.columns = ['ds', 'y']
daily_sales['ds'] = pd.to_datetime(daily_sales['ds'])

print("Training Prophet model...")
model = Prophet(seasonality_mode='multiplicative')
model.fit(daily_sales)

# Forecast next 30 days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

print("Forecast for next 30 days:")
print(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail(30))

forecast.to_csv(r'C:\Neuralretail\data\features\forecast.csv', index=False)
print("Forecast saved!")
