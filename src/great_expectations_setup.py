import pandas as pd
import json
import os

print("=" * 50)
print("NeuralRetail - Data Validation Checks")
print("=" * 50)

# Load data
df = pd.read_csv(r'C:\Neuralretail\data\raw\online_retail_II.csv', encoding='latin-1')

print("\nRunning quality checks...")

# Define all checks
checks = []

def check(name, result, expected=True):
    status = "PASSED" if result == expected else "FAILED"
    checks.append({"check": name, "status": status})
    print(f"  [{status}] {name}")

# Column existence checks
check("Column Invoice exists", "Invoice" in df.columns)
check("Column Customer ID exists", "Customer ID" in df.columns)
check("Column Price exists", "Price" in df.columns)
check("Column Quantity exists", "Quantity" in df.columns)
check("Column InvoiceDate exists", "InvoiceDate" in df.columns)
check("Column StockCode exists", "StockCode" in df.columns)
check("Column Country exists", "Country" in df.columns)

# Null checks
check("Invoice has no nulls", df['Invoice'].isnull().sum() == 0)
check("InvoiceDate has no nulls", df['InvoiceDate'].isnull().sum() == 0)
check("Price has no nulls", df['Price'].isnull().sum() == 0)
check("Quantity has no nulls", df['Quantity'].isnull().sum() == 0)

# Range checks
check("Price >= 0 for most rows", (df['Price'] >= 0).mean() > 0.95)
check("Quantity range is valid", df['Quantity'].between(-100000, 100000).all())

# Row count check
check("Dataset has more than 1000 rows", len(df) > 1000)

# Duplicates check
check("Duplicates under 5%", df.duplicated().mean() < 0.05)

# Summary
passed = sum(1 for c in checks if c['status'] == 'PASSED')
failed = sum(1 for c in checks if c['status'] == 'FAILED')
total = len(checks)

print(f"\nValidation Results:")
print(f"Total Checks : {total}")
print(f"Passed       : {passed}")
print(f"Failed       : {failed}")
print(f"Success Rate : {round(passed/total*100, 2)}%")

# Save results
os.makedirs('reports', exist_ok=True)
with open('reports/ge_validation.json', 'w') as f:
    json.dump({
        "total": total,
        "passed": passed,
        "failed": failed,
        "success_rate": round(passed/total*100, 2),
        "checks": checks
    }, f, indent=2)

print("\nValidation report saved to reports/ge_validation.json")
print("=" * 50)