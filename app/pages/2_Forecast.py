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
load_theme("Demand Forecast", "📈")
render_sidebar(active_page="Demand Forecast")

gradient_banner(
    eyebrow="Predictive Intelligence",
    title="📈 Demand Forecast Dashboard",
    subtitle="AI-powered 30-day sales forecast generated using the Prophet time-series model, "
              "with confidence intervals to support inventory and planning decisions.",
    color="blue",
)

# -----------------------------
# Load Forecast Data (unchanged logic)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
forecast_path = BASE_DIR / "data" / "features" / "forecast.csv"

if forecast_path.exists():

    forecast = pd.read_csv(forecast_path)
    forecast["ds"] = pd.to_datetime(forecast["ds"])

    st.success("✅ Forecast loaded successfully!")

    # -----------------------------
    # KPI Cards
    # -----------------------------
    section_header("📌", "Forecast KPIs")

    kpi_row([
        {"icon": "📅", "label": "Forecast Days", "value": "30", "color": "blue"},
        {"icon": "🚀", "label": "Maximum Sales", "value": f"{forecast['yhat'].max():,.0f}", "color": "purple"},
        {"icon": "📊", "label": "Average Sales", "value": f"{forecast['yhat'].mean():,.0f}", "color": "teal"},
    ])

    st.write("")
    st.markdown("---")

    # -----------------------------
    # Forecast Table
    # -----------------------------
    section_header("📋", "Forecast Data")

    st.dataframe(
        forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].rename(
            columns={
                "ds": "Date",
                "yhat": "Forecasted Sales",
                "yhat_lower": "Lower Bound",
                "yhat_upper": "Upper Bound",
            }
        ),
        use_container_width=True,
    )

    st.markdown("---")

    # -----------------------------
    # Forecast Chart
    # -----------------------------
    section_header("📈", "Sales Forecast")

    fig = px.line(
        forecast,
        x="ds",
        y="yhat",
        markers=True,
        title="30-Day Sales Forecast",
        labels={"ds": "Date", "yhat": "Forecasted Sales"},
        color_discrete_sequence=[CHART_COLORS[0]],
    )
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Forecast: %{y:,.0f}<extra></extra>",
    )
    st.plotly_chart(style_fig(fig), use_container_width=True)

    # -----------------------------
    # Confidence Interval
    # -----------------------------
    section_header("📊", "Prediction Interval")

    fig2 = px.line(
        forecast,
        x="ds",
        y=["yhat_lower", "yhat", "yhat_upper"],
        title="Forecast with Confidence Interval",
        labels={"ds": "Date", "value": "Sales", "variable": "Series"},
        color_discrete_sequence=CHART_COLORS,
    )
    fig2.for_each_trace(lambda t: t.update(
        name={"yhat_lower": "Lower Bound", "yhat": "Forecast", "yhat_upper": "Upper Bound"}.get(t.name, t.name)
    ))
    fig2.update_traces(hovertemplate="%{y:,.0f}<extra></extra>")
    st.plotly_chart(style_fig(fig2), use_container_width=True)

    # -----------------------------
    # Business Insights
    # -----------------------------
    st.markdown("---")
    section_header("💡", "Business Insights")

    insight_box("📈", "Sales are expected to increase over the forecast period.", kind="success")
    insight_box("📦", "Inventory planning should focus on high-demand periods.", kind="info")
    insight_box("🛒", "Use the forecast to reduce stock-outs and excess inventory.", kind="info")
    insight_box("🤖", "Forecast generated using the Prophet time-series model.", kind="info")

    # -----------------------------
    # Download Button
    # -----------------------------
    st.write("")
    with open(forecast_path, "rb") as file:
        st.download_button(
            label="⬇ Download Forecast CSV",
            data=file,
            file_name="forecast.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.caption("NeuralRetail Analytics Dashboard | Built with Streamlit • Prophet • Plotly")

else:
    st.error("❌ forecast.csv not found. Please run demand_forecast.py first.")
