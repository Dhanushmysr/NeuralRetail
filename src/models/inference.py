import os
import joblib
import pandas as pd

MODEL_DIR = "models"

# ==========================
# Load Saved Models
# ==========================

print("Loading trained models...")

churn_model = joblib.load(
    os.path.join(MODEL_DIR, "churn_model.pkl")
)

scaler = joblib.load(
    os.path.join(MODEL_DIR, "scaler.pkl")
)

forecast_model = joblib.load(
    os.path.join(MODEL_DIR, "forecast_model.pkl")
)

print("Models loaded successfully.\n")


# =====================================================
# Customer Churn Prediction
# =====================================================

def predict_churn(customer_data):
    """
    Predict customer churn.

    Parameters
    ----------
    customer_data : pandas.DataFrame

    Returns
    -------
    dict
    """

    scaled = scaler.transform(customer_data)

    prediction = churn_model.predict(scaled)[0]

    probability = churn_model.predict_proba(scaled)[0]

    return {
        "prediction": int(prediction),
        "probability": round(float(max(probability)), 4)
    }


# =====================================================
# Sales Forecast
# =====================================================

def forecast_sales(days=30):
    """
    Forecast future sales.

    Parameters
    ----------
    days : int

    Returns
    -------
    pandas.DataFrame
    """

    future = forecast_model.make_future_dataframe(
        periods=days,
        freq="D"
    )

    forecast = forecast_model.predict(future)

    return forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ]


# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("NeuralRetail Inference Engine")
    print("=" * 60)

    print("\nForecast Example\n")

    forecast = forecast_sales(7)

    print(forecast.tail())

    print("\nInference engine is ready.")
