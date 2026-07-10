import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.theme import (
    load_theme, gradient_banner, section_header, kpi_row,
    render_sidebar, insight_box, style_fig, CHART_COLORS,
)

# -----------------------------
# Theme + Page Configuration
# -----------------------------
load_theme("Customer Churn", "👥")
render_sidebar(active_page="Customer Churn")

gradient_banner(
    eyebrow="Retention Intelligence",
    title="👥 Customer Churn Dashboard",
    subtitle="XGBoost-powered churn probabilities for every customer, so retention teams can "
              "act on risk before customers leave.",
    color="purple",
)

# -----------------------------
# Load Data (unchanged logic)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
churn_file = BASE_DIR / "data" / "features" / "churn_scores.csv"

if churn_file.exists():

    df = pd.read_csv(churn_file)

    st.success("✅ Churn scores loaded successfully!")

    # -----------------------------
    # KPI Cards
    # -----------------------------
    section_header("📌", "Churn KPIs")

    high_risk = len(df[df["ChurnProbability"] > 0.7])

    kpi_row([
        {"icon": "👥", "label": "Total Customers", "value": f"{len(df):,}", "color": "blue"},
        {"icon": "📉", "label": "Avg Churn Probability", "value": f"{df['ChurnProbability'].mean():.1%}", "color": "orange"},
        {"icon": "⚠️", "label": "High-Risk Customers", "value": f"{high_risk:,}", "color": "red"},
    ])

    st.write("")
    st.markdown("---")

    # -----------------------------
    # Customer Data
    # -----------------------------
    section_header("📋", "Customer Churn Data")

    st.dataframe(
        df[["Recency", "Frequency", "Monetary", "Churn", "ChurnProbability"]],
        use_container_width=True,
    )

    st.markdown("---")

    # -----------------------------
    # Charts
    # -----------------------------
    section_header("📊", "Churn Analysis")

    left, right = st.columns(2)

    with left:
        fig = px.pie(
            df,
            names="Churn",
            title="Churn Distribution",
            color_discrete_sequence=CHART_COLORS,
            hole=0.45,
        )
        fig.update_traces(
            textinfo="percent+label",
            hovertemplate="%{label}: %{value} customers (%{percent})<extra></extra>",
        )
        st.plotly_chart(style_fig(fig, height=380), use_container_width=True)

    with right:
        fig2 = px.histogram(
            df,
            x="ChurnProbability",
            nbins=20,
            title="Churn Probability Distribution",
            labels={"ChurnProbability": "Churn Probability"},
            color_discrete_sequence=[CHART_COLORS[3]],
        )
        fig2.update_traces(hovertemplate="Probability: %{x:.2f}<br>Customers: %{y}<extra></extra>")
        st.plotly_chart(style_fig(fig2, height=380), use_container_width=True)

    # -----------------------------
    # High Risk Customers
    # -----------------------------
    st.markdown("---")
    section_header("⚠️", "High-Risk Customers")

    insight_box(
        "⚠️",
        f"There are <b>{high_risk}</b> customers with a churn probability greater than <b>70%</b>.",
        kind="warning",
    )
    insight_box("🎁", "Offer personalized discounts to at-risk customers.", kind="info")
    insight_box("💎", "Send loyalty rewards to strengthen retention.", kind="info")
    insight_box("📧", "Launch targeted email campaigns for high-risk segments.", kind="info")
    insight_box("☎️", "Follow up proactively through customer support.", kind="info")

    # -----------------------------
    # Download Button
    # -----------------------------
    st.write("")
    with open(churn_file, "rb") as file:
        st.download_button(
            label="⬇ Download Churn Scores",
            data=file,
            file_name="churn_scores.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.caption("NeuralRetail Analytics Dashboard | Built with Streamlit • XGBoost • Plotly")

else:
    st.error("❌ churn_scores.csv not found. Please run churn_model.py first.")
