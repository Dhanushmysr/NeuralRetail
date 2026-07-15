from fastapi import FastAPI
import pandas as pd
import os
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="NeuralRetail API")

# ==========================
# LOAD ML MODEL
# ==========================

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ==========================
# LOAD CLEAN DATASET
# ==========================

# ==========================
# LOAD CLEAN DATASET
# ==========================

csv_file = os.path.join(
    BASE_DIR,
    "clean_data.csv"
)

df = pd.read_csv(csv_file)

# Rename columns
df.columns = [
    "invoice",
    "stockcode",
    "description",
    "quantity",
    "invoicedate",
    "price",
    "customer_id",
    "country",
    "total_price",
    "month"
]

df["invoicedate"] = pd.to_datetime(df["invoicedate"])

# ==========================
# REQUEST MODEL
# ==========================

class ChurnRequest(BaseModel):
    Total_Orders: float
    Total_Revenue: float
    Average_Order_Value: float
    Purchase_Frequency: float
    CLV: float
    Recency: float
    Frequency: float
    Monetary: float
    R_Score: float
    F_Score: float
    M_Score: float

# ==========================
# HOME
# ==========================

@app.get("/")
def home():
    return {
        "message": "NeuralRetail API Running Successfully"
    }

# ==========================
# TOTAL CUSTOMERS
# ==========================

@app.get("/customers")
def customers():
    return {
        "total_customers": int(df["customer_id"].nunique())
    }

# ==========================
# TOTAL REVENUE
# ==========================

@app.get("/revenue")
def revenue():
    return {
        "total_revenue": float(df["total_price"].sum())
    }

# ==========================
# TOTAL ORDERS
# ==========================

@app.get("/orders")
def orders():
    return {
        "total_orders": int(df["invoice"].nunique())
    }

# ==========================
# TOP COUNTRY
# ==========================

@app.get("/top-country")
def top_country():

    country = (
        df.groupby("country")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    return {
        "country": str(country.index[0]),
        "revenue": float(country.iloc[0])
    }

# ==========================
# TOP PRODUCT
# ==========================

@app.get("/top-product")
def top_product():

    product = (
        df.groupby("description")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    return {
        "product": str(product.index[0]),
        "revenue": float(product.iloc[0])
    }

# ==========================
# CUSTOMER DETAILS
# ==========================

@app.get("/customer/{customer_id}")
def customer_details(customer_id: int):

    customer = df[df["customer_id"] == customer_id]

    if customer.empty:
        return {
            "message": "Customer Not Found"
        }

    return {
        "customer_id": customer_id,
        "orders": int(customer["invoice"].nunique()),
        "revenue": float(customer["total_price"].sum())
    }

# ==========================
# MONTHLY SALES
# ==========================

@app.get("/monthly-sales")
def monthly_sales():

    monthly = (
        df.groupby("month")["total_price"]
        .sum()
        .reset_index()
    )

    return monthly.to_dict(orient="records")

# ==========================
# COUNTRY SALES
# ==========================

@app.get("/country/{country_name}")
def country_sales(country_name: str):

    data = df[df["country"].str.lower() == country_name.lower()]

    if data.empty:
        return {
            "message": "Country Not Found"
        }

    return {
        "country": country_name,
        "revenue": float(data["total_price"].sum()),
        "orders": int(data["invoice"].nunique())
    }

# ==========================
# HEALTH CHECK
# ==========================

@app.get("/health")
def health():
    return {
        "status": "API Running Successfully"
    }

# ==========================
# CHURN PREDICTION
# ==========================

@app.post("/predict-churn")
def predict_churn(data: ChurnRequest):

    # Feature order must match training
    features = np.array([[
        0,  # Placeholder for Unnamed: 0
        data.Total_Orders,
        data.Total_Revenue,
        data.Average_Order_Value,
        data.Purchase_Frequency,
        data.CLV,
        data.Recency,
        data.Frequency,
        data.Monetary,
        data.R_Score,
        data.F_Score,
        data.M_Score
    ]])

    # Scale features
    scaled_features = scaler.transform(features)

    # Prediction
    prediction = model.predict(scaled_features)[0]

    # Probability
    probability = model.predict_proba(scaled_features)[0][1]

    return {
        "prediction": "Churn" if prediction == 1 else "No Churn",
        "prediction_label": int(prediction),
        "churn_probability": round(float(probability), 4)
    }
