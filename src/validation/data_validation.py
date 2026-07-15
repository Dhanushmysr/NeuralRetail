import pandas as pd
import numpy as np
import os

print("=" * 50)
print("NeuralRetail - Data Quality Validation")
print("=" * 50)

os.makedirs('reports', exist_ok=True)

df = pd.read_csv(r'C:\Neuralretail\data\raw\online_retail_II.csv', encoding='latin-1')

print("\n1. BASIC INFO")
print(f"Total Rows: {df.shape[0]}")
print(f"Total Columns: {df.shape[1]}")
print(f"Columns: {df.columns.tolist()}")

print("\n2. MISSING VALUES")
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
print(missing_df)

print("\n3. DUPLICATE ANALYSIS")
duplicates = df.duplicated().sum()
print(f"Duplicate rows: {duplicates}")
print(f"Duplicate %: {round(duplicates/len(df)*100, 2)}%")

print("\n4. DATA VALIDATION RULES")
cancelled = df['Invoice'].astype(str).str.startswith('C').sum()
negative_qty = (df['Quantity'] < 0).sum()
negative_price = (df['Price'] < 0).sum()
zero_price = (df['Price'] == 0).sum()
print(f"Cancelled orders: {cancelled}")
print(f"Negative quantities: {negative_qty}")
print(f"Negative prices: {negative_price}")
print(f"Zero prices: {zero_price}")

print("\n5. DATA QUALITY SCORE")
total_issues = missing['Customer ID'] + duplicates + cancelled + negative_qty + negative_price
quality_score = round((1 - total_issues/len(df)) * 100, 2)
print(f"Data Quality Score: {quality_score}%")

report = f"""
DATA QUALITY REPORT - NeuralRetail
====================================
Dataset: UCI Online Retail II
Total Rows: {df.shape[0]}
Total Columns: {df.shape[1]}

MISSING VALUES:
{missing_df.to_string()}

DUPLICATES: {duplicates} rows ({round(duplicates/len(df)*100,2)}%)

VALIDATION RULES:
- Cancelled Orders: {cancelled}
- Negative Quantities: {negative_qty}
- Negative Prices: {negative_price}
- Zero Prices: {zero_price}

DATA QUALITY SCORE: {quality_score}%
"""

with open('reports/data_quality.txt', 'w') as f:
    f.write(report)

print("Report saved!")
print("=" * 50)
