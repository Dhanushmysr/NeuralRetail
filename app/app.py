import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))
from utils.theme import load_theme, gradient_banner, section_header, kpi_row, render_sidebar, insight_box

# ----------------------------------
# Theme + Page Configuration
# ----------------------------------
load_theme("Home", "🛍️")

# ----------------------------------
# Sidebar
# ----------------------------------
render_sidebar(active_page="Home")

# ----------------------------------
# Try to load real data for headline numbers (falls back gracefully)
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
clean_path = BASE_DIR / "data" / "processed" / "clean_data.csv"

total_customers = total_products = None
total_revenue = None

if clean_path.exists():
    try:
        df = pd.read_csv(clean_path)
        total_customers = df["Customer ID"].nunique()
        total_products = df["Description"].nunique()
        total_revenue = df["TotalAmount"].sum()
    except Exception:
        pass

# ----------------------------------
# Hero Banner
# ----------------------------------
gradient_banner(
    eyebrow="AI-Powered Retail Analytics",
    title="🛍️ NeuralRetail Analytics Dashboard",
    subtitle=(
        "NeuralRetail helps retailers forecast demand, predict customer churn, "
        "segment customers, and generate business insights for better, data-driven "
        "decision-making — powered by Prophet, XGBoost, and K-Means."
    ),
    color="blue",
)

# ----------------------------------
# Top-line KPIs
# ----------------------------------
section_header("📌", "Platform at a Glance")

kpi_items = [
    {"icon": "📦", "label": "Modules", "value": "5", "color": "blue"},
    {"icon": "🤖", "label": "ML Models", "value": "3", "color": "purple"},
    {"icon": "📅", "label": "Forecast Horizon", "value": "30 Days", "color": "teal"},
    {"icon": "✅", "label": "Status", "value": "Active", "color": "green"},
]
kpi_row(kpi_items)

st.write("")

if total_customers is not None:
    section_header("📊", "Business Snapshot")
    kpi_row([
        {"icon": "👥", "label": "Customers", "value": f"{total_customers:,}", "color": "pink"},
        {"icon": "🛒", "label": "Products", "value": f"{total_products:,}", "color": "orange"},
        {"icon": "💰", "label": "Total Revenue", "value": f"₹{total_revenue:,.0f}", "color": "green"},
        {"icon": "📈", "label": "Forecast", "value": "30 Days", "color": "blue"},
    ])
    st.write("")

st.markdown("---")

# ----------------------------------
# Modules
# ----------------------------------
section_header("🚀", "Key Features")

modules = [
    ("📈", "Demand Forecasting", "Predict future product sales using Prophet time-series forecasting.", "blue"),
    ("👥", "Customer Churn", "Identify customers likely to leave using an XGBoost classifier.", "purple"),
    ("🎯", "Customer Segmentation", "Group customers by purchasing behaviour using K-Means clustering.", "teal"),
    ("💡", "Business Insights", "Executive-level KPIs, trends, and actionable recommendations.", "orange"),
]

cols = st.columns(4)
for col, (icon, title, desc, color) in zip(cols, modules):
    with col:
        st.markdown(
            f"""
            <div class="nr-card">
                <div style="font-size:1.6rem;">{icon}</div>
                <div style="font-weight:700; color:#0F172A; margin:6px 0 4px 0;">{title}</div>
                <div style="font-size:0.85rem; color:#475569; line-height:1.5;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
st.markdown("---")

# ----------------------------------
# Technology Stack
# ----------------------------------
section_header("🛠️", "Technologies Used")

tech_cols = st.columns(4)
techs = [("🐍", "Python"), ("⚡", "Streamlit"), ("🤖", "XGBoost"), ("📊", "Prophet & Plotly")]
for col, (icon, name) in zip(tech_cols, techs):
    with col:
        st.markdown(
            f"""
            <div class="nr-card" style="text-align:center;">
                <div style="font-size:1.5rem;">{icon}</div>
                <div style="font-weight:600; color:#1E293B; margin-top:4px;">{name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
st.markdown("---")

# ----------------------------------
# Business Benefits
# ----------------------------------
section_header("💡", "Business Benefits")

left, right = st.columns(2)
with left:
    insight_box("📦", "Better inventory planning through demand forecasting.", kind="success")
    insight_box("🎯", "Reduced customer churn through early risk identification.", kind="success")
    insight_box("😊", "Improved customer satisfaction via personalized engagement.", kind="success")
with right:
    insight_box("🤖", "AI-based sales forecasting powered by Prophet.", kind="info")
    insight_box("📣", "Targeted marketing based on customer segments.", kind="info")
    insight_box("📊", "Data-driven decision making across the business.", kind="info")

st.markdown("---")
st.caption("NeuralRetail Analytics Dashboard | Built with ❤️ using Streamlit, XGBoost, Prophet, Plotly & Scikit-learn")
