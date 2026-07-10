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
load_theme("Customer Segmentation", "🎯")
render_sidebar(active_page="Customer Segmentation")

gradient_banner(
    eyebrow="Customer Intelligence",
    title="🎯 Customer Segmentation Dashboard",
    subtitle="K-Means clustering on RFM (Recency, Frequency, Monetary) behaviour to group "
              "customers into actionable marketing segments.",
    color="teal",
)

# -----------------------------
# Load Data (unchanged logic)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
segment_file = BASE_DIR / "data" / "features" / "segments.csv"

if segment_file.exists():

    df = pd.read_csv(segment_file)

    st.success("✅ Customer segments loaded successfully!")

    # -----------------------------
    # KPI Cards
    # -----------------------------
    section_header("📌", "Segmentation KPIs")

    kpi_row([
        {"icon": "👥", "label": "Total Customers", "value": f"{len(df):,}", "color": "blue"},
        {"icon": "🧩", "label": "Segments", "value": f"{df['SegmentName'].nunique()}", "color": "purple"},
        {"icon": "🏆", "label": "Largest Segment", "value": df["SegmentName"].value_counts().idxmax(), "color": "teal"},
    ])

    st.write("")
    st.markdown("---")

    # -----------------------------
    # Customer Table
    # -----------------------------
    section_header("📋", "Customer Segmentation Data")

    st.dataframe(
        df[["Recency", "Frequency", "Monetary", "SegmentName"]],
        use_container_width=True,
    )

    st.markdown("---")

    # -----------------------------
    # Charts
    # -----------------------------
    section_header("📊", "Segment Analysis")

    left, right = st.columns(2)

    with left:
        fig = px.pie(
            df,
            names="SegmentName",
            title="Customer Segment Distribution",
            color_discrete_sequence=CHART_COLORS,
            hole=0.45,
        )
        fig.update_traces(
            textinfo="percent+label",
            hovertemplate="%{label}: %{value} customers (%{percent})<extra></extra>",
        )
        st.plotly_chart(style_fig(fig, height=380), use_container_width=True)

    with right:
        counts = df["SegmentName"].value_counts().reset_index()
        counts.columns = ["SegmentName", "count"]
        fig2 = px.bar(
            counts,
            x="SegmentName",
            y="count",
            title="Customers in Each Segment",
            labels={"SegmentName": "Segment", "count": "Customers"},
            color="SegmentName",
            color_discrete_sequence=CHART_COLORS,
        )
        fig2.update_traces(hovertemplate="%{x}: %{y} customers<extra></extra>")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig2, height=380), use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Scatter Plot
    # -----------------------------
    section_header("📊", "RFM Customer Segments")

    fig3 = px.scatter(
        df,
        x="Frequency",
        y="Monetary",
        color="SegmentName",
        size="Recency",
        hover_name="SegmentName",
        title="Frequency vs Monetary by Segment",
        labels={"Frequency": "Purchase Frequency", "Monetary": "Total Spend"},
        color_discrete_sequence=CHART_COLORS,
    )
    fig3.update_traces(hovertemplate="Frequency: %{x}<br>Monetary: %{y:,.0f}<extra></extra>")
    st.plotly_chart(style_fig(fig3, height=460), use_container_width=True)

    # -----------------------------
    # Marketing Strategy
    # -----------------------------
    st.markdown("---")
    section_header("💡", "Marketing Strategy")

    insight_box("🏆", "<b>Champions</b> → Reward with exclusive offers.", kind="success")
    insight_box("❤️", "<b>Loyal Customers</b> → Membership & loyalty programs.", kind="success")
    insight_box("⚠️", "<b>At Risk</b> → Discounts and retention campaigns.", kind="warning")
    insight_box("🆕", "<b>New Customers</b> → Welcome offers.", kind="info")
    insight_box("💤", "<b>Hibernating</b> → Email re-engagement.", kind="info")
    insight_box("❌", "<b>Lost Customers</b> → Win-back campaigns.", kind="danger")

    # -----------------------------
    # Download Button
    # -----------------------------
    st.write("")
    with open(segment_file, "rb") as file:
        st.download_button(
            "⬇ Download Segmentation Report",
            file,
            file_name="segments.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.caption("NeuralRetail Analytics Dashboard | Built with Streamlit • K-Means • Plotly")

else:
    st.error("❌ segments.csv not found. Run segmentation.py first.")
