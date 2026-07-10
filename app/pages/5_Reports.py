import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.theme import load_theme, gradient_banner, section_header, kpi_row, render_sidebar, insight_box

# -----------------------------------
# Theme + Page Configuration
# -----------------------------------
load_theme("Reports", "📄")
render_sidebar(active_page="Reports")

gradient_banner(
    eyebrow="Consolidated Reporting",
    title="📄 Business Reports Dashboard",
    subtitle="A single view of forecasting, churn prediction, and segmentation outputs, "
              "ready to preview and download.",
    color="indigo",
)

# -----------------------------------
# File Paths (unchanged logic)
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

forecast_file = BASE_DIR / "data" / "features" / "forecast.csv"
churn_file = BASE_DIR / "data" / "features" / "churn_scores.csv"
segment_file = BASE_DIR / "data" / "features" / "segments.csv"

forecast_exists = forecast_file.exists()
churn_exists = churn_file.exists()
segment_exists = segment_file.exists()

# -----------------------------------
# KPI Cards
# -----------------------------------
section_header("📌", "Report Availability")

kpi_row([
    {"icon": "📈", "label": "Forecast Report", "value": "Available" if forecast_exists else "Missing", "color": "blue" if forecast_exists else "red"},
    {"icon": "👥", "label": "Churn Report", "value": "Available" if churn_exists else "Missing", "color": "purple" if churn_exists else "red"},
    {"icon": "🎯", "label": "Segmentation Report", "value": "Available" if segment_exists else "Missing", "color": "teal" if segment_exists else "red"},
])

st.write("")
st.markdown("---")

# -----------------------------------
# Preview Reports
# -----------------------------------
if forecast_exists:
    section_header("📈", "Forecast Report")
    forecast = pd.read_csv(forecast_file)
    st.dataframe(forecast.head(), use_container_width=True)
    st.write("")

if churn_exists:
    section_header("👥", "Churn Report")
    churn = pd.read_csv(churn_file)
    st.dataframe(churn.head(), use_container_width=True)
    st.write("")

if segment_exists:
    section_header("🎯", "Segmentation Report")
    segment = pd.read_csv(segment_file)
    st.dataframe(segment.head(), use_container_width=True)

st.markdown("---")

# -----------------------------------
# Business Summary
# -----------------------------------
section_header("💡", "Business Summary")

if forecast_exists:
    insight_box("✅", "Demand forecast generated successfully.", kind="success")
if churn_exists:
    insight_box("✅", "Customer churn probabilities calculated.", kind="success")
if segment_exists:
    insight_box("✅", "Customer segmentation completed.", kind="success")

insight_box(
    "📊",
    "The dashboard combines machine learning models to help retail businesses predict future "
    "demand, identify customers at risk of churning, segment customers for personalized "
    "marketing, and support better business decisions.",
    kind="info",
)

st.markdown("---")

# -----------------------------------
# Downloads
# -----------------------------------
section_header("⬇️", "Download Reports")

dl1, dl2, dl3 = st.columns(3)

if forecast_exists:
    with dl1:
        with open(forecast_file, "rb") as f:
            st.download_button("📈 Forecast Report", f, file_name="forecast.csv", mime="text/csv")

if churn_exists:
    with dl2:
        with open(churn_file, "rb") as f:
            st.download_button("👥 Churn Report", f, file_name="churn_scores.csv", mime="text/csv")

if segment_exists:
    with dl3:
        with open(segment_file, "rb") as f:
            st.download_button("🎯 Segmentation Report", f, file_name="segments.csv", mime="text/csv")

st.markdown("---")
st.caption("NeuralRetail Analytics Dashboard | Reports Module | Streamlit • XGBoost • Prophet • K-Means")
