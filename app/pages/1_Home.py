import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.theme import load_theme, gradient_banner, section_header, kpi_row, render_sidebar, insight_box, badge_row

# ----------------------------------
# Theme + Page Configuration
# ----------------------------------
load_theme("Home", "🏠")
render_sidebar(active_page="Home")

# ----------------------------------
# Try to load real headline numbers
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
clean_path = BASE_DIR / "data" / "processed" / "clean_data.csv"

total_customers = total_products = total_revenue = None

if clean_path.exists():
    try:
        df = pd.read_csv(clean_path)
        total_customers = df["Customer ID"].nunique()
        total_products = df["Description"].nunique()
        total_revenue = df["TotalAmount"].sum()
    except Exception:
        pass

# ----------------------------------
# Hero
# ----------------------------------
gradient_banner(
    eyebrow="Retail Intelligence Platform",
    title="🏠 NeuralRetail Analytics Dashboard",
    subtitle="Predict • Analyze • Optimize • Grow — an AI-powered dashboard that helps businesses "
              "analyze customer behaviour, forecast sales, predict churn, and segment customers.",
    color="blue",
)

# ----------------------------------
# Platform KPIs
# ----------------------------------
section_header("📌", "Platform Overview")

kpi_row([
    {"icon": "📦", "label": "Modules", "value": "5", "color": "blue"},
    {"icon": "🤖", "label": "ML Models", "value": "3", "color": "purple"},
    {"icon": "📅", "label": "Forecast Horizon", "value": "30 Days", "color": "teal"},
    {"icon": "✅", "label": "Status", "value": "Active", "color": "green"},
])

st.write("")

if total_customers is not None:
    kpi_row([
        {"icon": "👥", "label": "Customers", "value": f"{total_customers:,}", "color": "pink"},
        {"icon": "🛒", "label": "Products", "value": f"{total_products:,}", "color": "orange"},
        {"icon": "💰", "label": "Revenue", "value": f"₹{total_revenue:,.0f}", "color": "green"},
        {"icon": "📈", "label": "Forecast", "value": "30 Days", "color": "blue"},
    ])

st.write("")
st.markdown("---")

# ----------------------------------
# Dashboard Modules
# ----------------------------------
section_header("🧭", "Dashboard Modules")

c1, c2 = st.columns(2)

with c1:
    st.markdown(
        """
        <div class="nr-card" style="margin-bottom:14px;">
            <div style="font-weight:700; color:#0F172A;">📈 Demand Forecast</div>
            <p style="font-size:0.88rem; color:#475569; margin:6px 0;">
                Predict future product sales using Prophet time-series forecasting.
            </p>
            <div style="font-size:0.82rem; color:#334155;">
                <b>Benefits:</b> Inventory Planning · Demand Prediction · Sales Trends
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="nr-card">
            <div style="font-weight:700; color:#0F172A;">👥 Customer Churn</div>
            <p style="font-size:0.88rem; color:#475569; margin:6px 0;">
                Identify customers who are likely to leave.
            </p>
            <div style="font-size:0.82rem; color:#334155;">
                <b>Benefits:</b> Customer Retention · Loyalty Programs · Marketing Campaigns
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="nr-card" style="margin-bottom:14px;">
            <div style="font-weight:700; color:#0F172A;">🎯 Customer Segmentation</div>
            <p style="font-size:0.88rem; color:#475569; margin:6px 0;">
                Group customers based on purchasing behaviour.
            </p>
            <div style="font-size:0.82rem; color:#334155;">
                <b>Benefits:</b> Personalized Marketing · Targeted Promotions · Customer Insights
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="nr-card">
            <div style="font-weight:700; color:#0F172A;">📄 Reports & Insights</div>
            <p style="font-size:0.88rem; color:#475569; margin:6px 0;">
                Consolidated business reports and executive insights.
            </p>
            <div style="font-size:0.82rem; color:#334155;">
                <b>Includes:</b> Sales Summary · Customer Insights · Forecast Reports
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.markdown("---")

# ----------------------------------
# Technologies
# ----------------------------------
section_header("🛠️", "Technologies Used")
badge_row(["Python", "Streamlit", "Plotly", "Prophet", "XGBoost", "K-Means", "Pandas"])

st.write("")
st.markdown("---")

# ----------------------------------
# About the Project
# ----------------------------------
section_header("📖", "About the Project")

st.markdown(
    """
    <div class="nr-card">
        <p style="font-size:0.92rem; color:#334155; line-height:1.6;">
            <b>NeuralRetail Analytics Dashboard</b> is an AI-powered retail analytics solution
            developed to help businesses make data-driven decisions.
        </p>
        <b>Objectives</b>
        <ul style="font-size:0.88rem; color:#475569;">
            <li>Forecast future sales using Prophet</li>
            <li>Predict customer churn using XGBoost</li>
            <li>Segment customers using K-Means clustering</li>
            <li>Generate business insights through interactive dashboards</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.markdown("---")

# ----------------------------------
# Executive Summary
# ----------------------------------
section_header("📊", "Executive Summary")

left, right = st.columns(2)
with left:
    insight_box("📈", "Revenue is increasing steadily.", kind="success")
    insight_box("🎯", "Customer retention is improving.", kind="success")
    insight_box("📅", "Sales forecast available for the next 30 days.", kind="success")
with right:
    insight_box("🤖", "Churn model trained using XGBoost.", kind="info")
    insight_box("🧩", "Segmentation completed using K-Means.", kind="info")
    insight_box("✅", "Reports generated successfully.", kind="info")

st.markdown("---")
st.caption("NeuralRetail Analytics Dashboard | Built with Streamlit, Prophet, XGBoost, Plotly & Scikit-learn")
