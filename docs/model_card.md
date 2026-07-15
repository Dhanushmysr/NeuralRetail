# Model Card

## Model Information

| Item | Details |
|------|---------|
| Project | NeuralRetail |
| Model Name | Customer Churn Prediction Model |
| Version | 1.0 |
| Author | NeuralRetail Team |
| Date | July 2026 |
| Algorithm | Logistic Regression (Hyperparameter Tuned) |

---

# Purpose

This model predicts whether a retail customer is likely to churn based on historical purchasing behavior and engineered customer features.

The objective is to help businesses identify at-risk customers and take proactive retention actions.

---

# Intended Users

- Business Analysts
- Marketing Teams
- Customer Relationship Managers
- Retail Decision Makers

---

# Dataset

The model was trained using the processed Customer Features dataset containing engineered retail customer information.

Target Variable

- Churn

Input Features

- Total Orders
- Total Revenue
- Average Order Value
- Purchase Frequency
- Customer Lifetime Value (CLV)
- Recency
- Frequency
- Monetary
- R Score
- F Score
- M Score
- RFM Score

---

# Training Details

Algorithm

- Logistic Regression

Hyperparameter Tuning

GridSearchCV was used to determine the optimal model parameters.

Best Parameters

- C = 0.01
- Penalty = L2
- Solver = lbfgs
- Max Iterations = 500

---

# Performance

Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 Score

Model comparison was performed against:

- Random Forest
- Gradient Boosting

The tuned Logistic Regression model achieved excellent predictive performance while remaining interpretable.

---

# Explainability

Explainable AI techniques were applied using SHAP.

Generated Visualizations

- SHAP Summary Plot
- SHAP Feature Importance Plot

Feature importance analysis identified:

1. Recency
2. RFM Score
3. R Score

as the strongest indicators of customer churn.

---

# Business Impact

The model enables businesses to

- Predict customer churn
- Identify high-risk customers
- Improve customer retention
- Optimize marketing campaigns
- Increase customer lifetime value

---

# Limitations

- Trained on historical retail data only.
- Performance may decrease if customer behavior changes significantly.
- Requires periodic retraining with updated data.

---

# Ethical Considerations

The model should support business decision-making and not be the sole basis for customer treatment. Predictions should be reviewed alongside business context.

---

# Future Improvements

- Real-time predictions
- Data drift monitoring
- Automated retraining
- Cloud deployment
- Model monitoring