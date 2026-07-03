
import os
import warnings
import joblib
import mlflow
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
)

warnings.filterwarnings("ignore")

DATA_PATH = "features/churn_dataset.csv"
OUTPUT_DIR = "outputs"
MODEL_DIR = "models"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

print("=" * 60)
print("NeuralRetail - Customer Churn Prediction")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=[c for c in ["customer_id","RFM_Score","Churn"] if c in df.columns]).copy()

for col in X.columns:
    if X[col].dtype == object:
        X[col] = pd.factorize(X[col])[0]

X = X.fillna(0)
y = df["Churn"]

X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.2,random_state=42,stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

mlflow.set_experiment("NeuralRetail_Churn")

with mlflow.start_run():
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train,y_train)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test,y_pred)
    prec = precision_score(y_test,y_pred,zero_division=0)
    rec = recall_score(y_test,y_pred,zero_division=0)
    f1 = f1_score(y_test,y_pred,zero_division=0)

    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1 Score : {f1:.4f}")

    metrics_file=os.path.join(OUTPUT_DIR,"churn_metrics.txt")
    with open(metrics_file,"w") as f:
        f.write(f"Accuracy : {acc:.4f}\nPrecision: {prec:.4f}\nRecall   : {rec:.4f}\nF1 Score : {f1:.4f}\n")

    report_file=os.path.join(OUTPUT_DIR,"classification_report.txt")
    with open(report_file,"w") as f:
        f.write(classification_report(y_test,y_pred,zero_division=0))

    disp=ConfusionMatrixDisplay(confusion_matrix(y_pred=y_pred,y_true=y_test))
    disp.plot(values_format="d")
    plt.title("Confusion Matrix")
    cm_file=os.path.join(OUTPUT_DIR,"confusion_matrix.png")
    plt.tight_layout()
    plt.savefig(cm_file,dpi=300)
    plt.close()

    joblib.dump(model,os.path.join(MODEL_DIR,"churn_model.pkl"))
    joblib.dump(scaler,os.path.join(MODEL_DIR,"scaler.pkl"))

    mlflow.log_param("Model","LogisticRegression")
    mlflow.log_metric("Accuracy",acc)
    mlflow.log_metric("Precision",prec)
    mlflow.log_metric("Recall",rec)
    mlflow.log_metric("F1",f1)
    mlflow.log_artifact(metrics_file)
    mlflow.log_artifact(report_file)
    mlflow.log_artifact(cm_file)
    mlflow.log_artifact(os.path.join(MODEL_DIR,"churn_model.pkl"))

print("Churn model training completed successfully.")
