import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 NeuralRetail Analytics Dashboard")
st.markdown("""
<div style='background:linear-gradient(90deg,#2563EB,#1E40AF);
padding:20px;
border-radius:15px;
color:white;
margin-bottom:20px;'>

<h2>AI Powered Retail Analytics Dashboard</h2>

<p>Predict • Analyze • Optimize • Grow</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
Welcome to **NeuralRetail**, an AI-powered Retail Analytics platform.

This dashboard helps businesses analyze customer behavior, forecast future sales,
predict customer churn, and perform customer segmentation using Machine Learning.
""")

st.markdown("---")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Modules",
    "4"
)

col2.metric(
    "ML Models",
    "3"
)

col3.metric(
    "Forecast Horizon",
    "30 Days"
)

col4.metric(
    "Status",
    "Active ✅"
)

st.markdown("---")

st.subheader("📌 Dashboard Modules")

c1, c2 = st.columns(2)

with c1:
    st.info("""
### 📈 Demand Forecast

Predict future product sales using Prophet time-series forecasting.

**Benefits**
- Inventory Planning
- Demand Prediction
- Sales Trends
""")

    st.success("""
### 👥 Customer Churn

Identify customers who are likely to leave.

**Benefits**
- Customer Retention
- Loyalty Programs
- Marketing Campaigns
""")

with c2:
    st.warning("""
### 🎯 Customer Segmentation

Group customers based on purchasing behavior.

**Benefits**
- Personalized Marketing
- Targeted Promotions
- Customer Insights
""")

    st.error("""
### 📄 Reports

Generate business reports and analytics.

**Includes**
- Sales Summary
- Customer Insights
- Forecast Reports
""")

st.markdown("---")

st.subheader("🚀 Technologies Used")

tech1, tech2, tech3, tech4 = st.columns(4)

tech1.success("🐍 Python")
tech2.success("⚡ Streamlit")
tech3.success("🤖 XGBoost")
tech4.success("📊 Plotly + Prophet")

st.markdown("---")
st.markdown("---")

st.subheader("📖 About the Project")

st.write("""
**NeuralRetail Analytics Dashboard** is an AI-powered retail analytics solution
developed to help businesses make data-driven decisions.

### Objectives
- Forecast future sales using Prophet
- Predict customer churn using XGBoost
- Segment customers using K-Means clustering
- Generate business insights through interactive dashboards

### Technologies Used
- Python
- Streamlit
- Plotly
- Prophet
- XGBoost
- Scikit-learn
- Pandas
""")

st.caption(
    "NeuralRetail Analytics Dashboard | Built with Streamlit, Prophet, XGBoost, Plotly & Scikit-learn"
)
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Customers", "5,878")
col2.metric("📦 Products", "3,681")
col3.metric("💰 Revenue", "$8.9M")
col4.metric("📈 Forecast", "30 Days")
st.subheader("📊 Executive Summary")

col1,col2=st.columns(2)

with col1:

    st.success("""
✔ Revenue is increasing steadily.

✔ Customer retention is improving.

✔ Sales forecast available for next 30 days.
""")

with col2:

    st.info("""
✔ Churn model trained using XGBoost.

✔ Segmentation completed using KMeans.

✔ Reports generated successfully.
""")
st.info("""
🏠 **Dashboard Overview**

This dashboard integrates Machine Learning models to help retailers forecast demand,
predict customer churn, segment customers, and generate business reports for
better decision-making.
""")
st.subheader("👨‍💻 Project Information")

st.write("""
**Project:** NeuralRetail Analytics Dashboard

**Technologies**
- Python
- Streamlit
- Prophet
- XGBoost
- K-Means
- Plotly
- Pandas
""")