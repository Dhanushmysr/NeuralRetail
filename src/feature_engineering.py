import pandas as pd

# ==========================
# LOAD CLEAN DATASET
# ==========================
df = pd.read_csv("clean_data.csv")

# Rename columns so the rest of the script works
df.rename(columns={
    "Invoice": "invoice",
    "InvoiceDate": "invoicedate",
    "Customer ID": "customer_id",
    "TotalAmount": "total_price"
}, inplace=True)

print("Dataset Loaded Successfully")
print(df.head())
print("\nColumns:")
print(df.columns.tolist())


# Customer Features

customer_features = df.groupby("customer_id").agg({
    "invoice": "nunique",
    "total_price": "sum"
})

customer_features.columns = [
    "Total_Orders",
    "Total_Revenue"
]

customer_features["Average_Order_Value"] = (
    customer_features["Total_Revenue"] /
    customer_features["Total_Orders"]
)

print("\nCustomer Features")
print(customer_features.head())
# ==========================
# RFM FEATURES
# ==========================

df["invoicedate"] = pd.to_datetime(df["invoicedate"])

reference_date = df["invoicedate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("customer_id").agg({

    "invoicedate": lambda x: (reference_date - x.max()).days,

    "invoice": "nunique",

    "total_price": "sum"

})

rfm.columns = [

    "Recency",

    "Frequency",

    "Monetary"

]

print("\nRFM Features")

print(rfm.head())
# ==========================
# RFM SCORE
# ==========================

rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    4,
    labels=[4,3,2,1],
    duplicates="drop"
)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    4,
    labels=[1,2,3,4],
    duplicates="drop"
)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    4,
    labels=[1,2,3,4],
    duplicates="drop"
)

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

print("\nRFM Scores")
print(rfm.head())
# ==========================
# PURCHASE FREQUENCY
# ==========================

purchase_frequency = df.groupby("customer_id")["invoice"].nunique()

customer_features["Purchase_Frequency"] = purchase_frequency

print("\nPurchase Frequency")
print(customer_features.head())
# ==========================
# CUSTOMER LIFETIME VALUE (CLV)
# ==========================

customer_features["CLV"] = (
    customer_features["Average_Order_Value"] *
    customer_features["Purchase_Frequency"]
)

print("\nCustomer Lifetime Value")
print(customer_features.head())
# ==========================
# TIME FEATURES
# ==========================

df["invoicedate"] = pd.to_datetime(df["invoicedate"])

df["Day_of_Week"] = df["invoicedate"].dt.day_name()

df["Month"] = df["invoicedate"].dt.month

df["Quarter"] = df["invoicedate"].dt.quarter

df["Holiday_Flag"] = df["Day_of_Week"].isin(
    ["Saturday", "Sunday"]
).astype(int)

print("\nTime Features")
print(
    df[
        [
            "invoicedate",
            "Day_of_Week",
            "Month",
            "Quarter",
            "Holiday_Flag"
        ]
    ].head()
)
# ==========================
# LAG FEATURES
# ==========================

df["Date"] = pd.to_datetime(df["invoicedate"]).dt.date

daily_sales = (
    df.groupby("Date")["total_price"]
    .sum()
    .reset_index()
)

daily_sales["Date"] = pd.to_datetime(daily_sales["Date"])

daily_sales = daily_sales.sort_values("Date")

daily_sales = daily_sales.reset_index(drop=True)

daily_sales["Lag_1"] = daily_sales["total_price"].shift(1)

daily_sales["Lag_7"] = daily_sales["total_price"].shift(7)

daily_sales["Lag_14"] = daily_sales["total_price"].shift(14)

print("\nLag Features")
print(daily_sales.head(20))

# ==========================
# ROLLING FEATURES
# ==========================

daily_sales["Rolling_Mean_7"] = (
    daily_sales["total_price"]
    .rolling(window=7)
    .mean()
)

daily_sales["Rolling_Mean_14"] = (
    daily_sales["total_price"]
    .rolling(window=14)
    .mean()
)

daily_sales["Rolling_Std_7"] = (
    daily_sales["total_price"]
    .rolling(window=7)
    .std()
)

print("\nRolling Features")
print(daily_sales.head(20))

# ==========================
# CREATE CHURN DATASET
# ==========================

customer_features = customer_features.merge(
    rfm,
    left_index=True,
    right_index=True,
    how="inner"
)

customer_features = customer_features.reset_index()

# Baseline churn label
customer_features["Churn"] = (
    customer_features["Recency"] > 90
).astype(int)

customer_features.to_csv(
    "features/churn_dataset.csv"
)

customer_features.to_excel(
    "features/churn_dataset.xlsx"
)

print("\nChurn Dataset Created")
print(customer_features.head())


# ==========================
# EXPORT FEATURE DATASETS
# ==========================

import os

os.makedirs("features", exist_ok=True)

customer_features.to_csv(
    "features/customer_features.csv"
)

customer_features.to_excel(
    "features/customer_features.xlsx"
)

rfm.to_csv(
    "features/rfm_features.csv"
)

rfm.to_excel(
    "features/rfm_features.xlsx"
)

daily_sales.to_csv(
    "features/time_series_features.csv",
    index=False
)

daily_sales.to_excel(
    "features/time_series_features.xlsx",
    index=False
)

print("\n===================================")
print("Feature Engineering Completed")
print("Files Saved Successfully")
print("===================================")
print(f"\nCustomer Features Shape : {customer_features.shape}")
print(f"RFM Features Shape      : {rfm.shape}")
print(f"Time Series Shape       : {daily_sales.shape}")

print("\nAll files exported successfully.")