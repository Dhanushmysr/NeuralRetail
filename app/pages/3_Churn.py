import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Customer Churn",
    page_icon="👥",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
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

# -----------------------------
# Title
# -----------------------------
st.title("👥 Customer Churn Dashboard")
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

# -----------------------------
# Load Data
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

churn_file = BASE_DIR / "data" / "features" / "churn_scores.csv"

if churn_file.exists():

    df = pd.read_csv(churn_file)

    st.success("Churn scores loaded successfully!")

    # -----------------------------
    # KPI Cards
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Customers",
        len(df)
    )

    col2.metric(
        "Average Churn Probability",
        f"{df['ChurnProbability'].mean():.2%}"
    )

    high_risk = len(df[df["ChurnProbability"] > 0.7])

    col3.metric(
        "High-Risk Customers",
        high_risk
    )

    st.markdown("---")

    # -----------------------------
    # Customer Data
    # -----------------------------
    st.subheader("📋 Customer Churn Data")

    st.dataframe(
        df[
            [
                "Recency",
                "Frequency",
                "Monetary",
                "Churn",
                "ChurnProbability"
            ]
        ],
        use_container_width=True
    )

    st.markdown("---")

    # -----------------------------
    # Charts
    # -----------------------------
    left, right = st.columns(2)

    with left:

        fig = px.pie(
            df,
            names="Churn",
            title="Churn Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig2 = px.histogram(
            df,
            x="ChurnProbability",
            nbins=20,
            title="Churn Probability Distribution"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # High Risk Customers
    # -----------------------------
    st.markdown("---")

    st.subheader("⚠ High-Risk Customers")

    st.warning(f"""
There are **{high_risk}** customers with a churn probability greater than **70%**.

Recommended actions:

- Offer personalized discounts
- Send loyalty rewards
- Launch targeted email campaigns
- Follow up with customer support
""")

    # -----------------------------
    # Download Button
    # -----------------------------
    with open(churn_file, "rb") as file:

        st.download_button(
            label="⬇ Download Churn Scores",
            data=file,
            file_name="churn_scores.csv",
            mime="text/csv"
        )

    # -----------------------------
    # Footer
    # -----------------------------
    st.markdown("---")

    st.caption(
        "NeuralRetail Analytics Dashboard | Built with Streamlit • XGBoost • Plotly"
    )

else:

    st.error("❌ churn_scores.csv not found. Please run churn_model.py first.")
st.info("""
👥 **Business Insight**

Customer churn prediction helps identify customers who are likely to leave,
allowing businesses to take proactive retention measures through personalized
offers and loyalty programs.
""")