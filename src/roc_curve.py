import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import RocCurveDisplay

# Load dataset
df = pd.read_csv("datasets/customer_features-1.csv")

X = df.drop(columns=["Unnamed: 0", "customer_id", "Churn"])
y = df["Churn"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ROC Curve
RocCurveDisplay.from_estimator(model, X_test, y_test)

plt.title("ROC Curve")

plt.savefig(
    "reports/roc_curve.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("ROC Curve Saved")