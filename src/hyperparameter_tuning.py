import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
# Load dataset
df = pd.read_csv("datasets/customer_features-1.csv")

print("Dataset Loaded Successfully")
print(df.head())
# Features
X = df.drop(columns=["Unnamed: 0", "customer_id", "Churn"])

# Target
y = df["Churn"]

print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget:")
print(y.head())
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", X_train.shape[0])
print("Testing Samples:", X_test.shape[0])
baseline_model = LogisticRegression(max_iter=1000)

baseline_model.fit(X_train, y_train)

baseline_predictions = baseline_model.predict(X_test)
print("\n===== Baseline Model =====")

print("Accuracy :", accuracy_score(y_test, baseline_predictions))
print("Precision:", precision_score(y_test, baseline_predictions))
print("Recall   :", recall_score(y_test, baseline_predictions))
print("F1 Score :", f1_score(y_test, baseline_predictions))

print("\nFeature Correlation with Churn:")

correlation = df.corr(numeric_only=True)["Churn"].sort_values(ascending=False)

print(correlation)
print("\n==============================")
print("Hyperparameter Tuning Started")
print("==============================")

param_grid = {
    "C": [0.01, 0.1, 1, 10, 100],
    "solver": ["lbfgs", "liblinear"],
    "penalty": ["l2"],
    "max_iter": [100, 300, 500, 1000]
}

grid_search = GridSearchCV(
    LogisticRegression(),
    param_grid=param_grid,
    cv=5,
    scoring="f1",
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

print("\nBest Parameters:")
print(grid_search.best_params_)
print("\n==============================")
print("Hyperparameter Tuning Started")
print("==============================")

param_grid = {
    "C": [0.01, 0.1, 1, 10, 100],
    "solver": ["lbfgs", "liblinear"],
    "penalty": ["l2"],
    "max_iter": [100, 300, 500, 1000]
}

grid_search = GridSearchCV(
    LogisticRegression(),
    param_grid=param_grid,
    cv=5,
    scoring="f1",
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

print("\nBest Parameters:")
print(grid_search.best_params_)
tuned_predictions = best_model.predict(X_test)

print("\n===== Tuned Model =====")

print("Accuracy :", accuracy_score(y_test, tuned_predictions))
print("Precision:", precision_score(y_test, tuned_predictions))
print("Recall   :", recall_score(y_test, tuned_predictions))
print("F1 Score :", f1_score(y_test, tuned_predictions))
joblib.dump(best_model, "src/models/best_churn_model.pkl")
