import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder
import base64
import os

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NCD Supply Chain Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS Theme ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080C14 !important;
    color: #E8EDF5 !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,195,255,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,107,53,0.06) 0%, transparent 60%),
        #080C14 !important;
}

[data-testid="stSidebar"] {
    background: #0D1320 !important;
    border-right: 1px solid rgba(0,195,255,0.12) !important;
}
[data-testid="stSidebar"] * { font-family: 'Syne', sans-serif !important; }
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #00C3FF !important;
    font-size: 11px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    padding: 18px 0 8px 0 !important;
    border-bottom: 1px solid rgba(0,195,255,0.15) !important;
    margin-bottom: 12px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #111827 !important;
    border: 1px solid rgba(0,195,255,0.2) !important;
    border-radius: 8px !important;
    color: #E8EDF5 !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(0,195,255,0.15) !important;
    border: 1px solid rgba(0,195,255,0.3) !important;
    color: #00C3FF !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #00C3FF !important;
    border-color: #00C3FF !important;
}
[data-testid="stSidebar"] label {
    color: #8899AA !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
}

.main .block-container {
    padding: 2rem 2.5rem 3rem 2.5rem !important;
    max-width: 1600px !important;
}

[data-testid="stTabs"] [role="tablist"] {
    background: #0D1320 !important;
    border: 1px solid rgba(0,195,255,0.12) !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 4px !important;
    margin-bottom: 28px !important;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: #4A5568 !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.3px !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease !important;
    border: none !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: #A0B4C8 !important;
    background: rgba(0,195,255,0.06) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #00C3FF22, #0080FF22) !important;
    color: #00C3FF !important;
    border: 1px solid rgba(0,195,255,0.3) !important;
}

[data-testid="stMetric"] {
    background: #0D1320 !important;
    border: 1px solid rgba(0,195,255,0.1) !important;
    border-radius: 14px !important;
    padding: 20px 22px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00C3FF, #0080FF);
}
[data-testid="stMetric"] label {
    color: #6B7D8E !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #E8EDF5 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 28px !important;
}
[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}

[data-testid="stDataFrame"] {
    background: #0D1320 !important;
    border: 1px solid rgba(0,195,255,0.1) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #00C3FF, #0066CC) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    padding: 10px 26px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(0,195,255,0.25) !important;
}
[data-testid="stDownloadButton"] button:hover {
    box-shadow: 0 6px 28px rgba(0,195,255,0.4) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 3px !important;
    font-family: 'Syne', sans-serif !important;
}

