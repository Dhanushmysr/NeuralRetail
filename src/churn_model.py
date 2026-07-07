import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
import xgboost as xgb
import shap
import warnings
warnings.filterwarnings('ignore')

print("Loading RFM data...")
rfm = pd.read_csv(r'C:\Neuralretail\data\features\rfm.csv')

# Create churn label — customers with Recency > 180 days are churned
rfm['Churn'] = (rfm['Recency'] > 180).astype(int)

print("Churn distribution:")
print(rfm['Churn'].value_counts())

# Features and target
X = rfm[['Recency', 'Frequency', 'Monetary']]
y = rfm['Churn']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost model
print("Training XGBoost model...")
model = xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict_proba(X_test)[:,1]
auc = roc_auc_score(y_test, y_pred)
print(f"AUC-ROC Score: {auc:.4f}")

# Save predictions
rfm['ChurnProbability'] = model.predict_proba(X)[:,1]
rfm.to_csv(r'C:\Neuralretail\data\features\churn_scores.csv', index=False)
print("Churn scores saved!")
