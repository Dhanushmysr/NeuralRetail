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

# -----------------------------------
# Theme + Page Configuration
# -----------------------------------
load_theme("Business Insights", "💡")
render_sidebar(active_page="Business Insights")

gradient_banner(
    eyebrow="Executive Intelligence",
    title="💡 Business Insights",
    subtitle="A consolidated, executive-level view of sales performance, demand forecasts, "
              "customer risk, and recommended actions — built from the same forecast, churn, "
              "and segmentation outputs used elsewhere in this dashboard.",
    color="orange",
)

# -----------------------------------
# Load data (all read-only; no model logic touched)
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

clean_path = BASE_DIR / "data" / "processed" / "clean_data.csv"
forecast_path = BASE_DIR / "data" / "features" / "forecast.csv"
churn_path = BASE_DIR / "data" / "features" / "churn_scores.csv"
segment_path = BASE_DIR / "data" / "features" / "segments.csv"

if not clean_path.exists():
    st.error("❌ clean_data.csv not found. Please run the data pipeline first.")
    st.stop()

sales_df = pd.read_csv(clean_path)
sales_df["InvoiceDate"] = pd.to_datetime(sales_df["InvoiceDate"], errors="coerce")

forecast_df = pd.read_csv(forecast_path) if forecast_path.exists() else None
if forecast_df is not None:
    forecast_df["ds"] = pd.to_datetime(forecast_df["ds"])

churn_df = pd.read_csv(churn_path) if churn_path.exists() else None
segment_df = pd.read_csv(segment_path) if segment_path.exists() else None

# -----------------------------------
# Core sales metrics
# -----------------------------------
order_totals = sales_df.groupby("Invoice")["TotalAmount"].sum()

total_sales = order_totals.sum()
total_orders = order_totals.shape[0]
avg_sales = order_totals.mean()
highest_sales = order_totals.max()
lowest_sales = order_totals.min()

monthly = sales_df.groupby("Month")["TotalAmount"].sum().sort_index()
if len(monthly) >= 2:
    last_month, prev_month = monthly.iloc[-1], monthly.iloc[-2]
    growth_pct = ((last_month - prev_month) / abs(prev_month)) * 100 if prev_month != 0 else 0
else:
    growth_pct = 0

product_sales = sales_df.groupby("Description")["TotalAmount"].sum().sort_values(ascending=False)
region_sales = sales_df.groupby("Country")["TotalAmount"].sum().sort_values(ascending=False)

best_product = product_sales.index[0] if len(product_sales) else "N/A"
best_region = region_sales.index[0] if len(region_sales) else "N/A"

# -----------------------------------
# Executive Summary KPIs
# -----------------------------------
section_header("📌", "Executive Summary")

kpi_row([
    {"icon": "💰", "label": "Total Sales", "value": f"₹{total_sales:,.0f}", "color": "green"},
    {"icon": "🧾", "label": "Total Orders", "value": f"{total_orders:,}", "color": "blue"},
    {"icon": "📊", "label": "Average Order Value", "value": f"₹{avg_sales:,.0f}", "color": "purple"},
    {"icon": "📈", "label": "MoM Growth", "value": f"{growth_pct:+.1f}%", "color": "teal" if growth_pct >= 0 else "red"},
])

st.write("")

kpi_row([
    {"icon": "🚀", "label": "Highest Order Value", "value": f"₹{highest_sales:,.0f}", "color": "orange"},
    {"icon": "🪫", "label": "Lowest Order Value", "value": f"₹{lowest_sales:,.0f}", "color": "pink"},
    {"icon": "🏆", "label": "Best-Selling Product", "value": best_product[:22] + ("…" if len(best_product) > 22 else ""), "color": "indigo"},
    {"icon": "🌍", "label": "Top Region", "value": best_region, "color": "blue"},
])

st.write("")
st.caption("Note: month-over-month growth is calculated from the two most recent months present "
           "in the data — if the latest month is only partially recorded, growth % may look "
           "artificially low. Check the trend chart below for full context.")
st.markdown("---")
section_header("📈", "Sales Trend Analysis")

trend_df = monthly.reset_index()
trend_df.columns = ["Month", "TotalSales"]

fig_trend = px.line(
    trend_df,
    x="Month",
    y="TotalSales",
    markers=True,
    title="Monthly Sales Trend",
    labels={"TotalSales": "Total Sales"},
    color_discrete_sequence=[CHART_COLORS[0]],
)
fig_trend.update_traces(line=dict(width=3), hovertemplate="%{x}<br>Sales: ₹%{y:,.0f}<extra></extra>")
st.plotly_chart(style_fig(fig_trend), use_container_width=True)

