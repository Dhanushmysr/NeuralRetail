import streamlit as st

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="NeuralRetail Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------
# Custom CSS
# ----------------------------------
st.markdown("""
<style>

/* Hide Streamlit default menu */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#1E3A8A;
}

[data-testid="stSidebar"] *{
    color:white;
}

/* Main background */
.main{
    background-color:#F8FAFC;
}

/* Headings */
h1{
    color:#1E3A8A;
}

h2,h3{
    color:#2563EB;
}

/* Metric Cards */
div[data-testid="metric-container"]{
    background:white;
    border:1px solid #E2E8F0;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

div[data-testid="metric-container"]{

background:linear-gradient(135deg,#ffffff,#f3f4f6);

border-radius:15px;

padding:18px;

box-shadow:0px 4px 12px rgba(0,0,0,.12);

border:1px solid #e5e7eb;

}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# Sidebar
# ----------------------------------
st.sidebar.title("🛍️ NeuralRetail")

st.sidebar.success("AI-Powered Retail Analytics")

st.sidebar.markdown("---")

st.sidebar.info("""
📌 **Dashboard Modules**

🏠 Home

📈 Demand Forecast

👥 Customer Churn

🎯 Customer Segmentation

📄 Business Reports
""")

st.sidebar.markdown("---")

st.sidebar.caption("Version 1.0")

# ----------------------------------
# Main Page
# ----------------------------------
st.title("🛍️ NeuralRetail Analytics Dashboard")
st.info("""
👋 **Welcome!**

NeuralRetail is an AI-powered analytics platform that helps retailers forecast demand,
predict customer churn, segment customers, and generate business insights for
better decision-making.
""")

st.markdown("""
Welcome to **NeuralRetail**, an AI-powered retail analytics platform that helps
businesses make data-driven decisions using Machine Learning.

### 🚀 Key Features

- 📈 Demand Forecasting using **Prophet**
- 👥 Customer Churn Prediction using **XGBoost**
- 🎯 Customer Segmentation using **K-Means**
- 📄 Interactive Business Reports
""")

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

col1.metric("📦 Modules", "4")

col2.metric("🤖 ML Models", "3")

col3.metric("📅 Forecast", "30 Days")

col4.metric("📊 Status", "Active")

st.markdown("---")

st.subheader("📌 Technologies Used")

c1, c2, c3, c4 = st.columns(4)

c1.success("🐍 Python")

c2.success("⚡ Streamlit")

c3.success("🤖 XGBoost")

c4.success("📊 Prophet & Plotly")

st.markdown("---")

st.caption(
    "NeuralRetail Analytics Dashboard | Built with ❤️ using Streamlit, XGBoost, Prophet, Plotly & Scikit-learn"
)
st.markdown("---")

st.subheader("💡 Business Benefits")

col1, col2 = st.columns(2)

with col1:
    st.success("""
✔ Better Inventory Planning

✔ Reduce Customer Churn

✔ Improve Customer Satisfaction
""")

with col2:
    st.success("""
✔ AI-Based Sales Forecasting

✔ Targeted Marketing

✔ Data-Driven Decision Making
""")