hr {
    border-color: rgba(0,195,255,0.08) !important;
    margin: 28px 0 !important;
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 32px;
}
.kpi-card {
    background: #0D1320;
    border: 1px solid rgba(0,195,255,0.1);
    border-radius: 14px;
    padding: 20px 22px 18px 22px;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: border-color 0.2s, transform 0.2s;
}
.kpi-card:hover {
    border-color: rgba(0,195,255,0.28);
    transform: translateY(-2px);
}
.kpi-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0;
}
.kpi-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6B7D8E;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: #E8EDF5;
    line-height: 1;
    margin-bottom: 6px;
}
.kpi-desc {
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    color: #4A5568;
    line-height: 1.5;
    margin-bottom: 10px;
}
.kpi-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 99px;
    margin-top: 2px;
}
.badge-blue   { background: rgba(0,195,255,0.12); color: #00C3FF; border: 1px solid rgba(0,195,255,0.2); }
.badge-green  { background: rgba(56,232,166,0.12); color: #38E8A6; border: 1px solid rgba(56,232,166,0.2); }
.badge-amber  { background: rgba(245,158,11,0.12); color: #F59E0B; border: 1px solid rgba(245,158,11,0.2); }
.badge-purple { background: rgba(168,85,247,0.12); color: #A855F7; border: 1px solid rgba(168,85,247,0.2); }
.sparkbar {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 28px;
    margin-top: 12px;
}
.sparkbar span {
    flex: 1;
    border-radius: 2px 2px 0 0;
    opacity: 0.65;
    transition: opacity 0.2s;
}
.sparkbar span:hover { opacity: 1; }
</style>
""", unsafe_allow_html=True)

# ─── Plotly theme ────────────────────────────────────────────────────────────
CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Syne, sans-serif", color="#8899AA", size=12),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.06)",
        tickfont=dict(color="#6B7D8E", size=11),
        title_font=dict(color="#8899AA")
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.06)",
        tickfont=dict(color="#6B7D8E", size=11),
        title_font=dict(color="#8899AA")
    ),
    legend=dict(
        bgcolor="rgba(13,19,32,0.8)",
        bordercolor="rgba(0,195,255,0.15)",
        borderwidth=1,
        font=dict(color="#A0B4C8", size=11)
    ),
    colorway=["#00C3FF", "#FF6B35", "#38E8A6", "#A855F7", "#F59E0B", "#EC4899", "#6366F1"],
    margin=dict(t=50, b=40, l=40, r=20)
)

COLOR_SEQ = ["#00C3FF", "#FF6B35", "#38E8A6", "#A855F7", "#F59E0B", "#EC4899", "#6366F1"]


def style_fig(fig, title=""):
    fig.update_layout(
        **CHART_THEME,
        title=dict(text=title, font=dict(color="#E8EDF5", size=15, family="Syne"), x=0, xanchor="left"),
    )
    return fig


# ─── Load Data & Model ────────────────────────────────────────────────────────
@st.cache_resource
def load_resources():
    model = joblib.load("C:/Users/vincy/Desktop/Unified Mentor Internship/Project 1/data_scaler.pkl.gz")
    df = pd.read_csv('C:/Users/vincy/Desktop/Unified Mentor Internship/Project 1/NFD_Cleand.csv')
    return model, df


model, df = load_resources()

# ─── Encoders ────────────────────────────────────────────────────────────────
categorical_cols = ['Ship Mode', 'Country/Region', 'City', 'State/Province', 'Division', 'Region', 'Product Name']
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    le.fit(df[col].astype(str))
    encoders[col] = le


def encode_input(input_df):
    processed = input_df.copy()
    for col in categorical_cols:
        processed[col] = encoders[col].transform(processed[col].astype(str))
    return processed


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 24px 0 20px 0; border-bottom: 1px solid rgba(0,195,255,0.15); margin-bottom: 20px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <div style="width:32px; height:32px; background:linear-gradient(135deg,#00C3FF,#0066CC);
                        border-radius:8px; display:flex; align-items:center; justify-content:center;
                        font-size:16px;">⬡</div>
            <span style="font-family:'Syne',sans-serif; font-weight:800; font-size:16px; color:#E8EDF5;">Nassau Candy Intelligence</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Filters")

    all_prods = sorted(df['Product Name'].unique().tolist())
    selected_products = st.multiselect("Products", all_prods, default=[all_prods[0]])

    all_regions = sorted(df['Region'].unique().tolist())
    selected_regions = st.multiselect("Regions", all_regions, default=all_regions)

    all_modes = df['Ship Mode'].unique().tolist()
    selected_modes = st.multiselect("Ship Modes", all_modes, default=all_modes)

    st.markdown("### Optimization")
    opt_priority = st.slider(
        "Priority  —  Profit ← · → Speed",
        0.0, 1.0, 0.5, step=0.05
    )

    st.markdown("""
    <div style="margin-top:32px; padding:14px 16px; background:rgba(0,195,255,0.05);
                border:1px solid rgba(0,195,255,0.12); border-radius:10px;">
        <p style="font-family:'DM Mono',monospace; font-size:10px; color:#4A5568;
                  letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px;">Model</p>
        <p style="font-family:'Syne',sans-serif; font-size:13px; color:#38E8A6; font-weight:600;">
            ● Live — Lead Time Predictor
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─── Filter Data ──────────────────────────────────────────────────────────────
mask = (
    df['Product Name'].isin(selected_products) &
    df['Region'].isin(selected_regions) &
    df['Ship Mode'].isin(selected_modes)
)
filtered_df = df[mask].copy()

# ─── Header ───────────────────────────────────────────────────────────────────
def get_b64(path):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

logo_path = "C:/Users/vincy/Desktop/Unified Mentor Internship/Project 1/logo.png"
logo_b64 = get_b64(logo_path)
logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""

st.markdown(f"""
<div style="
    display:flex; align-items:center; justify-content:space-between;
    padding: 28px 36px;
    background: linear-gradient(135deg, #0D1320 0%, #111827 100%);
    border: 1px solid rgba(0,195,255,0.12);
    border-radius: 18px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
">
  <div style="position:absolute;top:-60px;right:-60px;width:260px;height:260px;
              background:radial-gradient(circle, rgba(0,195,255,0.08) 0%, transparent 70%);
              pointer-events:none;"></div>
  <div style="display:flex; align-items:center; gap:22px; z-index:1;">
    {'<div style="width:64px;height:64px;background:#FFFFFF;border:1px solid rgba(0,195,255,0.2);border-radius:14px;display:flex;align-items:center;justify-content:center;"><img src="' + logo_src + '" style="max-width:46px;max-height:46px;object-fit:contain;"></div>' if logo_src else '<div style="width:64px;height:64px;background:linear-gradient(135deg,#00C3FF22,#0066CC22);border:1px solid rgba(0,195,255,0.2);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:28px;">⬡</div>'}
    <div>
      <h1 style="font-family:'Syne',sans-serif;font-weight:800;font-size:26px;
                 color:#E8EDF5;margin:0;line-height:1.1;">Factory Reallocation & Shipping Optimization Recommendation System for Nassau Candy Distributor</h1>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;align-items:flex-end;gap:8px;z-index:1;">
    <div style="display:flex;align-items:center;gap:6px;
                background:rgba(56,232,166,0.1);border:1px solid rgba(56,232,166,0.25);
                border-radius:50px;padding:5px 14px;">
      <span style="width:6px;height:6px;border-radius:50%;background:#38E8A6;
                   box-shadow:0 0 8px #38E8A6;display:inline-block;"></span>
      <span style="font-family:'DM Mono',monospace;font-size:11px;color:#38E8A6;letter-spacing:1px;">SYSTEM LIVE</span>
    </div>
    <div style="font-family:'DM Mono',monospace;font-size:11px;color:#2D3748;">
        {len(df):,} records indexed
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Guard ────────────────────────────────────────────────────────────────────
if filtered_df.empty:
    st.markdown("""
    <div style="background:#0D1320;border:1px solid rgba(255,107,53,0.25);border-radius:14px;
                padding:28px 32px;text-align:center;margin-top:20px;">
        <p style="font-size:32px;margin-bottom:10px;">⚠️</p>
        <h3 style="font-family:'Syne',sans-serif;color:#FF6B35;font-weight:700;margin-bottom:6px;">
            No Data Matches Your Filters
        </h3>
        <p style="font-family:'Syne',sans-serif;color:#4A5568;font-size:14px;">
            Adjust the Control Panel on the left to see results.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🚀  Factory Simulator",
    "⚖️  What-If Analysis",
    "📋  Recommendations",
    "🚨  Risk & Impact"
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Factory Simulator
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:20px;color:#E8EDF5;margin-bottom:4px;">
        Factory Performance & Financial Overview
    </h2>
    """, unsafe_allow_html=True)

    features = ['Ship Mode', 'Customer ID', 'Country/Region', 'City', 'State/Province',
                'Postal Code', 'Division', 'Region', 'Product Name', 'Sales', 'Units', 'Gross Profit', 'Cost']
    X_sim = encode_input(filtered_df[features])
    filtered_df['Predicted_Lead_Time'] = model.predict(X_sim)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <div style="width:3px;height:18px;background:linear-gradient(180deg,#00C3FF,#0066CC);border-radius:2px;"></div>
        <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;color:#E8EDF5;">
            Lead Time Predictions by Product & Region
        </span>
    </div>
    """, unsafe_allow_html=True)

    fig_lt = px.bar(
        filtered_df, x='Product Name', y='Predicted_Lead_Time', color='Region',
        barmode='group', labels={'Predicted_Lead_Time': 'Lead Time (Days)'},
        color_discrete_sequence=COLOR_SEQ
    )
    fig_lt.update_traces(marker_line_width=0, opacity=0.9)
    style_fig(fig_lt, "")
    st.plotly_chart(fig_lt, use_container_width=True)

    st.divider()

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <div style="width:3px;height:18px;background:linear-gradient(180deg,#FF6B35,#FF3D00);border-radius:2px;"></div>
        <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;color:#E8EDF5;">
            Financial Analysis by Division
        </span>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        fig_sales = px.pie(
            filtered_df, values='Sales', names='Division',
            hole=0.55, color_discrete_sequence=COLOR_SEQ
        )
        fig_sales.update_traces(
            textfont=dict(family="Syne, sans-serif", color="#E8EDF5", size=12),
            marker=dict(line=dict(color="#080C14", width=2)),
        )
        fig_sales.update_layout(
            **CHART_THEME,
            title=dict(text="Sales by Division", font=dict(color="#E8EDF5", size=14, family="Syne"), x=0),
            showlegend=True,
            annotations=[dict(
                text=f"<b style='font-size:16px;color:#E8EDF5'>Sales</b>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(family="Syne", size=14, color="#8899AA")
            )]
        )
        st.plotly_chart(fig_sales, use_container_width=True)

    with col_b:
        fig_cost = px.bar(
            filtered_df, x='Division', y='Cost', color='Region',
            barmode='stack', color_discrete_sequence=COLOR_SEQ
        )
        fig_cost.update_traces(marker_line_width=0)
        style_fig(fig_cost, "Operational Cost by Division")
        st.plotly_chart(fig_cost, use_container_width=True)

    st.divider()

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <div style="width:3px;height:18px;background:linear-gradient(180deg,#38E8A6,#00A86B);border-radius:2px;"></div>
        <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;color:#E8EDF5;">
            Profitability Matrix
        </span>
    </div>
    """, unsafe_allow_html=True)

    fig_profit = px.scatter(
        filtered_df, x='Sales', y='Gross Profit', size='Units',
        color='Product Name', hover_name='Product Name',
        labels={'Gross Profit': 'Gross Profit ($)', 'Sales': 'Sales ($)'},
        color_discrete_sequence=COLOR_SEQ
    )
    fig_profit.add_hline(y=0, line_dash="dot", line_color="rgba(255,107,53,0.5)", line_width=1.5)
    fig_profit.update_traces(marker=dict(opacity=0.85, line=dict(width=0)))
    style_fig(fig_profit, "Sales vs. Gross Profit — bubble size = Units")
    st.plotly_chart(fig_profit, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — What-If Scenario Analysis
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:20px;color:#E8EDF5;margin-bottom:4px;">
        What-If Scenario Analysis
    </h2>
    <p style="font-family:'DM Mono',monospace;font-size:11px;color:#4A5568;margin-bottom:28px;letter-spacing:1px;">
        ACTUAL vs OPTIMIZED  ·  IMPROVEMENT TRACKING
    </p>
    """, unsafe_allow_html=True)

    avg_actual    = filtered_df['lead_time'].mean()
    avg_predicted = filtered_df['Predicted_Lead_Time'].mean()
    improvement   = avg_actual - avg_predicted
    eff_pct       = (improvement / avg_actual * 100) if avg_actual != 0 else 0

    # ── Compute all four KPI values ──────────────────────────────────────────
    total_items   = len(filtered_df)
    healthy_items = len(filtered_df[filtered_df['Gross Profit'] >= df['Gross Profit'].mean() * 0.5])
    pis_pct       = (healthy_items / total_items * 100) if total_items else 0

    std_dev   = filtered_df['Predicted_Lead_Time'].std()
    mean_val  = filtered_df['Predicted_Lead_Time'].mean()
    conf_score = max(0.0, min(100.0, 100 - (std_dev / mean_val * 10 if mean_val != 0 else 0)))

    coverage = (len(filtered_df) / len(df)) * 100

    # ── Spark bar data (7 trailing bars normalised to 100) ───────────────────
    def spark_bars(final_val, n=7, noise=4):
        import random, math
        bars = []
        for i in range(n):
            frac = (i + 1) / n
            bars.append(round(max(10, min(100, final_val * frac + random.uniform(-noise, noise)))))
        bars[-1] = round(min(100, final_val))
        return bars

    ltr_bars  = spark_bars(min(eff_pct,  100))
    pis_bars  = spark_bars(pis_pct)
    scs_bars  = spark_bars(conf_score)
    rc_bars   = spark_bars(coverage)

    def bars_html(bars, color):
        spans = "".join(
            f'<span style="height:{b}%;background:{color};"></span>'
            for b in bars
        )
        return f'<div class="sparkbar">{spans}</div>'

    # ── KPI Cards HTML ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="kpi-grid">

      <!-- 1. Lead Time Reduction -->
      <div class="kpi-card">
        <div class="kpi-accent" style="background:linear-gradient(90deg,#00C3FF,#0080FF);"></div>
        <div class="kpi-label">Lead Time Reduction</div>
        <div class="kpi-value">{eff_pct:.1f}%</div>
        <div class="kpi-desc">Operational gain vs current avg lead time</div>
        {bars_html(ltr_bars, '#00C3FF')}
        <span class="kpi-badge badge-blue">Operational gain</span>
      </div>

      <!-- 2. Profit Impact Stability -->
      <div class="kpi-card">
        <div class="kpi-accent" style="background:linear-gradient(90deg,#38E8A6,#00A86B);"></div>
        <div class="kpi-label">Profit Impact Stability</div>
        <div class="kpi-value">{pis_pct:.1f}%</div>
        <div class="kpi-desc">Items maintaining healthy profit margins</div>
        {bars_html(pis_bars, '#38E8A6')}
        <span class="kpi-badge badge-green">Financial safety</span>
      </div>

      <!-- 3. Scenario Confidence Score -->
      <div class="kpi-card">
        <div class="kpi-accent" style="background:linear-gradient(90deg,#F59E0B,#FBBF24);"></div>
        <div class="kpi-label">Scenario Confidence Score</div>
        <div class="kpi-value">{conf_score:.1f}%</div>
        <div class="kpi-desc">Reliability based on prediction variance</div>
        {bars_html(scs_bars, '#F59E0B')}
        <span class="kpi-badge badge-amber">Reliability</span>
      </div>

      <!-- 4. Recommendation Coverage -->
      <div class="kpi-card">
        <div class="kpi-accent" style="background:linear-gradient(90deg,#A855F7,#7C3AED);"></div>
        <div class="kpi-label">Recommendation Coverage</div>
        <div class="kpi-value">{coverage:.1f}%</div>
        <div class="kpi-desc">% of total inventory currently filtered</div>
        {bars_html(rc_bars, '#A855F7')}
        <span class="kpi-badge badge-purple">Scalability</span>
      </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # Funnel chart
    comparison_df = pd.DataFrame({
        'Scenario': ['Current (Actual)', 'Optimized (Predicted)'],
        'Days': [round(avg_actual, 1), round(avg_predicted, 1)]
    })
    fig_funnel = go.Figure(go.Funnel(
        y=comparison_df['Scenario'],
        x=comparison_df['Days'],
        textinfo="value+percent initial",
        marker=dict(
            color=["#00C3FF", "#38E8A6"],
            line=dict(width=0)
        ),
        textfont=dict(family="Syne, sans-serif", color="#E8EDF5", size=14),
        connector=dict(line=dict(color="rgba(0,195,255,0.2)", width=1, dash="dot"))
    ))
    fig_funnel.update_layout(
        **CHART_THEME,
        title=dict(text="Lead Time Reduction Funnel", font=dict(color="#E8EDF5", size=15, family="Syne"), x=0),
        height=320
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    st.divider()
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <div style="width:3px;height:18px;background:linear-gradient(180deg,#A855F7,#6366F1);border-radius:2px;"></div>
        <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;color:#E8EDF5;">
            Lead Time Distribution
        </span>
    </div>
    """, unsafe_allow_html=True)

    fig_dist = go.Figure()
    fig_dist.add_trace(go.Histogram(
        x=filtered_df['lead_time'], name="Actual",
        marker_color="#00C3FF", opacity=0.7, nbinsx=30
    ))
    fig_dist.add_trace(go.Histogram(
        x=filtered_df['Predicted_Lead_Time'], name="Optimized",
        marker_color="#38E8A6", opacity=0.7, nbinsx=30
    ))
    fig_dist.update_layout(
        **CHART_THEME,
        barmode='overlay',
        title=dict(text="Actual vs Predicted Lead Time Distribution", font=dict(color="#E8EDF5", size=15, family="Syne"), x=0),
        xaxis_title="Days", yaxis_title="Frequency"
    )
    st.plotly_chart(fig_dist, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — Recommendations
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:20px;color:#E8EDF5;margin-bottom:4px;">
        Optimization Recommendations
    </h2>
    <p style="font-family:'DM Mono',monospace;font-size:11px;color:#4A5568;margin-bottom:28px;letter-spacing:1px;">
        RANKED BY COMPOSITE SCORE  ·  ADJUSTABLE VIA PRIORITY SLIDER
    </p>
    """, unsafe_allow_html=True)

    max_lt = filtered_df['Predicted_Lead_Time'].max() or 1
    max_gp = filtered_df['Gross Profit'].max() or 1

    filtered_df['Score'] = (
        (1 - opt_priority) * (filtered_df['Gross Profit'] / max_gp) +
        opt_priority * (1 - (filtered_df['Predicted_Lead_Time'] / max_lt))
    )

    recs = filtered_df[
        ['Product Name', 'Region', 'Ship Mode', 'Predicted_Lead_Time', 'Gross Profit', 'Score']
    ].sort_values('Score', ascending=False).reset_index(drop=True)
    recs.index += 1

    top10 = recs.head(10)
    fig_bar = px.bar(
        top10.reset_index(), x='Product Name', y='Score',
        color='Score', color_continuous_scale=[[0, '#0D1320'], [0.4, '#00C3FF'], [1, '#38E8A6']],
        labels={'Score': 'Composite Score'}
    )
    fig_bar.update_traces(marker_line_width=0)
    fig_bar.update_layout(
        **CHART_THEME,
        title=dict(text="Top 10 Scored Routes / Products", font=dict(color="#E8EDF5", size=15, family="Syne"), x=0),
        showlegend=False, coloraxis_showscale=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.dataframe(
        recs.style
            .background_gradient(subset=['Score'], cmap='YlGn')
            .format({'Score': '{:.3f}', 'Predicted_Lead_Time': '{:.1f}', 'Gross Profit': '${:,.0f}'}),
        use_container_width=True, height=420
    )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.download_button(
        "📩  Download Full Optimization Report",
        recs.to_csv(index=True),
        "optimization_report.csv",
        mime="text/csv"
    )


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — Risk & Impact
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <h2 style="font-family:'Syne',sans-serif;font-weight:700;font-size:20px;color:#E8EDF5;margin-bottom:4px;">
        Risk Assessment Panel
    </h2>
    <p style="font-family:'DM Mono',monospace;font-size:11px;color:#4A5568;margin-bottom:28px;letter-spacing:1px;">
        FINANCIAL SAFEGUARDS  ·  OPERATIONAL RISK FLAGS  ·  MODEL CONFIDENCE
    </p>
    """, unsafe_allow_html=True)

    r1, r2 = st.columns(2, gap="large")
    with r1:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
            <div style="width:3px;height:18px;background:linear-gradient(180deg,#F59E0B,#D97706);border-radius:2px;"></div>
            <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:14px;color:#E8EDF5;">
                Financial Safeguards
            </span>
        </div>
        """, unsafe_allow_html=True)
        low_margin = filtered_df[filtered_df['Gross Profit'] < (df['Gross Profit'].mean() * 0.5)]
        if not low_margin.empty:
            st.error(f"🚨 **{len(low_margin)} items** are significantly below average profit margins.")
        else:
            st.success("💎 All selected items maintain healthy profit margins.")

    with r2:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">
            <div style="width:3px;height:18px;background:linear-gradient(180deg,#EC4899,#DB2777);border-radius:2px;"></div>
            <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:14px;color:#E8EDF5;">
                Operational Risks
            </span>
        </div>
        """, unsafe_allow_html=True)
        high_delay = filtered_df[filtered_df['Predicted_Lead_Time'] > 10]
        if not high_delay.empty:
            st.warning(f"⚠️ **{len(high_delay)} scenarios** still exceed the 10-day lead time threshold.")
        else:
            st.info("✅ All predicted paths are within operational speed targets.")

    st.divider()

    # ── Risk scatter ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <div style="width:3px;height:18px;background:linear-gradient(180deg,#6366F1,#4F46E5);border-radius:2px;"></div>
        <span style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;color:#E8EDF5;">
            Risk Landscape — Lead Time vs Gross Profit
        </span>
    </div>
    """, unsafe_allow_html=True)

    fig_risk = px.scatter(
        filtered_df, x='Predicted_Lead_Time', y='Gross Profit',
        color='Region', size='Cost', hover_name='Product Name',
        color_discrete_sequence=COLOR_SEQ,
        labels={'Predicted_Lead_Time': 'Predicted Lead Time (Days)', 'Gross Profit': 'Gross Profit ($)'}
    )
    fig_risk.add_vline(x=10, line_dash="dot", line_color="rgba(255,107,53,0.5)", line_width=1.5,
                       annotation_text="10-Day Threshold", annotation_font_color="#FF6B35",
                       annotation_font_size=11)
    fig_risk.add_hline(y=df['Gross Profit'].mean() * 0.5, line_dash="dot",
                       line_color="rgba(245,158,11,0.5)", line_width=1.5,
                       annotation_text="Low Margin Zone", annotation_font_color="#F59E0B",
                       annotation_font_size=11)
    fig_risk.update_traces(marker=dict(opacity=0.8, line=dict(width=0)))
    style_fig(fig_risk, "")
    st.plotly_chart(fig_risk, use_container_width=True)