section_header("🍂", "Seasonal Trends")
sales_df["MonthNum"] = sales_df["InvoiceDate"].dt.month
seasonal = sales_df.groupby("MonthNum")["TotalAmount"].sum().reindex(range(1, 13), fill_value=0)
seasonal_df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "TotalSales": seasonal.values,
})
fig_season = px.bar(
    seasonal_df,
    x="Month",
    y="TotalSales",
    title="Sales by Calendar Month (All Years Combined)",
    color="TotalSales",
    color_continuous_scale=["#DBEAFE", "#2563EB"],
)
fig_season.update_traces(hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>")
fig_season.update_layout(coloraxis_showscale=False)
st.plotly_chart(style_fig(fig_season), use_container_width=True)

st.markdown("---")

# -----------------------------------
# Top / Worst Performing Products
# -----------------------------------
section_header("🏆", "Top & Worst Performing Products")

top_n = 10
top_products = product_sales.head(top_n).reset_index()
top_products.columns = ["Description", "TotalSales"]
worst_products = product_sales[product_sales > 0].tail(top_n).sort_values().reset_index()
worst_products.columns = ["Description", "TotalSales"]

left, right = st.columns(2)
with left:
    fig_top = px.bar(
        top_products.sort_values("TotalSales"),
        x="TotalSales", y="Description",
        orientation="h",
        title="Top 10 Products by Sales",
        color_discrete_sequence=[CHART_COLORS[4]],
    )
    fig_top.update_traces(hovertemplate="%{y}<br>Sales: ₹%{x:,.0f}<extra></extra>")
    st.plotly_chart(style_fig(fig_top, height=420), use_container_width=True)

with right:
    fig_worst = px.bar(
        worst_products,
        x="TotalSales", y="Description",
        orientation="h",
        title="Lowest 10 Performing Products (with sales > 0)",
        color_discrete_sequence=[CHART_COLORS[6]],
    )
    fig_worst.update_traces(hovertemplate="%{y}<br>Sales: ₹%{x:,.0f}<extra></extra>")
    st.plotly_chart(style_fig(fig_worst, height=420), use_container_width=True)

st.markdown("---")

# -----------------------------------
# Region-wise Performance
# -----------------------------------
section_header("🌍", "Region-wise Performance")

region_df = region_sales.head(10).reset_index()
region_df.columns = ["Country", "TotalSales"]

left, right = st.columns([1.3, 1])
with left:
    fig_region = px.bar(
        region_df.sort_values("TotalSales"),
        x="TotalSales", y="Country",
        orientation="h",
        title="Top 10 Regions by Sales",
        color_discrete_sequence=[CHART_COLORS[1]],
    )
    fig_region.update_traces(hovertemplate="%{y}<br>Sales: ₹%{x:,.0f}<extra></extra>")
    st.plotly_chart(style_fig(fig_region, height=420), use_container_width=True)

with right:
    fig_region_pie = px.pie(
        region_df, names="Country", values="TotalSales",
        title="Revenue Share — Top 10 Regions",
        color_discrete_sequence=CHART_COLORS, hole=0.45,
    )
    fig_region_pie.update_traces(hovertemplate="%{label}: ₹%{value:,.0f} (%{percent})<extra></extra>")
    st.plotly_chart(style_fig(fig_region_pie, height=420), use_container_width=True)

st.markdown("---")

# -----------------------------------
# Revenue Distribution (Category-wise proxy)
# -----------------------------------
section_header("📦", "Revenue Distribution")

st.caption("No dedicated product-category column exists in the source data — this view groups "
           "revenue by top individual products as a proxy for category performance.")

fig_dist = px.pie(
    top_products, names="Description", values="TotalSales",
    title="Revenue Share — Top 10 Products",
    color_discrete_sequence=CHART_COLORS, hole=0.4,
)
fig_dist.update_traces(hovertemplate="%{label}: ₹%{value:,.0f} (%{percent})<extra></extra>")
st.plotly_chart(style_fig(fig_dist), use_container_width=True)

st.markdown("---")

# -----------------------------------
# Demand Forecast Summary
# -----------------------------------
section_header("📈", "Demand Forecast Summary")

if forecast_df is not None:
    forecast_avg = forecast_df["yhat"].mean()
    forecast_total = forecast_df["yhat"].sum()
    historical_avg_daily = sales_df.groupby(sales_df["InvoiceDate"].dt.date)["TotalAmount"].sum().mean()
    forecast_vs_history = ((forecast_avg - historical_avg_daily) / historical_avg_daily) * 100 if historical_avg_daily else 0

    kpi_row([
        {"icon": "📅", "label": "Forecast Horizon", "value": f"{len(forecast_df)} Days", "color": "blue"},
        {"icon": "📊", "label": "Avg Daily Forecast", "value": f"₹{forecast_avg:,.0f}", "color": "purple"},
        {"icon": "💰", "label": "Total Forecasted Sales", "value": f"₹{forecast_total:,.0f}", "color": "green"},
        {"icon": "📈", "label": "vs Historical Daily Avg", "value": f"{forecast_vs_history:+.1f}%", "color": "teal" if forecast_vs_history >= 0 else "red"},
    ])
else:
    st.warning("⚠️ forecast.csv not found — run demand_forecast.py to populate this section.")

st.markdown("---")

# -----------------------------------
# Risk Indicators (from churn model)
# -----------------------------------
section_header("🚨", "Risk Indicators")

if churn_df is not None:
    high_risk = churn_df[churn_df["ChurnProbability"] > 0.7]
    risk_share = len(high_risk) / len(churn_df) * 100
    revenue_at_risk = high_risk["Monetary"].sum()

    kpi_row([
        {"icon": "⚠️", "label": "High-Risk Customers", "value": f"{len(high_risk):,}", "color": "red"},
        {"icon": "📉", "label": "Share of Customer Base", "value": f"{risk_share:.1f}%", "color": "orange"},
        {"icon": "💸", "label": "Revenue at Risk", "value": f"₹{revenue_at_risk:,.0f}", "color": "pink"},
    ])
else:
    st.warning("⚠️ churn_scores.csv not found — run churn_model.py to populate this section.")

st.markdown("---")

# -----------------------------------
# Business Recommendations
# -----------------------------------
section_header("💡", "Business Recommendations")

insight_box("📦", f"<b>{best_product}</b> is the top-selling product — ensure consistent stock availability.", kind="success")
insight_box("🌍", f"<b>{best_region}</b> is the strongest region by revenue — prioritize marketing spend and logistics here.", kind="success")
insight_box(
    "📈" if growth_pct >= 0 else "📉",
    f"Month-over-month sales {'grew' if growth_pct >= 0 else 'declined'} by <b>{abs(growth_pct):.1f}%</b> — "
    f"{'sustain current momentum with targeted promotions.' if growth_pct >= 0 else 'investigate causes and consider a re-engagement campaign.'}",
    kind="success" if growth_pct >= 0 else "warning",
)
if churn_df is not None:
    insight_box("🚨", f"<b>{risk_share:.1f}%</b> of customers are high-risk for churn, representing <b>₹{revenue_at_risk:,.0f}</b> in revenue — prioritize retention offers for this segment.", kind="warning")

st.write("")
section_header("📦", "Inventory Suggestions")

insight_box("✅", f"Maintain higher safety stock for <b>{best_product}</b> and other top-10 products to avoid stock-outs.", kind="info")
if forecast_df is not None:
    insight_box(
        "📊",
        f"Forecasted demand is trending {'upward' if forecast_vs_history >= 0 else 'downward'} relative to historical "
        f"averages — {'plan for increased inventory over the next 30 days.' if forecast_vs_history >= 0 else 'consider trimming excess inventory to reduce holding costs.'}",
        kind="info",
    )
insight_box("🐌", "Review slow-moving products (bottom 10 list above) for markdown or bundling opportunities.", kind="info")

st.write("")
section_header("🎯", "Actionable Insights")

insight_box("1️⃣", "Launch a retention campaign targeting high-risk, high-value customers first.", kind="info")
insight_box("2️⃣", f"Double down on marketing in <b>{best_region}</b> where revenue concentration is highest.", kind="info")
insight_box("3️⃣", "Use the 30-day demand forecast to align purchasing and warehouse staffing.", kind="info")
insight_box("4️⃣", "Bundle low-performing products with top sellers to improve sell-through.", kind="info")

st.markdown("---")
st.caption("NeuralRetail Analytics Dashboard | Business Insights | Streamlit • Pandas • Plotly")
