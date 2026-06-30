import pandas as pd
import os

print("=" * 50)
print("NeuralRetail - Data Ingestion Pipeline")
print("=" * 50)

os.makedirs('data/bronze', exist_ok=True)

print("\nLoading UCI Online Retail II dataset...")
df = pd.read_csv(r'C:\Neuralretail\data\raw\online_retail_II.csv', encoding='latin-1')
print(f"Raw data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

print("\nCleaning data...")
df_clean = df.dropna(subset=['Customer ID'])
df_clean = df_clean[~df_clean['Invoice'].astype(str).str.startswith('C')]
df_clean = df_clean[df_clean['Quantity'] > 0]
df_clean = df_clean[df_clean['Price'] > 0]
df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['Price']
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])

print(f"Clean data: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns")
print(f"Removed {df.shape[0] - df_clean.shape[0]} invalid rows")

print("\nSaving to Bronze Layer...")
df.to_parquet('data/bronze/retail_ii_raw.parquet', index=False)
df_clean.to_parquet('data/bronze/retail_ii_clean.parquet', index=False)

print("Bronze layer created!")
print("Files saved:")
print("  data/bronze/retail_ii_raw.parquet")
print("  data/bronze/retail_ii_clean.parquet")
print("=" * 50)
