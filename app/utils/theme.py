"""
Shared theme, styling, and reusable UI components for the NeuralRetail
Streamlit app.

Every page calls `load_theme()` once near the top, then uses the helper
functions below (kpi_card, kpi_row, section_header, gradient_banner,
insight_box) to render consistent, professional UI without repeating
CSS/HTML in every file.

IMPORTANT: This module only affects presentation. It does not read, alter,
or depend on any forecasting/ML logic — those live in src/ and are loaded
independently by each page exactly as before.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Color palette (single source of truth for the whole app)
# ---------------------------------------------------------------------------

PALETTE = {
    "blue":   {"grad": "linear-gradient(135deg,#2563EB,#1E40AF)", "solid": "#2563EB", "soft": "#EFF6FF"},
    "teal":   {"grad": "linear-gradient(135deg,#0D9488,#0F766E)", "solid": "#0D9488", "soft": "#F0FDFA"},
    "purple": {"grad": "linear-gradient(135deg,#7C3AED,#5B21B6)", "solid": "#7C3AED", "soft": "#F5F3FF"},
    "pink":   {"grad": "linear-gradient(135deg,#DB2777,#9D174D)", "solid": "#DB2777", "soft": "#FDF2F8"},
    "green":  {"grad": "linear-gradient(135deg,#16A34A,#15803D)", "solid": "#16A34A", "soft": "#F0FDF4"},
    "orange": {"grad": "linear-gradient(135deg,#EA580C,#C2410C)", "solid": "#EA580C", "soft": "#FFF7ED"},
    "red":    {"grad": "linear-gradient(135deg,#DC2626,#991B1B)", "solid": "#DC2626", "soft": "#FEF2F2"},
    "indigo": {"grad": "linear-gradient(135deg,#4F46E5,#3730A3)", "solid": "#4F46E5", "soft": "#EEF2FF"},
}

# Plotly discrete color sequence used across every chart for consistency
CHART_COLORS = ["#2563EB", "#0D9488", "#7C3AED", "#DB2777", "#EA580C", "#16A34A", "#4F46E5"]

PLOTLY_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Inter, Segoe UI, sans-serif", size=13, color="#0F172A"),
    title_font=dict(size=18, color="#0F172A"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(t=60, l=10, r=10, b=10),
    hoverlabel=dict(bgcolor="white", font_size=13, bordercolor="#E2E8F0"),
)


def style_fig(fig, height=420):
    """Apply consistent layout/styling to any Plotly figure in one call."""
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig


# ---------------------------------------------------------------------------
# Global CSS + page config
# ---------------------------------------------------------------------------

def load_theme(page_title, page_icon, layout="wide"):
    """Set page config and inject the shared CSS. Call once at the top of
    every page, before any other st.* calls."""

    st.set_page_config(
        page_title=f"{page_title} | NeuralRetail",
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }

        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}

        .main .block-container {
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            max-width: 1300px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        }
        [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
        [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12); }
        [data-testid="stSidebar"] .stCaption { color: #94A3B8 !important; }

        /* Headings */
        h1 { color: #0F172A; font-weight: 800; letter-spacing: -0.5px; }
        h2, h3 { color: #1E293B; font-weight: 700; }

        /* Native metric containers (still used in a few places) */
        div[data-testid="metric-container"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 16px 18px;
            border-radius: 14px;
            box-shadow: 0px 3px 10px rgba(15,23,42,0.06);
        }

        /* Buttons */
        .stButton>button, .stDownloadButton>button {
            border-radius: 10px;
            border: none;
            background: linear-gradient(135deg,#2563EB,#1E40AF);
            color: white;
            font-weight: 600;
            padding: 0.55rem 1.3rem;
            box-shadow: 0px 3px 10px rgba(37,99,235,0.25);
            transition: transform 0.15s ease;
        }
        .stButton>button:hover, .stDownloadButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0px 6px 14px rgba(37,99,235,0.35);
        }

        /* Dataframe */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #E2E8F0;
        }

        hr { margin: 1.6rem 0; border-color: #E2E8F0; }

        /* ---- Custom component classes ---- */

        .nr-banner {
            padding: 28px 32px;
            border-radius: 16px;
            color: white;
            margin-bottom: 24px;
            box-shadow: 0px 10px 24px rgba(15,23,42,0.18);
        }
        .nr-banner-eyebrow {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            opacity: 0.85;
            margin-bottom: 6px;
        }
        .nr-banner-title { font-size: 1.9rem; font-weight: 800; margin: 0 0 6px 0; }
        .nr-banner-subtitle { font-size: 0.98rem; opacity: 0.92; margin: 0; max-width: 780px; line-height: 1.5; }

        .nr-section-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #0F172A;
            margin: 4px 0 14px 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nr-kpi {
            border-radius: 14px;
            padding: 18px 16px;
            color: white;
            height: 100%;
            box-shadow: 0px 6px 16px rgba(15,23,42,0.12);
            transition: transform 0.15s ease;
        }
        .nr-kpi:hover { transform: translateY(-2px); }
        .nr-kpi-icon { font-size: 1.4rem; opacity: 0.95; }
        .nr-kpi-value { font-size: 1.5rem; font-weight: 800; margin-top: 6px; line-height: 1.15; }
        .nr-kpi-label { font-size: 0.78rem; font-weight: 600; opacity: 0.92; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 3px; }
        .nr-kpi-delta { font-size: 0.78rem; margin-top: 6px; opacity: 0.95; }

        .nr-card {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0px 3px 12px rgba(15,23,42,0.05);
            height: 100%;
        }

        .nr-insight {
            display: flex;
            gap: 12px;
            align-items: flex-start;
            background: #FFFFFF;
            border-left: 4px solid #2563EB;
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 10px;
            box-shadow: 0px 2px 8px rgba(15,23,42,0.05);
        }
        .nr-insight-success { border-left-color: #16A34A; }
        .nr-insight-warning { border-left-color: #EA580C; }
        .nr-insight-danger  { border-left-color: #DC2626; }
        .nr-insight-info    { border-left-color: #2563EB; }
        .nr-insight-icon { font-size: 1.1rem; }
        .nr-insight-text { font-size: 0.92rem; color: #1E293B; line-height: 1.5; }

        .nr-badge {
            display: inline-block;
            background: #EFF6FF;
            color: #1D4ED8;
            border: 1px solid #BFDBFE;
            border-radius: 999px;
            padding: 5px 14px;
            font-size: 0.82rem;
            font-weight: 600;
            margin: 3px 4px 3px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def gradient_banner(eyebrow, title, subtitle, color="blue"):
    grad = PALETTE.get(color, PALETTE["blue"])["grad"]
    st.markdown(
        f"""
        <div class="nr-banner" style="background:{grad};">
            <div class="nr-banner-eyebrow">{eyebrow}</div>
            <div class="nr-banner-title">{title}</div>
            <p class="nr-banner-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(icon, title):
    st.markdown(f'<div class="nr-section-title">{icon} {title}</div>', unsafe_allow_html=True)


