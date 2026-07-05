import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="🎯",
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
st.title("🎯 Customer Segmentation Dashboard")
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

segment_file = BASE_DIR / "data" / "features" / "segments.csv"

if segment_file.exists():

    df = pd.read_csv(segment_file)

    st.success("Customer segments loaded successfully!")

    # -----------------------------
    # KPI Cards
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Customers",
        len(df)
    )

    col2.metric(
        "Segments",
        df["SegmentName"].nunique()
    )

    col3.metric(
        "Largest Segment",
        df["SegmentName"].value_counts().idxmax()
    )

    st.markdown("---")

    # -----------------------------
    # Customer Table
    # -----------------------------
    st.subheader("📋 Customer Segmentation Data")

    st.dataframe(
        df[
            [
                "Recency",
                "Frequency",
                "Monetary",
                "SegmentName"
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
            names="SegmentName",
            title="Customer Segment Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig2 = px.bar(
            df["SegmentName"].value_counts().reset_index(),
            x="SegmentName",
            y="count",
            title="Customers in Each Segment"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # -----------------------------
    # Scatter Plot
    # -----------------------------
    st.subheader("📊 RFM Customer Segments")

    fig3 = px.scatter(
        df,
        x="Frequency",
        y="Monetary",
        color="SegmentName",
        size="Recency",
        hover_name="SegmentName",
        title="Frequency vs Monetary"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # -----------------------------
    # Marketing Strategy
    # -----------------------------
    st.markdown("---")

    st.subheader("💡 Marketing Strategy")

    st.info("""
🏆 **Champions** → Reward with exclusive offers

❤️ **Loyal Customers** → Membership & loyalty programs

⚠ **At Risk** → Discounts and retention campaigns

🆕 **New Customers** → Welcome offers

💤 **Hibernating** → Email re-engagement

❌ **Lost Customers** → Win-back campaigns
""")

    # -----------------------------
    # Download Button
    # -----------------------------
    with open(segment_file, "rb") as file:

        st.download_button(
            "⬇ Download Segmentation Report",
            file,
            file_name="segments.csv",
            mime="text/csv"
        )

    # -----------------------------
    # Footer
    # -----------------------------
    st.markdown("---")

    st.caption(
        "NeuralRetail Analytics Dashboard | Built with Streamlit • K-Means • Plotly"
    )

else:

    st.error("❌ segments.csv not found. Run segmentation.py first.")
st.info("""
🎯 **Business Insight**

Customer segmentation groups customers based on purchasing behavior,
helping businesses create targeted marketing campaigns and improve customer engagement.
""")