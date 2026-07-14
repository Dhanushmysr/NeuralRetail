import pandas as pd

# ============================
# Read Model Comparison Results
# ============================

results = pd.read_csv("reports/model_comparison.csv")

table_html = results.to_html(
    index=False,
    classes="styled-table",
    border=0
)

# ============================
# Best Parameters
# ============================

best_parameters = """
<ul>
<li><b>C:</b> 0.01</li>
<li><b>Solver:</b> lbfgs</li>
<li><b>Penalty:</b> l2</li>
<li><b>Max Iterations:</b> 500</li>
</ul>
"""

# ============================
# HTML Report
# ============================

html = f"""
<!DOCTYPE html>

<html>

<head>

<title>NeuralRetail Model Improvement Report</title>

<style>

body{{
    font-family:Arial;
    background:#f4f4f4;
    margin:0;
}}

.header{{
    background:#ff9800;
    color:white;
    padding:30px;
    text-align:center;
}}

.container{{
    width:90%;
    margin:auto;
}}

.card{{
    background:white;
    margin:20px 0;
    padding:25px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,.2);
}}

h2{{
    color:#ff9800;
}}

.styled-table{{
    border-collapse:collapse;
    width:100%;
}}

.styled-table th{{
    background:#ff9800;
    color:white;
    padding:12px;
}}

.styled-table td{{
    padding:12px;
    text-align:center;
}}

img{{
    width:90%;
    display:block;
    margin:auto;
}}

.footer{{
    background:#222;
    color:white;
    text-align:center;
    padding:15px;
    margin-top:40px;
}}

</style>

</head>

<body>

<div class="header">

<h1>NeuralRetail</h1>

<h2>Model Improvement Report</h2>

<p>Week 2 Deliverable</p>

</div>

<div class="container">

<div class="card">

<h2>Objective</h2>

<p>

Improve customer churn prediction through hyperparameter tuning,
model comparison and model explainability.

</p>

</div>

<div class="card">

<h2>Dataset Overview</h2>

<ul>

<li>Dataset : Customer Features</li>

<li>Target : Churn</li>

<li>Features : 12</li>

<li>Train/Test Split : 80/20</li>

<li>Algorithm : Logistic Regression, Random Forest, Gradient Boosting</li>

</ul>

</div>

<div class="card">

<h2>Hyperparameter Tuning</h2>

{best_parameters}

</div>

<div class="card">

<h2>Model Comparison</h2>

{table_html}

</div>

<div class="card">

<h2>Feature Importance</h2>

<img src="feature_importance.png">

<p>

<b>Observation:</b>
Recency, RFM Score and R Score are the most influential features.

</p>

<p>

<b>Business Insight:</b>

Customers who have not purchased recently are most likely to churn.

</p>

</div>

<div class="card">

<h2>SHAP Summary Plot</h2>

<img src="shap_summary.png">

<p>

SHAP explains the contribution of every feature to individual predictions.

</p>

</div>

<div class="card">

<h2>SHAP Feature Importance</h2>

<img src="shap_bar.png">

<p>

The bar plot ranks features according to their average impact on predictions.

</p>

</div>

<div class="card">

<h2>Confusion Matrix</h2>

<img src="confusion_matrix.png">

</div>

<div class="card">

<h2>ROC Curve</h2>

<img src="roc_curve.png">

</div>

<div class="card">

<h2>Key Business Insights</h2>

<ul>

<li>Recent customer activity is the strongest predictor of churn.</li>

<li>RFM Score is highly effective in customer segmentation.</li>

<li>Customers with low purchase frequency require targeted retention strategies.</li>

<li>Feature engineering significantly improved model performance.</li>

</ul>

</div>

<div class="card">

<h2>Recommendations</h2>

<ul>

<li>Monitor inactive customers regularly.</li>

<li>Launch personalized retention campaigns.</li>

<li>Reward loyal customers.</li>

<li>Retrain the model periodically with new customer data.</li>

</ul>

</div>

<div class="card">

<h2>Conclusion</h2>

<p>

The project successfully improved churn prediction using feature engineering,
hyperparameter tuning and explainable AI techniques.
The developed model demonstrates excellent predictive performance and
provides actionable business insights.

</p>

</div>

</div>

<div class="footer">

NeuralRetail © 2026

</div>

</body>

</html>

"""

with open("reports/model_improvement_report.html","w",encoding="utf-8") as f:
    f.write(html)

print("Professional HTML Report Generated Successfully!")