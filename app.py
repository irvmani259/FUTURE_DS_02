import re
import io
import warnings
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
warnings.filterwarnings("ignore")

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Churn Analysis System",
    page_icon="https://cdn-icons-gif.flaticon.com/16275/16275733.gif",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS + JS Animations ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0F0E0E; color: #d4d8e2; }

/* ── Keyframes ── */
@keyframes fadeRight {
  0%   { opacity: 0; transform: translateX(-48px); }
  100% { opacity: 1; transform: translateX(0);     }
}

@keyframes fadeRightFast {
  0%   { opacity: 0; transform: translateX(-32px); }
  100% { opacity: 1; transform: translateX(0);     }
}

@keyframes fadeUp {
  0%   { opacity: 0; transform: translateY(22px); }
  100% { opacity: 1; transform: translateY(0);    }
}

@keyframes fadeIn {
  0%   { opacity: 0; }
  100% { opacity: 1; }
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: #0e1117 !important;
  border-right: 1px solid #1e2433;
}
section[data-testid="stSidebar"] * { color: #b0b8cc !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stFileUploader label { color: #7c8ba0 !important; font-size: 0.78rem; }

/* ── Metric cards ── */
div[data-testid="metric-container"] {
  background: linear-gradient(145deg, #0f1420, #141b28);
  border: 1px solid #1e2a3d;
  border-radius: 12px;
  padding: 16px 20px 14px;
  transition: border-color .2s, transform .2s, box-shadow .2s;
  animation: fadeRight 0.65s ease both;
}
div[data-testid="metric-container"]:hover {
  border-color: #3d6fff44;
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(77,159,255,0.10);
}
div[data-testid="metric-container"] label              { color: #6a7898 !important; font-size: 0.73rem; letter-spacing: .05em; text-transform: uppercase; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #e8edf7 !important; font-size: 1.75rem; font-weight: 700; }
div[data-testid="stMetricDelta"] svg { display:none; }

/* Stagger each metric card */
div[data-testid="metric-container"]:nth-child(1) { animation-delay: 0.10s; }
div[data-testid="metric-container"]:nth-child(2) { animation-delay: 0.20s; }
div[data-testid="metric-container"]:nth-child(3) { animation-delay: 0.30s; }
div[data-testid="metric-container"]:nth-child(4) { animation-delay: 0.40s; }
div[data-testid="metric-container"]:nth-child(5) { animation-delay: 0.50s; }
div[data-testid="metric-container"]:nth-child(6) { animation-delay: 0.60s; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: #0e1117; border-bottom: 1px solid #1e2433; gap: 4px;
  animation: fadeRight 0.55s ease both;
  animation-delay: 0.3s;
}
.stTabs [data-baseweb="tab"] {
  background: transparent; color: #6a7898;
  border-radius: 8px 8px 0 0; padding: 10px 18px;
  font-size: 0.85rem; font-weight: 500;
  border: 1px solid transparent; border-bottom: none;
  transition: color .2s, background .2s;
}
.stTabs [aria-selected="true"] {
  background: #141b28 !important; color: #4d9fff !important;
  border-color: #1e2a3d !important;
}

/* ── Cards ── */
.card {
  background: linear-gradient(145deg, #0f1420, #111827);
  border: 1px solid #1e2a3d; border-radius: 14px;
  padding: 22px 26px; margin-bottom: 18px;
  animation: fadeRight 0.65s ease both;
  animation-delay: 0.25s;
}
.card-title {
  font-size: 0.78rem; font-weight: 600; color: #4d9fff;
  letter-spacing: .08em; text-transform: uppercase; margin-bottom: 14px;
}

/* ── Hero ── */
.hero {
  background: linear-gradient(140deg, #0b1220 0%, #112E81 60%, #0b1220 100%);
  border: 1px solid #1e2a3d; border-radius: 16px;
  padding: 30px 36px; margin-bottom: 24px;
  position: relative; overflow: hidden;
  animation: fadeRight 0.80s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.hero::before {
  content: '';
  position: absolute; top: -60px; right: -60px;
  width: 220px; height: 220px;
  background: radial-gradient(circle, #1a4fff22 0%, transparent 70%);
  border-radius: 50%;
  animation: fadeIn 1.2s ease both;
  animation-delay: 0.6s;
}
.hero h1 { font-size: 1.85rem; font-weight: 700; color: #e8edf7; margin: 0 0 8px; }
.hero p  { font-size: 0.92rem; color: #6a7898; margin: 0; }
.hero .badge {
  display: inline-block; background: #1a3a6e; color: #4d9fff;
  font-size: 0.7rem; font-weight: 600; letter-spacing: .06em;
  padding: 3px 10px; border-radius: 20px; margin-bottom: 12px;
  border: 1px solid #2a5aaa44;
  animation: fadeRight 0.5s ease both;
  animation-delay: 0.4s;
}

/* ── Insight boxes ── */
.insight {
  display: flex; gap: 12px; align-items: flex-start;
  background: #0f1420; border: 1px solid #1e2a3d; border-radius: 10px;
  padding: 13px 16px; margin: 7px 0; font-size: 0.87rem; color: #b0b8cc;
  animation: fadeRight 0.55s ease both;
  transition: border-color .2s, transform .2s;
}
.insight:hover { border-color: #2a3a55; transform: translateX(4px); }
.insight .icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }
.insight b     { color: #4d9fff; }
.insight.warn  { border-color: #8b4a00; background: #130c00; }
.insight.good  { border-color: #1a5c2e; background: #071209; }
.insight.bad   { border-color: #7a1a1a; background: #130606; }

/* Stagger insights */
.insight:nth-child(1) { animation-delay: 0.10s; }
.insight:nth-child(2) { animation-delay: 0.20s; }
.insight:nth-child(3) { animation-delay: 0.30s; }
.insight:nth-child(4) { animation-delay: 0.40s; }
.insight:nth-child(5) { animation-delay: 0.50s; }
.insight:nth-child(6) { animation-delay: 0.60s; }
.insight:nth-child(7) { animation-delay: 0.70s; }
.insight:nth-child(8) { animation-delay: 0.80s; }
/* ── Section headers ── */
.sec-hdr {
  font-size: 0.78rem; font-weight: 600; color: #4d9fff;
  letter-spacing: .08em; text-transform: uppercase;
  border-left: 3px solid #2a5aff; padding-left: 10px;
  margin: 24px 0 12px;
  animation: fadeRight 0.5s ease both;
  animation-delay: 0.15s;
}

/* ── Recommendation cards ── */
.rec-card {
  background: #0f1420; border: 1px solid #1e2a3d; border-radius: 10px;
  padding: 14px 18px; margin: 8px 0;
  animation: fadeRight 0.55s ease both;
  transition: border-color .2s, transform .2s, box-shadow .2s;
}
.rec-card:hover {
  border-color: #2a5aff44;
  transform: translateX(6px);
  box-shadow: 0 4px 18px rgba(77,159,255,0.08);
}
.rec-card:nth-child(1) { animation-delay: 0.10s; }
.rec-card:nth-child(2) { animation-delay: 0.20s; }
.rec-card:nth-child(3) { animation-delay: 0.30s; }
.rec-card:nth-child(4) { animation-delay: 0.40s; }
.rec-card:nth-child(5) { animation-delay: 0.50s; }
.rec-card:nth-child(6) { animation-delay: 0.60s; }
.rec-card:nth-child(7) { animation-delay: 0.70s; }
.rec-card:nth-child(8) { animation-delay: 0.80s; }
.rec-card .rec-title   { color: #4d9fff; font-weight: 600; font-size: 0.92rem; margin-bottom: 6px; }
.rec-card .rec-body    { color: #8a95a8; font-size: 0.85rem; line-height: 1.55; }

/* ── Upload zone ── */
[data-testid="stFileUploader"] > div {
  background: #0f1420 !important; border: 2px dashed #1e2a3d !important;
  border-radius: 12px !important;
  animation: fadeRight 0.6s ease both;
  animation-delay: 0.3s;
}
[data-testid="stFileUploader"] button {
  background: #1a3a6e !important; color: #4d9fff !important;
  border: 1px solid #2a5aaa !important; border-radius: 8px !important;
}

/* ── Dataframes ── */
.stDataFrame {
  border-radius: 10px; border: 1px solid #1e2a3d;
  animation: fadeRight 0.6s ease both;
  animation-delay: 0.2s;
}

/* ── Plotly chart wrappers — fade+slide from left ── */
.stPlotlyChart {
  animation: fadeRight 0.70s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: 0.18s;
  border-radius: 12px;
  overflow: hidden;
}

/* Stagger multiple charts in the same view */
.stPlotlyChart:nth-of-type(1) { animation-delay: 0.18s; }
.stPlotlyChart:nth-of-type(2) { animation-delay: 0.32s; }
.stPlotlyChart:nth-of-type(3) { animation-delay: 0.46s; }
.stPlotlyChart:nth-of-type(4) { animation-delay: 0.60s; }
.stPlotlyChart:nth-of-type(5) { animation-delay: 0.74s; }
.stPlotlyChart:nth-of-type(6) { animation-delay: 0.88s; }

/* ── Columns ── */
[data-testid="column"] {
  animation: fadeRight 0.60s ease both;
}
[data-testid="column"]:nth-child(1) { animation-delay: 0.10s; }
[data-testid="column"]:nth-child(2) { animation-delay: 0.22s; }
[data-testid="column"]:nth-child(3) { animation-delay: 0.34s; }
[data-testid="column"]:nth-child(4) { animation-delay: 0.46s; }
[data-testid="column"]:nth-child(5) { animation-delay: 0.58s; }
[data-testid="column"]:nth-child(6) { animation-delay: 0.70s; }

/* ── Info / success / warning banners ── */
.stAlert {
  animation: fadeRight 0.55s ease both;
  animation-delay: 0.2s;
}

/* ── Select boxes & widgets ── */
.stSelectbox, .stMultiSelect, .stCheckbox, .stDownloadButton {
  animation: fadeRight 0.50s ease both;
  animation-delay: 0.15s;
}

/* ── Progress bar label ── */
.prog-label { font-size: 0.8rem; color: #6a7898; margin-bottom: 4px; }

/* ── Divider ── */
.divider { border: none; border-top: 1px solid #1e2433; margin: 20px 0; }

/* ── Quality badge ── */
.qbadge {
  display: inline-block; border-radius: 6px; padding: 2px 9px;
  font-size: 0.72rem; font-weight: 600; letter-spacing: .04em;
  animation: fadeIn 0.5s ease both;
}
.qbadge.ok   { background: #0a2e15; color: #3fb950; border: 1px solid #1a5c2e; }
.qbadge.warn { background: #2e1a00; color: #f0a500; border: 1px solid #8b5000; }
.qbadge.bad  { background: #2e0a0a; color: #f85149; border: 1px solid #7a1a1a; }

/* ── Tab panel content entrance ── */
[data-baseweb="tab-panel"] {
  animation: fadeRight 0.60s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: 0.05s;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY THEME
# ══════════════════════════════════════════════════════════════════════════════
DARK = dict(
    plot_bgcolor="#0f1420", paper_bgcolor="#0f1420",
    font=dict(family="Inter", color="#b0b8cc", size=12),
    xaxis=dict(gridcolor="#1a2236", linecolor="#1e2a3d", zeroline=False,
               tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#1a2236", linecolor="#1e2a3d", zeroline=False,
               tickfont=dict(size=11)),
    legend=dict(bgcolor="#0b1018", bordercolor="#1e2a3d", borderwidth=1,
                font=dict(size=11)),
    margin=dict(l=46, r=26, t=48, b=40),
    hoverlabel=dict(bgcolor="#141b28", bordercolor="#2a3a55",
                    font=dict(color="#e8edf7", size=12)),
)
SEQ       = ["#4d9fff", "#f87171", "#34d399", "#a78bfa", "#fbbf24", "#38bdf8", "#fb923c"]
CHURN_MAP = {"Churned": "#f87171", "Retained": "#34d399"}

# ── Plotly built-in transition applied to every figure ──────────────────────
PLOTLY_TRANSITION = dict(duration=600, easing="cubic-in-out")


# ══════════════════════════════════════════════════════════════════════════════
# FILE LOADERS
# ══════════════════════════════════════════════════════════════════════════════
def load_csv(file) -> pd.DataFrame:
    for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
        try:
            file.seek(0)
            return pd.read_csv(file, encoding=enc)
        except Exception:
            pass
    return pd.DataFrame()


def load_excel(file) -> pd.DataFrame:
    try:
        return pd.read_excel(file, engine="openpyxl")
    except Exception:
        try:
            return pd.read_excel(file, engine="xlrd")
        except Exception as e:
            st.error(f"Excel error: {e}")
    return pd.DataFrame()


def load_pdf(file) -> pd.DataFrame:
    try:
        import pdfplumber
        file.seek(0)
        raw = file.read()
        rows, header = [], None
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            for page in pdf.pages:
                for tbl in (page.extract_tables() or []):
                    if not tbl:
                        continue
                    clean = [[str(c).strip() if c else "" for c in r] for r in tbl]
                    if header is None:
                        header = clean[0]; rows.extend(clean[1:])
                    else:
                        rows.extend(clean)
        if header and rows:
            df = pd.DataFrame(rows, columns=header)
            df.replace("", np.nan, inplace=True)
            return df
    except Exception as e:
        st.error(f"PDF parse error: {e}")
    return pd.DataFrame()


def auto_cast(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype == object:
            num = pd.to_numeric(df[col], errors="coerce")
            if num.notna().sum() / len(df) > 0.7:
                df[col] = num; continue
            try:
                dt = pd.to_datetime(df[col], errors="coerce")
                if dt.notna().sum() / len(df) > 0.7:
                    df[col] = dt; continue
            except Exception:
                pass
    return df


# ══════════════════════════════════════════════════════════════════════════════
# COLUMN DETECTORS
# ══════════════════════════════════════════════════════════════════════════════
def detect_churn(df):
    for c in df.columns:
        if re.search(r'churn', c, re.I): return c
    for c in df.columns:
        uv = set(df[c].dropna().astype(str).str.lower().unique())
        if uv.issubset({"0","1","yes","no","true","false","y","n"}): return c
    return df.columns[-1]

def detect_tenure(df):
    for c in df.columns:
        if re.search(r'tenure|month|duration|age|lifetime', c, re.I) and pd.api.types.is_numeric_dtype(df[c]):
            return c
    return None

def detect_signup(df):
    for c in df.columns:
        if re.search(r'signup|join|cohort|start|date', c, re.I): return c
    return None

def detect_id(df):
    for c in df.columns:
        if re.search(r'\bid\b|customerid|custid|userid', c, re.I): return c
    return None

def to_binary(s: pd.Series) -> pd.Series:
    m = {"yes":1,"no":0,"true":1,"false":0,"1":1,"0":0,"y":1,"n":0,
         True:1,False:0,1:1,0:0}
    return s.astype(str).str.strip().str.lower().map(m).fillna(0).astype(int)


# ══════════════════════════════════════════════════════════════════════════════
# SAMPLE DATA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def sample_data(n=1500):
    rng      = np.random.default_rng(42)
    tenure   = rng.integers(1, 73, n)
    charges  = np.round(rng.uniform(18, 130, n), 2)
    contract = rng.choice(["Month-to-month","One year","Two year"], n, p=[0.55,0.25,0.20])
    internet = rng.choice(["DSL","Fiber optic","No"], n, p=[0.35,0.44,0.21])
    gender   = rng.choice(["Male","Female"], n)
    senior   = rng.choice([0,1], n, p=[0.84,0.16])
    support  = rng.choice(["Yes","No"], n, p=[0.45,0.55])
    region   = rng.choice(["North","South","East","West"], n)
    base = (0.38 - 0.005*tenure + 0.0015*charges
            + 0.22*(contract=="Month-to-month") - 0.12*(contract=="Two year")
            + 0.06*senior - 0.08*(support=="Yes") + rng.normal(0,0.05,n))
    churn  = (np.clip(base,0,1) > 0.35).astype(int)
    months = pd.date_range("2021-01-01", periods=n, freq="7h")
    signup = [d.strftime("%Y-%m") for d in months]
    return pd.DataFrame({
        "CustomerID":     [f"C{i:05d}" for i in range(n)],
        "Gender":         gender, "SeniorCitizen": senior,
        "TechSupport":    support, "Region": region,
        "tenure":         tenure, "Contract": contract,
        "InternetService":internet, "MonthlyCharges": charges,
        "TotalCharges":   np.round(tenure*charges*rng.uniform(0.88,1.0,n),2),
        "SignupMonth":    signup, "Churn": churn,
    })


# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fig_apply(fig, title="", height=380):
    """Apply dark theme + Plotly built-in entrance transition."""
    cfg = dict(**DARK, height=height)
    if title:
        cfg["title"] = dict(
            text=title,
            font=dict(color="#e8edf7", size=14, family="Inter"),
            x=0.02, xanchor="left"
        )
    # Plotly native transition — animates axis rescaling & bar/line updates
    cfg["transition"] = PLOTLY_TRANSITION
    fig.update_layout(**cfg)
    return fig


def churn_donut(df, cc):
    vals   = df[cc].value_counts()
    labels = [("Churned" if v==1 else "Retained") for v in vals.index]
    colors = [CHURN_MAP[l] for l in labels]
    fig = go.Figure(go.Pie(
        labels=labels, values=vals.values,
        hole=0.62, marker_colors=colors,
        textinfo="percent+label", textfont_size=12,
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
    ))
    fig_apply(fig, "Churn Distribution", height=320)
    fig.update_layout(showlegend=True)
    return fig


def tenure_violin(df, tc, cc):
    df2 = df.copy()
    df2["Status"] = df2[cc].map({1:"Churned",0:"Retained"})
    fig = go.Figure()
    for s, col in CHURN_MAP.items():
        sub = df2[df2["Status"]==s][tc].dropna()
        h = col.lstrip("#")
        r2,g2,b2 = int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
        fill_rgba = f"rgba({r2},{g2},{b2},0.25)"
        fig.add_trace(go.Violin(
            y=sub, name=s, fillcolor=fill_rgba,
            line_color=col, box_visible=True, meanline_visible=True,
            points="outliers", pointpos=0,
            hovertemplate=f"<b>{s}</b><br>Value: %{{y}}<extra></extra>"
        ))
    return fig_apply(fig, "Tenure Distribution – Churned vs Retained")


def charge_box(df, cc):
    charge_col = next(
        (c for c in df.columns if re.search(r'monthly|charge|revenue|price',c,re.I)
         and pd.api.types.is_numeric_dtype(df[c])), None)
    if not charge_col: return None, None
    df2 = df.copy()
    df2["Status"] = df2[cc].map({1:"Churned",0:"Retained"})
    fig = go.Figure()
    for s,col in CHURN_MAP.items():
        sub = df2[df2["Status"]==s][charge_col].dropna()
        fig.add_trace(go.Box(
            y=sub, name=s, marker_color=col,
            boxpoints="outliers", notched=True,
            hovertemplate=f"<b>{s}</b><br>%{{y:.2f}}<extra></extra>"
        ))
    return fig_apply(fig, f"{charge_col} – Churned vs Retained"), charge_col


def cohort_line(df, sc, cc, tc):
    d   = df[[sc,cc]].dropna().copy()
    grp = d.groupby(sc).agg(Customers=(cc,"count"),Churned=(cc,"sum")).reset_index()
    grp["Retention"] = ((grp["Customers"]-grp["Churned"])/grp["Customers"]*100).round(2)
    grp["ChurnRate"] = (grp["Churned"]/grp["Customers"]*100).round(2)
    grp = grp.sort_values(sc)
    avg = grp["Retention"].mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=grp[sc], y=grp["Retention"],
        mode="lines+markers", name="Retention %",
        line=dict(color="#4d9fff",width=2.5),
        marker=dict(size=7,color="#4d9fff"),
        fill="tozeroy", fillcolor="rgba(77,159,255,0.08)",
        hovertemplate="<b>%{x}</b><br>Retention: %{y:.1f}%<extra></extra>"
    ))
    fig.add_hline(y=avg, line_dash="dot", line_color="#fbbf24",
                  annotation_text=f"Avg {avg:.1f}%",
                  annotation_font_color="#fbbf24", annotation_position="right")
    fig_apply(fig, "Monthly Cohort Retention (%)", height=360)
    fig.update_layout(xaxis_title="Signup Month", yaxis=dict(range=[0,105],title="Retention (%)"))
    return fig, grp


def survival(df, tc, cc):
    d = df[[tc,cc]].dropna().copy()
    d[tc] = pd.to_numeric(d[tc], errors="coerce")
    d = d.dropna(); d[tc] = d[tc].astype(int)
    total = len(d); mx = int(d[tc].max())
    tl,sv,ci_lo,ci_hi = [],[],[],[]
    for t in range(1, mx+1):
        alive = ((d[tc]>=t)|(d[cc]==0)).sum()
        p  = alive/total
        se = np.sqrt(p*(1-p)/total) if total else 0
        tl.append(t); sv.append(round(p*100,2))
        ci_lo.append(max(0,round((p-1.96*se)*100,2)))
        ci_hi.append(min(100,round((p+1.96*se)*100,2)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tl+tl[::-1], y=ci_hi+ci_lo[::-1],
        fill="toself", fillcolor="rgba(77,159,255,0.09)", line_color="rgba(0,0,0,0)",
        name="95% CI", hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=tl, y=sv, mode="lines", name="Survival %",
        line=dict(color="#4d9fff",width=2.5),
        hovertemplate="Month %{x}<br>Survival: %{y:.1f}%<extra></extra>"
    ))
    fig_apply(fig, "Customer Survival Curve (Kaplan-Meier style)", 380)
    fig.update_layout(xaxis_title="Months Since Signup",
                      yaxis_title="% Still Active", yaxis=dict(range=[0,105]))
    return fig


def bar_cat(df, cc, cat):
    g = df.groupby(cat)[cc].agg(["sum","count"]).reset_index()
    g.columns = [cat,"Churned","Total"]
    g["ChurnRate"]  = (g["Churned"]/g["Total"]*100).round(2)
    g["RetainRate"] = 100-g["ChurnRate"]
    g = g.sort_values("ChurnRate", ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Churned %",  x=g[cat], y=g["ChurnRate"],  marker_color="#f87171",
                         hovertemplate=f"<b>%{{x}}</b><br>Churn: %{{y:.1f}}%<extra></extra>"))
    fig.add_trace(go.Bar(name="Retained %", x=g[cat], y=g["RetainRate"], marker_color="#34d399",
                         hovertemplate=f"<b>%{{x}}</b><br>Retained: %{{y:.1f}}%<extra></extra>"))
    fig.update_layout(barmode="stack")
    fig_apply(fig, f"Churn vs Retention Rate by {cat}", 360)
    return fig, g


def correlation_bar(df, cc):
    num = df.select_dtypes(include=np.number)
    num = num[[c for c in num.columns if c!=cc and num[c].nunique()>2]]
    if num.empty: return None
    corr = num.corrwith(df[cc]).abs().sort_values()
    fig  = go.Figure(go.Bar(
        x=corr.values, y=corr.index, orientation="h",
        marker=dict(color=corr.values, colorscale="Blues",
                    line=dict(color="#1e2a3d",width=0.5)),
        hovertemplate="<b>%{y}</b><br>|Correlation|: %{x:.3f}<extra></extra>"
    ))
    fig_apply(fig, "Feature Correlation with Churn (|Pearson r|)", 380)
    fig.update_layout(xaxis_title="Absolute Correlation", yaxis_title="")
    return fig


def heatmap(df):
    num = df.select_dtypes(include=np.number)
    if len(num.columns)<2: return None
    corr = num.corr().round(3)
    fig  = px.imshow(corr, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                     text_auto=".2f", aspect="auto")
    fig_apply(fig, "Numeric Correlation Heatmap", max(340,len(corr)*38))
    fig.update_coloraxes(colorbar=dict(tickfont=dict(color="#b0b8cc")))
    return fig


def scatter_tenure_charge(df, tc, cc):
    charge_col = next(
        (c for c in df.columns if re.search(r'monthly|charge',c,re.I)
         and pd.api.types.is_numeric_dtype(df[c])), None)
    if not charge_col or not tc: return None
    df2 = df.copy()
    df2["Status"] = df2[cc].map({1:"Churned",0:"Retained"})
    sample_df = df2.sample(min(800,len(df2)), random_state=1)
    try:
        import statsmodels  # noqa
        fig = px.scatter(sample_df, x=tc, y=charge_col, color="Status",
                         color_discrete_map=CHURN_MAP, opacity=0.65,
                         hover_data=[tc,charge_col],
                         trendline="ols", trendline_scope="overall",
                         trendline_color_override="#fbbf24")
    except ImportError:
        fig = px.scatter(sample_df, x=tc, y=charge_col, color="Status",
                         color_discrete_map=CHURN_MAP, opacity=0.65,
                         hover_data=[tc,charge_col])
    fig_apply(fig, f"Tenure vs {charge_col} coloured by Churn", 400)
    return fig


def clv_analysis(df, tc, cc):
    charge_col = next(
        (c for c in df.columns if re.search(r'monthly|charge',c,re.I)
         and pd.api.types.is_numeric_dtype(df[c])), None)
    if not charge_col or not tc: return None, None
    df2 = df.copy()
    df2["CLV"]    = df2[tc]*df2[charge_col]
    df2["Status"] = df2[cc].map({1:"Churned",0:"Retained"})
    fig = px.histogram(df2, x="CLV", color="Status",
                       color_discrete_map=CHURN_MAP, barmode="overlay",
                       nbins=40, opacity=0.72,
                       labels={"CLV":"Customer Lifetime Value ($)"})
    fig_apply(fig, "Customer Lifetime Value (CLV) Distribution", 380)
    summary = df2.groupby("Status")["CLV"].agg(["mean","median","std"]).round(2)
    return fig, summary


def monthly_churn_trend(df, sc, cc):
    d = df[[sc,cc]].dropna().copy()
    g = d.groupby(sc)[cc].agg(["mean","count"]).reset_index()
    g.columns = [sc,"ChurnRate","Customers"]
    g["ChurnRate"] = (g["ChurnRate"]*100).round(2)
    g = g.sort_values(sc)
    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Bar(
        x=g[sc], y=g["Customers"], name="Customers",
        marker_color="rgba(77,159,255,0.13)",
        marker_line_color="#4d9fff", marker_line_width=1,
        hovertemplate="<b>%{x}</b><br>Customers: %{y:,}<extra></extra>"
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=g[sc], y=g["ChurnRate"], name="Churn Rate %",
        mode="lines+markers", line=dict(color="#f87171",width=2.5),
        marker=dict(size=7),
        hovertemplate="<b>%{x}</b><br>Churn Rate: %{y:.1f}%<extra></extra>"
    ), secondary_y=False)
    _cfg = dict(**DARK)
    _cfg["height"]     = 360
    _cfg["title"]      = dict(text="Monthly Churn Rate Trend",
                               font=dict(color="#e8edf7",size=14,family="Inter"), x=0.02)
    _cfg["transition"] = PLOTLY_TRANSITION
    fig.update_layout(**_cfg)
    fig.update_yaxes(title_text="Churn Rate (%)", secondary_y=False,
                     gridcolor="#1a2236", tickfont=dict(size=11))
    fig.update_yaxes(title_text="No. of Customers", secondary_y=True,
                     showgrid=False, tickfont=dict(size=11))
    return fig


# ── Smart insights ─────────────────────────────────────────────────────────────
def make_insights(df, cc, cr, tc, signup_col=None):
    ins = []
    benchmark = 20.0
    if cr > benchmark:
        ins.append(("bad","🔴",
            f"Churn rate is <b>{cr:.2f}%</b> — <b>{cr-benchmark:.1f}pp above</b> the 20% SaaS benchmark. Urgent retention action required."))
    elif cr > 10:
        ins.append(("warn","🟡",
            f"Churn rate is <b>{cr:.2f}%</b> — moderate. Industry best-in-class is &lt;10%."))
    else:
        ins.append(("good","🟢",
            f"Churn rate is <b>{cr:.2f}%</b> — healthy, within best-in-class range (&lt;10%)."))
    if tc:
        avg_c = df[df[cc]==1][tc].mean(); avg_r = df[df[cc]==0][tc].mean()
        diff  = avg_r - avg_c
        ins.append(("warn" if diff>5 else "","📅",
            f"Churned customers leave at avg <b>{avg_c:.1f} mo</b>; retained avg <b>{avg_r:.1f} mo</b>. "
            f"The <b>{diff:.1f}-month gap</b> is a critical intervention window."))
        early       = (df[tc]<=3).sum()
        early_churn = df[(df[tc]<=3)&(df[cc]==1)].shape[0]
        if early > 0:
            ep = early_churn/early*100
            ins.append(("bad" if ep>40 else "warn","⚡",
                f"<b>{ep:.1f}%</b> of customers who signed up in the first 3 months churned — "
                "high early churn suggests onboarding issues."))
    charge_col = next(
        (c for c in df.columns if re.search(r'monthly|charge',c,re.I)
         and pd.api.types.is_numeric_dtype(df[c])), None)
    if charge_col:
        ac = df[df[cc]==1][charge_col].mean(); ar = df[df[cc]==0][charge_col].mean()
        if ac > ar:
            ins.append(("warn","💵",
                f"Churned customers pay <b>${ac:.2f}/mo</b> vs <b>${ar:.2f}/mo</b> for retained — "
                "higher charges correlate with churn; consider value-based pricing."))
    id_col  = detect_id(df)
    exclude = {cc}
    if id_col:    exclude.add(id_col)
    if signup_col: exclude.add(signup_col)
    cats = [c for c in df.select_dtypes("object").columns
            if c not in exclude and df[c].nunique()<=20]
    for cat in cats[:4]:
        g = df.groupby(cat)[cc].mean()
        worst = g.idxmax(); best = g.idxmin()
        ins.append(("","𖥔",
            f"<b>{cat}</b>: highest churn in <b>{worst}</b> ({g[worst]*100:.1f}%), "
            f"lowest in <b>{best}</b> ({g[best]*100:.1f}%)."))
    return ins


RECS = [
    (' ✦ ',"Early-Life Intervention",
     "60–70% of churn happens in the first 90 days. Build an automated 'day 3 / day 14 / day 30' onboarding email journey addressing common drop-off points."),
    ("✦","Contract Upsell Campaign",
     "Month-to-month customers churn 2–3× more than annual subscribers. Offer a 15–20% discount for upgrading to annual plans — model shows ROI positive within 2 months."),
    ("✦","Dynamic Pricing Audit",
     "High-charge customers are over-represented in churn. Introduce mid-tier bundles or loyalty discounts at the 6-month and 12-month tenure milestones."),
    ("✦","Weekly Churn-Risk Scoring",
     "Train a logistic regression or gradient-boosting model on tenure, charges, and contract type. Flag top 10% risk customers weekly for proactive outreach."),
    ("✦","Exit-Survey Programme",
     "Capture churn reasons via a 3-question exit survey. Qualitative data fills analytical blind spots and surfaces product/UX issues invisible in quantitative data."),
    ("✦","Loyalty Rewards Programme",
     "Introduce perks at 3, 6, 12, and 24-month tenure milestones. Even small rewards (free month, feature unlock) measurably reduce voluntary churn."),
    ("✦","Re-engagement Automation",
     "Build a 'win-back' sequence targeting lapsed customers within 30 days of churn. Personalise with last-used feature + limited-time offer."),
    ("✦","Monthly Retention Reviews",
     "Institute a monthly retention KPI review shared across product, marketing, and CX teams. Assign a churn-rate owner and set quarterly reduction targets."),
]


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="font-size:1.5rem;font-weight:bold;">✧ Churn Analyser</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.75rem;color:#4d9fff;letter-spacing:.05em;margin-bottom:12px;">'
        'Analyse customer churn patterns and identify opportunities for retention.'
        '</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.9rem;color:#3fb950;padding:2px 0;font-weight:bold;">'
        '<img src="https://cdn-icons-png.flaticon.com/128/15424/15424097.png" '
        'style="width:16px;height:16px;margin-right:10px;"> Upload Dataset</div><br>',
        unsafe_allow_html=True)
    uploaded   = st.file_uploader("CSV · Excel · PDF", type=["csv","xlsx","xls","pdf"],
                                   help="Upload any customer / subscription dataset")
    use_sample = st.checkbox("Use built-in sample data", value=(uploaded is None))
    st.markdown("---")
    churn_sel = tenure_sel = signup_sel = None
    st.markdown("### Key Features")
    for item in ["Churn rate & retention trends","Cohort analysis","Survival curve",
                 "CLV analysis","Segment drill-down","Feature correlations","Actionable insights"]:
        st.markdown(f'<div style="font-size:0.8rem;color:#3fb950;padding:2px 0;">✦ {item}</div>',
                    unsafe_allow_html=True)
    st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════
df_raw = pd.DataFrame()
if uploaded:
    n = uploaded.name.lower()
    with st.spinner("Parsing file…"):
        if n.endswith(".csv"):              df_raw = load_csv(uploaded)
        elif n.endswith((".xlsx",".xls")): df_raw = load_excel(uploaded)
        elif n.endswith(".pdf"):           df_raw = load_pdf(uploaded)
    if df_raw.empty:
        st.warning("Could not extract data from file — falling back to sample dataset.")
        df_raw = sample_data()
    else:
        st.success(f"✅ Loaded **{len(df_raw):,} rows × {len(df_raw.columns)} columns** from `{uploaded.name}`")
elif use_sample:
    df_raw = sample_data()
else:
    st.warning("Upload a dataset or enable sample data in the sidebar.")
    st.stop()

df = auto_cast(df_raw.copy())


# ── Sidebar column pickers ─────────────────────────────────────────────────────
with st.sidebar:
    all_cols = df.columns.tolist()
    g_churn  = detect_churn(df)
    churn_sel = st.selectbox("Churn column", all_cols,
                              index=all_cols.index(g_churn) if g_churn in all_cols else 0)
    df[churn_sel] = to_binary(df[churn_sel])
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    g_tenure = detect_tenure(df)
    tenure_options = ["(none)"]+num_cols
    t_def = num_cols.index(g_tenure)+1 if g_tenure and g_tenure in num_cols else 0
    tenure_sel = st.selectbox("Tenure column", tenure_options, index=t_def)
    tenure_sel = None if tenure_sel=="(none)" else tenure_sel
    g_signup = detect_signup(df)
    signup_options = ["(none)"]+all_cols
    s_def = all_cols.index(g_signup)+1 if g_signup and g_signup in all_cols else 0
    signup_sel = st.selectbox("Signup / cohort column", signup_options, index=s_def)
    signup_sel = None if signup_sel=="(none)" else signup_sel
    _id_col      = detect_id(df)
    _exclude_cats = {churn_sel}
    if signup_sel: _exclude_cats.add(signup_sel)
    if _id_col:    _exclude_cats.add(_id_col)
    cat_opts = [c for c in df.select_dtypes("object").columns
                if df[c].nunique()<=25 and c not in _exclude_cats]


# ══════════════════════════════════════════════════════════════════════════════
# DERIVED GLOBALS
# ══════════════════════════════════════════════════════════════════════════════
total      = len(df)
churned    = int(df[churn_sel].sum())
retained   = total - churned
cr         = churned/total*100
charge_col = next(
    (c for c in df.columns if re.search(r'monthly|charge',c,re.I)
     and pd.api.types.is_numeric_dtype(df[c])), None)


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="badge">DATA SCIENCE INTELLIGENCE</div>
  <h1> CUSTOMER RETENTION &amp; CHURN ANALYSIS</h1>
  <p>Predictive churn modeling executes binary classification algorithms on multi-dimensional telemetry<br>
     feature vectors—synthesizing RFM metrics, event-stream logs, and support-ticket latency—to isolate anomalous behavioral vectors.</p>
</div>
""", unsafe_allow_html=True)

# ── Quick KPIs ─────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.metric("Total Customers", f"{total:,}")
k2.metric("Churned",  f"{churned:,}",  f"-{cr:.1f}%",       delta_color="inverse")
k3.metric("Retained", f"{retained:,}", f"+{100-cr:.1f}%")
k4.metric("Churn Rate", f"{cr:.2f}%")
if tenure_sel:
    k5.metric("Avg Tenure", f"{df[tenure_sel].mean():.1f} mo")
    churn_t  = df[df[churn_sel]==1][tenure_sel].mean()
    retain_t = df[df[churn_sel]==0][tenure_sel].mean()
    k6.metric("Churn vs Retain Tenure", f"{churn_t:.1f} vs {retain_t:.1f} mo")
elif charge_col:
    k5.metric("Avg Monthly Charge", f"${df[charge_col].mean():.2f}")
    k6.metric("Churn Avg Charge",   f"${df[df[churn_sel]==1][charge_col].mean():.2f}")


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
TABS = st.tabs([
    " Overview", " Cohort & Survival", " CLV Analysis",
    " Segment Drill-Down", " Correlations", " Insights & Recs", " Data Quality",
])


# ─────────── TAB 0 – OVERVIEW ──────────────────────────────────────────────────
with TABS[0]:
    c1,c2 = st.columns(2)
    with c1:
        st.plotly_chart(churn_donut(df, churn_sel), use_container_width=True)
    with c2:
        if tenure_sel:
            st.plotly_chart(tenure_violin(df, tenure_sel, churn_sel), use_container_width=True)
        else:
            st.info("Select a **Tenure** column in the sidebar to see the tenure violin chart.")
    if charge_col:
        b_fig,_ = charge_box(df, churn_sel)
        if b_fig: st.plotly_chart(b_fig, use_container_width=True)
    if tenure_sel and charge_col:
        sc_fig = scatter_tenure_charge(df, tenure_sel, churn_sel)
        if sc_fig: st.plotly_chart(sc_fig, use_container_width=True)


# ─────────── TAB 1 – COHORT & SURVIVAL ────────────────────────────────────────
with TABS[1]:
    if signup_sel and tenure_sel:
        st.markdown('<div class="sec-hdr">Monthly Cohort Retention</div>', unsafe_allow_html=True)
        cf, cohort_df = cohort_line(df, signup_sel, churn_sel, tenure_sel)
        st.plotly_chart(cf, use_container_width=True)
        col_a,col_b = st.columns([3,2])
        with col_a:
            st.markdown('<div class="sec-hdr">Churn Rate Trend</div>', unsafe_allow_html=True)
            st.plotly_chart(monthly_churn_trend(df, signup_sel, churn_sel), use_container_width=True)
        with col_b:
            st.markdown('<div class="sec-hdr">Cohort Summary Table</div>', unsafe_allow_html=True)
            show = cohort_df.copy()
            show.columns = ["Signup Month","Customers","Churned","Retention %","Churn Rate %"]
            st.dataframe(
                show.style
                    .background_gradient(subset=["Retention %"], cmap="RdYlGn")
                    .format({"Retention %":"{:.1f}","Churn Rate %":"{:.1f}"}),
                use_container_width=True, height=360)
        st.markdown('<div class="sec-hdr">Survival Curve</div>', unsafe_allow_html=True)
        st.plotly_chart(survival(df, tenure_sel, churn_sel), use_container_width=True)
        surv_data = []
        mx = int(df[tenure_sel].max()); total_s = len(df)
        for t in range(1, mx+1):
            alive = ((df[tenure_sel]>=t)|(df[churn_sel]==0)).sum()
            surv_data.append(alive/total_s*100)
        median_surv = next((i+1 for i,v in enumerate(surv_data) if v<=50), None)
        if median_surv:
            st.markdown(
                f'<div class="insight"><div class="icon">📌</div>'
                f'<div>Median customer survival: <b>{median_surv} months</b> — '
                f'50% of customers churn by month {median_surv}.</div></div>',
                unsafe_allow_html=True)
    else:
        st.info("Select both **Signup** and **Tenure** columns in the sidebar to unlock cohort analysis.")


# ─────────── TAB 2 – CLV ───────────────────────────────────────────────────────
with TABS[2]:
    if tenure_sel and charge_col:
        st.markdown('<div class="sec-hdr">Customer Lifetime Value Analysis</div>', unsafe_allow_html=True)
        clv_fig, clv_sum = clv_analysis(df, tenure_sel, churn_sel)
        if clv_fig is not None:
            st.plotly_chart(clv_fig, use_container_width=True)
            st.markdown('<div class="sec-hdr">CLV Summary by Status</div>', unsafe_allow_html=True)
            st.dataframe(
                clv_sum.rename(columns={"mean":"Mean CLV ($)","median":"Median CLV ($)","std":"Std Dev ($)"}),
                use_container_width=True)
            churn_clv  = clv_sum.loc["Churned","mean"]  if "Churned"  in clv_sum.index else 0
            retain_clv = clv_sum.loc["Retained","mean"] if "Retained" in clv_sum.index else 0
            lost = churn_clv * churned
            if churn_clv>0 and retain_clv>0:
                st.markdown(
                    f'<div class="insight bad"><div class="icon">💸</div>'
                    f'<div>Estimated revenue lost to churn: <b>${lost:,.0f}</b> '
                    f'(avg churned CLV ${churn_clv:,.0f} × {churned:,} churned customers). '
                    f'Retained customers generate <b>{retain_clv/churn_clv:.1f}× more lifetime value</b>.</div></div>',
                    unsafe_allow_html=True)
        if cat_opts:
            st.markdown('<div class="sec-hdr">CLV by Segment</div>', unsafe_allow_html=True)
            seg    = st.selectbox("Segment", cat_opts, key="clv_seg")
            df_clv = df.copy()
            df_clv["_CLV"] = df_clv[tenure_sel]*df_clv[charge_col]
            g = df_clv.groupby(seg)["_CLV"].agg(["mean","median","count"]).round(2).reset_index()
            g.columns = [seg,"Mean CLV","Median CLV","Customers"]
            fig_clv_seg = px.bar(g, x=seg, y="Mean CLV", color="Mean CLV",
                                  color_continuous_scale="Blues", text="Mean CLV",
                                  labels={"Mean CLV":"Mean CLV ($)"})
            fig_clv_seg.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig_apply(fig_clv_seg, f"Mean CLV by {seg}")
            fig_clv_seg.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_clv_seg, use_container_width=True)
    else:
        st.info("Select **Tenure** and ensure a **Monthly Charges** column exists to unlock CLV analysis.")


# ─────────── TAB 3 – SEGMENTS ──────────────────────────────────────────────────
with TABS[3]:
    if cat_opts:
        sel = st.multiselect("Select columns to analyse", cat_opts,
                              default=cat_opts[:min(3,len(cat_opts))])
        for cat in sel:
            bfig, gtbl = bar_cat(df, churn_sel, cat)
            ca,cb = st.columns([3,2])
            with ca:
                st.plotly_chart(bfig, use_container_width=True)
            with cb:
                st.markdown(f'<div class="sec-hdr">{cat} – Churn Table</div>', unsafe_allow_html=True)
                st.dataframe(
                    gtbl.style
                        .format({"ChurnRate":"{:.1f}%","RetainRate":"{:.1f}%"})
                        .background_gradient(subset=["ChurnRate"], cmap="Reds"),
                    use_container_width=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    else:
        st.info("No suitable categorical columns detected for segment analysis.")


# ─────────── TAB 4 – CORRELATIONS ─────────────────────────────────────────────
with TABS[4]:
    st.markdown('<div class="sec-hdr">Feature–Churn Correlations</div>', unsafe_allow_html=True)
    corr_fig = correlation_bar(df, churn_sel)
    if corr_fig: st.plotly_chart(corr_fig, use_container_width=True)
    else:        st.info("No numeric features available.")
    st.markdown('<div class="sec-hdr">Full Correlation Heatmap</div>', unsafe_allow_html=True)
    hm = heatmap(df)
    if hm: st.plotly_chart(hm, use_container_width=True)
    num2 = df.select_dtypes(include=np.number)
    num2 = num2[[c for c in num2.columns if c!=churn_sel and num2[c].nunique()>2]]
    if not num2.empty:
        corr_vals = num2.corrwith(df[churn_sel]).round(4)
        tbl = pd.DataFrame({
            "Feature":   corr_vals.index,
            "Pearson r": corr_vals.values,
            "|r|":       corr_vals.abs().values,
            "Direction": ["↑ Increases churn" if v>0 else "↓ Decreases churn" for v in corr_vals.values]
        }).sort_values("|r|", ascending=False)
        st.markdown('<div class="sec-hdr">Correlation Table</div>', unsafe_allow_html=True)
        st.dataframe(
            tbl.style
               .format({"Pearson r":"{:.4f}","|r|":"{:.4f}"})
               .background_gradient(subset=["|r|"], cmap="Blues"),
            use_container_width=True)


# ─────────── TAB 5 – INSIGHTS ─────────────────────────────────────────────────
with TABS[5]:
    st.markdown('<div class="sec-hdr">Auto-Generated Insights</div>', unsafe_allow_html=True)
    insights = make_insights(df, churn_sel, cr, tenure_sel, signup_col=signup_sel)
    for cls,icon,text in insights:
        st.markdown(
            f'<div class="insight {cls}"><div class="icon">{icon}</div><div>{text}</div></div>',
            unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">Strategic Recommendations</div>', unsafe_allow_html=True)
    for icon,title,body in RECS:
        st.markdown(f"""
        <div class="rec-card">
          <div class="rec-title">{icon} {title}</div>
          <div class="rec-body">{body}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">Export</div>', unsafe_allow_html=True)
    col_x,col_y = st.columns(2)
    txt  = "CUSTOMER RETENTION & CHURN ANALYSIS REPORT\n"+"="*52+"\n"
    txt += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    txt += "KEY METRICS\n"+"-"*30+"\n"
    txt += f"Total Customers : {total:,}\nChurned         : {churned:,}\nChurn Rate      : {cr:.2f}%\n\n"
    txt += "INSIGHTS\n"+"-"*30+"\n"
    for _,icon,text in insights:
        clean = re.sub(r'<.*?>','',text); txt += f"{icon} {clean}\n"
    txt += "\nRECOMMENDATIONS\n"+"-"*30+"\n"
    for icon,title,body in RECS:
        txt += f"\n{icon} {title}\n{body}\n"
    col_x.download_button("🡻 Download Report (.txt)",       txt,              "churn_report.txt",  "text/plain")
    col_y.download_button("🡻 Download Cleaned Data (.csv)", df.to_csv(index=False), "cleaned_data.csv","text/csv")
    if signup_sel and tenure_sel:
        _,cohort_ex = cohort_line(df, signup_sel, churn_sel, tenure_sel)
        cohort_ex.columns = ["Signup Month","Customers","Churned","Retention %","Churn Rate %"]
        st.download_button("🡻 Download Cohort Table (.csv)", cohort_ex.to_csv(index=False),
                           "cohort_table.csv","text/csv")


# ─────────── TAB 6 – DATA QUALITY ─────────────────────────────────────────────
with TABS[6]:
    st.markdown('<div class="sec-hdr">Dataset Overview</div>', unsafe_allow_html=True)
    qa1,qa2,qa3,qa4 = st.columns(4)
    qa1.metric("Rows",         f"{len(df):,}")
    qa2.metric("Columns",      len(df.columns))
    qa3.metric("Missing Vals", df.isnull().sum().sum())
    qa4.metric("Duplicates",   df.duplicated().sum())
    st.markdown('<div class="sec-hdr">Column-Level Quality Report</div>', unsafe_allow_html=True)
    records = []
    for c in df.columns:
        miss     = df[c].isnull().sum()
        miss_pct = miss/len(df)*100
        dtype    = str(df[c].dtype); uniq = df[c].nunique()
        badge    = "ok" if miss_pct<5 else "warn" if miss_pct<20 else "bad"
        label    = "✅ Good" if badge=="ok" else "⚠️ Moderate" if badge=="warn" else "❌ High Missing"
        records.append({"Column":c,"Type":dtype,"Unique":uniq,
                         "Missing":miss,"Missing %":round(miss_pct,1),"Quality":label})
    qdf = pd.DataFrame(records)
    def _row_style(row):
        q = str(row.get("Quality",""))
        bg = "background:#071209" if "✅" in q else "background:#130c00" if "⚠️" in q else "background:#130606"
        return [bg]*len(row)
    st.dataframe(qdf.style.apply(_row_style, axis=1), use_container_width=True)
    st.markdown('<div class="sec-hdr">Descriptive Statistics</div>', unsafe_allow_html=True)
    st.dataframe(df.describe(include="all").T.style.background_gradient(cmap="Blues"),
                 use_container_width=True)
    st.markdown('<div class="sec-hdr">Data Preview (first 500 rows)</div>', unsafe_allow_html=True)
    st.dataframe(df.head(500), use_container_width=True)