def kpi_row(items):
    """items: list of dicts with keys icon, label, value, color, delta(optional)"""
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        color = PALETTE.get(item.get("color", "blue"), PALETTE["blue"])["grad"]
        delta_html = f'<div class="nr-kpi-delta">{item["delta"]}</div>' if item.get("delta") else ""
        with col:
            st.markdown(
                f"""
                <div class="nr-kpi" style="background:{color};">
                    <div class="nr-kpi-icon">{item['icon']}</div>
                    <div class="nr-kpi-value">{item['value']}</div>
                    <div class="nr-kpi-label">{item['label']}</div>
                    {delta_html}
                </div>
                """,
                unsafe_allow_html=True,
            )


def insight_box(icon, text, kind="info"):
    st.markdown(
        f"""
        <div class="nr-insight nr-insight-{kind}">
            <span class="nr-insight-icon">{icon}</span>
            <span class="nr-insight-text">{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge_row(labels):
    html = "".join(f'<span class="nr-badge">{label}</span>' for label in labels)
    st.markdown(html, unsafe_allow_html=True)


def render_sidebar(active_page=""):
    st.sidebar.markdown(
        """
        <div style="text-align:center; padding: 8px 0 18px 0;">
            <div style="font-size:1.8rem;">🛍️</div>
            <div style="font-size:1.15rem; font-weight:800; color:white;">NeuralRetail</div>
            <div style="font-size:0.75rem; color:#94A3B8;">AI-Powered Retail Analytics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")

    nav_items = [
        ("🏠", "Home"),
        ("📈", "Demand Forecast"),
        ("👥", "Customer Churn"),
        ("🎯", "Customer Segmentation"),
        ("💡", "Business Insights"),
        ("📄", "Reports"),
    ]

    nav_html = ""
    for icon, label in nav_items:
        is_active = label == active_page
        style = (
            "background:rgba(37,99,235,0.25); border-left:3px solid #2563EB; font-weight:700;"
            if is_active
            else "border-left:3px solid transparent;"
        )
        nav_html += (
            f'<div style="padding:8px 10px; border-radius:6px; margin-bottom:3px; {style}">'
            f'{icon} &nbsp; {label}</div>'
        )

    st.sidebar.markdown(nav_html, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.caption("Version 1.0 · Built with Streamlit")
