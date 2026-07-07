import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("Loading data...")
df = pd.read_csv(r'C:\Neuralretail\data\processed\clean_data.csv')
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

print("Data loaded:", df.shape)
print("Total Revenue:", round(df['TotalAmount'].sum(), 2))
print("Total Customers:", df['Customer ID'].nunique())
print("Total Products:", df['StockCode'].nunique())
