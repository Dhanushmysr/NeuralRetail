import pandas as pd
import shap
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv("datasets/customer_features-1.csv")

# Features and Target
X = df.drop(columns=["Unnamed: 0", "customer_id", "Churn"])
y = df["Churn"]

# ==========================================
# Train Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================================
# Train Random Forest Model
# ==========================================

model = RandomForestClassifier(random_state=42)

model.fit(X_train, y_train)

print("Model trained successfully.")

# ==========================================
# Create SHAP Explainer
# ==========================================

explainer = shap.Explainer(model, X_train)

print("Generating SHAP values...")

shap_values = explainer(X_test)

print("SHAP values generated.")

print("Shape:", shap_values.values.shape)

# ==========================================
# Select SHAP values for Positive Class
# ==========================================

if len(shap_values.values.shape) == 3:

    shap_class1 = shap.Explanation(
        values=shap_values.values[:, :, 1],
        base_values=shap_values.base_values[:, 1],
        data=shap_values.data,
        feature_names=shap_values.feature_names,
    )

else:

    shap_class1 = shap_values

# ==========================================
# SHAP Summary Plot
# ==========================================

plt.figure(figsize=(10,6))

shap.plots.beeswarm(
    shap_class1,
    max_display=12,
    show=False
)

plt.savefig(
    "reports/shap_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("✓ SHAP Summary Plot Saved")

# ==========================================
# SHAP Bar Plot
# ==========================================

plt.figure(figsize=(10,6))

shap.plots.bar(
    shap_class1,
    max_display=12,
    show=False
)

plt.savefig(
    "reports/shap_bar.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("✓ SHAP Bar Plot Saved")