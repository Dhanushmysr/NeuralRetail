import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

# -----------------------------------
# Custom CSS
# -----------------------------------
st.markdown("""
<style>
div[data-testid="metric-container"]{
    background-color:#EAF4FF;
    border:1px solid #CBD5E1;
    padding:15px;
    border-radius:12px;
}

h1{
    color:#2563EB;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 Business Reports Dashboard")

# -----------------------------------
# File Paths
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

forecast_file = BASE_DIR / "data" / "features" / "forecast.csv"
churn_file = BASE_DIR / "data" / "features" / "churn_scores.csv"
segment_file = BASE_DIR / "data" / "features" / "segments.csv"

# -----------------------------------
# File Status
# -----------------------------------
forecast_exists = forecast_file.exists()
churn_exists = churn_file.exists()
segment_exists = segment_file.exists()

# -----------------------------------
# KPI Cards
# -----------------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Forecast Report",
    "Available" if forecast_exists else "Missing"
)

col2.metric(
    "Churn Report",
    "Available" if churn_exists else "Missing"
)

col3.metric(
    "Segmentation Report",
    "Available" if segment_exists else "Missing"
)

st.markdown("---")

# -----------------------------------
# Preview Reports
# -----------------------------------
if forecast_exists:
    st.subheader("📈 Forecast Report")
    forecast = pd.read_csv(forecast_file)
    st.dataframe(forecast.head(), use_container_width=True)

if churn_exists:
    st.subheader("👥 Churn Report")
    churn = pd.read_csv(churn_file)
    st.dataframe(churn.head(), use_container_width=True)

if segment_exists:
    st.subheader("🎯 Segmentation Report")
    segment = pd.read_csv(segment_file)
    st.dataframe(segment.head(), use_container_width=True)

st.markdown("---")

# -----------------------------------
# Business Summary
# -----------------------------------
st.subheader("💡 Business Summary")

summary = []

if forecast_exists:
    summary.append("✅ Demand forecast generated successfully.")

if churn_exists:
    summary.append("✅ Customer churn probabilities calculated.")

if segment_exists:
    summary.append("✅ Customer segmentation completed.")

for item in summary:
    st.success(item)

st.info("""
The dashboard combines machine learning models to help retail businesses:

- Predict future demand
- Identify customers at risk of churning
- Segment customers for personalized marketing
- Support better business decisions
""")

st.markdown("---")

# -----------------------------------
# Downloads
# -----------------------------------
st.subheader("⬇ Download Reports")

if forecast_exists:
    with open(forecast_file, "rb") as f:
        st.download_button(
            "Download Forecast Report",
            f,
            file_name="forecast.csv",
            mime="text/csv"
        )

if churn_exists:
    with open(churn_file, "rb") as f:
        st.download_button(
            "Download Churn Report",
            f,
            file_name="churn_scores.csv",
            mime="text/csv"
        )

if segment_exists:
    with open(segment_file, "rb") as f:
        st.download_button(
            "Download Segmentation Report",
            f,
            file_name="segments.csv",
            mime="text/csv"
        )

st.markdown("---")

st.caption(
    "NeuralRetail Analytics Dashboard | Reports Module | Streamlit • XGBoost • Prophet • K-Means"
)
st.info("""
📄 **Business Insight**

The reports module provides a consolidated view of forecasting, churn prediction,
and customer segmentation results, enabling data-driven business decisions.
""")