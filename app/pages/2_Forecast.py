import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Demand Forecast",
    page_icon="📈",
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
st.title("📈 Demand Forecast Dashboard")
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
# Load Forecast Data
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
forecast_path = BASE_DIR / "data" / "features" / "forecast.csv"

if forecast_path.exists():

    forecast = pd.read_csv(forecast_path)
    forecast["ds"] = pd.to_datetime(forecast["ds"])

    st.success("Forecast loaded successfully!")

    st.markdown("---")

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Forecast Days",
        30
    )

    col2.metric(
        "Maximum Sales",
        f"{forecast['yhat'].max():,.0f}"
    )

    col3.metric(
        "Average Sales",
        f"{forecast['yhat'].mean():,.0f}"
    )

    st.markdown("---")

    # Forecast Table
    st.subheader("📋 Forecast Data")

    st.dataframe(
        forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]],
        use_container_width=True
    )

    # Forecast Chart
    st.subheader("📈 Sales Forecast")

    fig = px.line(
        forecast,
        x="ds",
        y="yhat",
        markers=True,
        title="30-Day Sales Forecast"
    )
    

    st.plotly_chart(fig, use_container_width=True)

    # Confidence Interval
    st.subheader("📊 Prediction Interval")

    fig2 = px.line(
        forecast,
        x="ds",
        y=["yhat_lower", "yhat", "yhat_upper"],
        title="Forecast with Confidence Interval"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Business Insights
    st.markdown("---")

    st.subheader("💡 Business Insights")

    st.success("""
- 📈 Sales are expected to increase over the forecast period.
- 📦 Inventory planning should focus on high-demand periods.
- 🛒 Use the forecast to reduce stock-outs and excess inventory.
- 🤖 Forecast generated using the Prophet time-series model.
""")

    # Download Button
    with open(forecast_path, "rb") as file:
        st.download_button(
            label="⬇ Download Forecast CSV",
            data=file,
            file_name="forecast.csv",
            mime="text/csv"
        )

    # Footer
    st.markdown("---")
    st.caption(
        "NeuralRetail Analytics Dashboard | Built with Streamlit • Prophet • Plotly"
    )

else:
    st.error("❌ forecast.csv not found. Please run demand_forecast.py first.")
st.info("""
📈 **Business Insight**

Demand is expected to fluctuate over the forecast period.
Businesses can use this forecast to optimize inventory planning and reduce stock shortages.
""")