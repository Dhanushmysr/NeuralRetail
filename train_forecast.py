
import os
import warnings
import joblib
import mlflow
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

warnings.filterwarnings("ignore")

# ==========================
# CONFIGURATION
# ==========================
DATA_PATH = "features/time_series_features.csv"
OUTPUT_DIR = "outputs"
MODEL_DIR = "models"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# ==========================
# LOAD DATA
# ==========================
print("=" * 60)
print("NeuralRetail - Demand Forecasting")
print("=" * 60)

df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])

forecast_df = df[["Date", "total_price"]].rename(
    columns={
        "Date": "ds",
        "total_price": "y"
    }
)

forecast_df = forecast_df.sort_values("ds").reset_index(drop=True)

split_index = int(len(forecast_df) * 0.80)

train = forecast_df.iloc[:split_index].copy()
test = forecast_df.iloc[split_index:].copy()

print(f"Training rows : {len(train)}")
print(f"Testing rows  : {len(test)}")

# ==========================
# MLFLOW
# ==========================
mlflow.set_experiment("NeuralRetail_Forecasting")

with mlflow.start_run():

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode="multiplicative",
        changepoint_prior_scale=0.05
    )

    model.fit(train)

    future = model.make_future_dataframe(
        periods=len(test) + 30,
        freq="D"
    )

    forecast = model.predict(future)

    prediction = forecast[["ds", "yhat"]].tail(len(test)).reset_index(drop=True)
    actual = test.reset_index(drop=True)

    rmse = np.sqrt(
    mean_squared_error(
        actual["y"],
        prediction["yhat"]
    )
    )

    mae = mean_absolute_error(
    actual["y"],
    prediction["yhat"]
)

    mape = (
     np.mean(
        np.abs(
            (actual["y"] - prediction["yhat"])
            / actual["y"].replace(0, np.nan)
        )
    )
    ) * 100

    print("\nEvaluation Metrics")
    print(f"RMSE : {rmse:.2f}")
    print(f"MAE  : {mae:.2f}")
    print(f"MAPE : {mape:.2f}%")

    metrics_path = os.path.join(OUTPUT_DIR, "forecast_metrics.txt")
    with open(metrics_path, "w") as f:
        f.write(f"RMSE : {rmse:.4f}\n")
        f.write(f"MAE  : {mae:.4f}\n")
        f.write(f"MAPE : {mape:.4f}\n")

    forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
    ].to_csv(
    os.path.join(
        OUTPUT_DIR,
        "forecast.csv"
    ),
    index=False
    )

    fig = model.plot(forecast)
    plt.title("NeuralRetail Demand Forecast", fontsize=16)
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.grid(True)

    plot_path = os.path.join(
    OUTPUT_DIR,
    "forecast_plot.png"
    )

    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()

    model_path = os.path.join(MODEL_DIR, "forecast_model.pkl")
    joblib.dump(model, model_path)

    mlflow.log_param("Model", "Prophet")
    mlflow.log_param("Train Size", len(train))
    mlflow.log_param("Test Size", len(test))

    mlflow.log_metric("RMSE", rmse)
    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("MAPE", mape)

    mlflow.log_artifact(metrics_path)
    mlflow.log_artifact(plot_path)
    mlflow.log_artifact(model_path)
    mlflow.log_artifact(os.path.join(OUTPUT_DIR, "forecast.csv"))

print("\nForecasting completed successfully.")
print("Outputs saved to outputs/")
print("Model saved to models/")
