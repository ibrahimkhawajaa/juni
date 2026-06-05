import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import warnings
warnings.filterwarnings("ignore")

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataLens EDA Studio",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');

  html, body, [class*="css"] {
      font-family: 'DM Sans', sans-serif;
  }

  /* Dark background */
  .stApp {
      background-color: #0d0f14;
      color: #e8eaf0;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #13151e 0%, #0d0f14 100%);
      border-right: 1px solid #1e2130;
  }

  /* Header */
  .hero-header {
      background: linear-gradient(135deg, #1a1d2e 0%, #0f1118 100%);
      border: 1px solid #252840;
      border-radius: 16px;
      padding: 2rem 2.5rem;
      margin-bottom: 1.5rem;
      position: relative;
      overflow: hidden;
  }
  .hero-header::before {
      content: '';
      position: absolute;
      top: -50%;
      right: -10%;
      width: 300px;
      height: 300px;
      background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
      pointer-events: none;
  }
  .hero-title {
      font-family: 'Space Mono', monospace;
      font-size: 2.2rem;
      font-weight: 700;
      background: linear-gradient(135deg, #818cf8, #c084fc, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin: 0;
      line-height: 1.2;
  }
  .hero-sub {
      color: #6b7280;
      font-size: 0.95rem;
      margin-top: 0.5rem;
      font-weight: 300;
  }

  /* Metric cards */
  .metric-card {
      background: #13151e;
      border: 1px solid #1e2130;
      border-radius: 12px;
      padding: 1.2rem 1.5rem;
      text-align: center;
      transition: border-color 0.2s;
  }
  .metric-card:hover { border-color: #6366f1; }
  .metric-value {
      font-family: 'Space Mono', monospace;
      font-size: 1.8rem;
      font-weight: 700;
      color: #818cf8;
  }
  .metric-label {
      font-size: 0.78rem;
      color: #6b7280;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-top: 0.3rem;
  }

  /* Section headers */
  .section-title {
      font-family: 'Space Mono', monospace;
      font-size: 1rem;
      color: #818cf8;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      border-left: 3px solid #6366f1;
      padding-left: 0.75rem;
      margin: 1.5rem 0 1rem;
  }

  /* Dataframe styling */
  .stDataFrame { border-radius: 10px; overflow: hidden; }

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {
      gap: 0.5rem;
      background: #13151e;
      border-radius: 10px;
      padding: 0.3rem;
      border: 1px solid #1e2130;
  }
  .stTabs [data-baseweb="tab"] {
      border-radius: 8px;
      color: #6b7280;
      font-weight: 500;
      font-size: 0.85rem;
  }
  .stTabs [aria-selected="true"] {
      background: #6366f1 !important;
      color: white !important;
  }

  /* Selectbox, sliders */
  .stSelectbox > div > div, .stMultiSelect > div > div {
      background: #13151e;
      border-color: #1e2130;
      color: #e8eaf0;
  }

  /* Pill badges */
  .badge {
      display: inline-block;
      padding: 2px 10px;
      border-radius: 999px;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.04em;
  }
  .badge-num  { background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid #6366f140; }
  .badge-cat  { background: rgba(192,132,252,0.15); color: #c084fc; border: 1px solid #a855f740; }
  .badge-date { background: rgba(56,189,248,0.15);  color: #38bdf8; border: 1px solid #0ea5e940; }
  .badge-bool { background: rgba(52,211,153,0.15);  color: #34d399; border: 1px solid #10b98140; }

  /* Insight box */
  .insight-box {
      background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(192,132,252,0.06));
      border: 1px solid #252840;
      border-left: 3px solid #6366f1;
      border-radius: 10px;
      padding: 1rem 1.2rem;
      margin: 0.75rem 0;
      font-size: 0.88rem;
      color: #c7cad6;
  }

  /* Hide Streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: #0d0f14; }
  ::-webkit-scrollbar-thumb { background: #252840; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ───────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#9ca3af", size=12),
    xaxis=dict(gridcolor="#1e2130", linecolor="#252840", zerolinecolor="#252840"),
    yaxis=dict(gridcolor="#1e2130", linecolor="#252840", zerolinecolor="#252840"),
    margin=dict(l=20, r=20, t=40, b=20),
    colorway=["#818cf8","#c084fc","#38bdf8","#34d399","#fb923c","#f472b6","#facc15"],
    hoverlabel=dict(bgcolor="#13151e", bordercolor="#252840", font_color="#e8eaf0"),
)
COLOR_SEQ = px.colors.qualitative.Pastel

# ── Data loader ────────────────────────────────────────────────────────────────
@st.cache_data
def load_builtin(name):
    if name == "Titanic 🚢":
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        return pd.read_csv(url)
    elif name == "Iris 🌸":
        from sklearn.datasets import load_iris
        d = load_iris(as_frame=True)
        df = d.frame.copy()
        df["species"] = d.target_names[df["target"]]
        return df.drop("target", axis=1)
    elif name == "Tips 🍽️":
        return px.data.tips()
    elif name == "Gapminder 🌍":
        return px.data.gapminder().query("year == 2007").drop("year", axis=1)
    elif name == "Car Crashes 🚗":
        return sns.load_dataset("car_crashes")
    elif name == "Penguins 🐧":
        return sns.load_dataset("penguins")
    return None

@st.cache_data
def parse_upload(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    elif name.endswith((".xls", ".xlsx")):
        return pd.read_excel(file)
    elif name.endswith(".json"):
        return pd.read_json(file)
    elif name.endswith(".parquet"):
        return pd.read_parquet(file)
    return None

def dtype_badge(dtype):
    s = str(dtype)
    if "int" in s or "float" in s:
        return '<span class="badge badge-num">numeric</span>'
    elif "datetime" in s:
        return '<span class="badge badge-date">datetime</span>'
    elif "bool" in s:
        return '<span class="badge badge-bool">bool</span>'
    else:
        return '<span class="badge badge-cat">categorical</span>'

def apply_sort(df, sort_col, ascending):
    if sort_col and sort_col in df.columns:
        return df.sort_values(sort_col, ascending=ascending)
    return df

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:Space Mono,monospace;font-size:1.1rem;
                color:#818cf8;padding:0.5rem 0 1rem;letter-spacing:0.05em'>
      🔬 DATALENS
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Data Source**")
    data_source = st.radio("", ["Built-in Dataset", "Upload File"], label_visibility="collapsed")

    df = None
    dataset_name = ""

    if data_source == "Built-in Dataset":
        dataset_name = st.selectbox(
            "Choose dataset",
            ["Titanic 🚢", "Iris 🌸", "Tips 🍽️", "Gapminder 🌍",
             "Car Crashes 🚗", "Penguins 🐧"]
        )
        df = load_builtin(dataset_name)
    else:
        uploaded = st.file_uploader("Upload CSV / Excel / JSON / Parquet",
                                    type=["csv","xlsx","xls","json","parquet"])
        if uploaded:
            df = parse_upload(uploaded)
            dataset_name = uploaded.name

    st.divider()

    if df is not None:
        st.markdown("**Global Filters**")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        # Row limit
        row_limit = st.slider("Max rows to display", 10, min(5000, len(df)),
                              min(500, len(df)), step=10)

        # Numeric filter
        if num_cols:
            filter_num_col = st.selectbox("Filter by numeric column", ["None"] + num_cols)
            if filter_num_col != "None":
                mn = float(df[filter_num_col].min())
                mx = float(df[filter_num_col].max())
                rng = st.slider(f"{filter_num_col} range", mn, mx, (mn, mx))
                df = df[(df[filter_num_col] >= rng[0]) & (df[filter_num_col] <= rng[1])]

        # Categorical filter
        if cat_cols:
            filter_cat_col = st.selectbox("Filter by category column", ["None"] + cat_cols)
            if filter_cat_col != "None":
                opts = df[filter_cat_col].dropna().unique().tolist()
                sel = st.multiselect(f"{filter_cat_col} values", opts, default=opts)
                if sel:
                    df = df[df[filter_cat_col].isin(sel)]

        df = df.head(row_limit)

        st.divider()
        st.markdown("**Sorting**")
        sort_col = st.selectbox("Sort by column", ["None"] + df.columns.tolist())
        sort_dir = st.radio("Direction", ["Ascending ↑", "Descending ↓"],
                            horizontal=True)
        ascending = sort_dir == "Ascending ↑"
        if sort_col != "None":
            df = apply_sort(df, sort_col, ascending)

# ── Main content ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
  <p class="hero-title">DataLens EDA Studio</p>
  <p class="hero-sub">Exploratory Data Analysis · {dataset_name or 'No dataset loaded'}</p>
</div>
""", unsafe_allow_html=True)

if df is None:
    st.info("👈 Select a built-in dataset or upload your own file to get started.")
    st.stop()

# ── Key metrics ────────────────────────────────────────────────────────────────
num_cols  = df.select_dtypes(include=np.number).columns.tolist()
cat_cols  = df.select_dtypes(include="object").columns.tolist()
missing   = df.isnull().sum().sum()
miss_pct  = round(missing / df.size * 100, 1)
dup_rows  = df.duplicated().sum()

c1, c2, c3, c4, c5, c6 = st.columns(6)
metrics = [
    (len(df), "Rows"),
    (len(df.columns), "Columns"),
    (len(num_cols), "Numeric"),
    (len(cat_cols), "Categorical"),
    (f"{miss_pct}%", "Missing"),
    (dup_rows, "Duplicates"),
]
for col, (val, lbl) in zip([c1,c2,c3,c4,c5,c6], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-value">{val}</div>
          <div class="metric-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("")

# ── Tabs ───────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📋 Data Table",
    "📊 Overview",
    "🔢 Numerics",
    "🏷️ Categoricals",
    "🔗 Correlations",
    "🚨 Data Quality",
    "📈 Custom Plot",
])

# ─── Tab 0 — Data Table ────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown('<p class="section-title">Dataset Preview</p>', unsafe_allow_html=True)

    col_search, col_sort_t, col_dir_t = st.columns([3, 2, 1])
    with col_search:
        search = st.text_input("🔍 Search column name", "")
    with col_sort_t:
        tsort = st.selectbox("Sort by", ["None"] + df.columns.tolist(), key="tab_sort")
    with col_dir_t:
        tdir  = st.selectbox("Dir", ["↑ Asc", "↓ Desc"], key="tab_dir")

    show_df = df.copy()
    if search:
        matched = [c for c in show_df.columns if search.lower() in c.lower()]
        show_df = show_df[matched]
    if tsort != "None" and tsort in show_df.columns:
        show_df = show_df.sort_values(tsort, ascending=(tdir == "↑ Asc"))

    st.dataframe(show_df, use_container_width=True, height=420)

    # Column schema
    st.markdown('<p class="section-title">Column Schema</p>', unsafe_allow_html=True)
    schema_rows = []
    for col in df.columns:
        schema_rows.append({
            "Column": col,
            "Type": str(df[col].dtype),
            "Non-Null": df[col].count(),
            "Null": df[col].isnull().sum(),
            "Unique": df[col].nunique(),
            "Sample": str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "—",
        })
    schema_df = pd.DataFrame(schema_rows)
    st.dataframe(schema_df, use_container_width=True, height=300)

    # Download
    csv_bytes = df.to_csv(index=False).encode()
    st.download_button("⬇️ Download filtered CSV", csv_bytes,
                       "filtered_data.csv", "text/csv")

# ─── Tab 1 — Overview ─────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown('<p class="section-title">Statistical Summary</p>', unsafe_allow_html=True)

    sort_stat = st.selectbox("Sort summary by", ["None"] + df.describe().columns.tolist(), key="stat_sort")
    stat_dir  = st.radio("Order", ["Ascending ↑", "Descending ↓"], horizontal=True, key="stat_dir")

    desc = df.describe(include="all").T.reset_index().rename(columns={"index":"column"})
    if sort_stat != "None" and sort_stat in desc.columns:
        desc = desc.sort_values(sort_stat, ascending=(stat_dir == "Ascending ↑"))
    st.dataframe(desc, use_container_width=True, height=380)

    st.markdown('<p class="section-title">Shape of Numeric Distributions</p>', unsafe_allow_html=True)
    if num_cols:
        n = len(num_cols)
        cols_per_row = 3
        rows = (n + cols_per_row - 1) // cols_per_row
        fig = make_subplots(rows=rows, cols=cols_per_row,
                            subplot_titles=num_cols)
        for i, c in enumerate(num_cols):
            r, col_idx = divmod(i, cols_per_row)
            fig.add_trace(
                go.Histogram(x=df[c].dropna(), name=c,
                             marker_color="#818cf8", opacity=0.8,
                             showlegend=False),
                row=r+1, col=col_idx+1
            )
        fig.update_layout(**PLOTLY_LAYOUT, height=max(300, rows * 220))
        st.plotly_chart(fig, use_container_width=True)

# ─── Tab 2 — Numerics ─────────────────────────────────────────────────────────
with tabs[2]:
    if not num_cols:
        st.warning("No numeric columns found.")
    else:
        st.markdown('<p class="section-title">Numeric Column Explorer</p>',
                    unsafe_allow_html=True)

        c_left, c_right = st.columns(2)
        with c_left:
            sel_num = st.selectbox("Select column", num_cols, key="num_sel")
        with c_right:
            plot_type = st.selectbox("Chart type",
                                     ["Histogram", "Box Plot", "Violin",
                                      "ECDF", "Rug Plot"])

        series = df[sel_num].dropna()

        # Stats strip
        q1, median, q3 = np.percentile(series, [25, 50, 75])
        stats_cols = st.columns(5)
        for col, (lbl, val) in zip(stats_cols, [
            ("Mean",   f"{series.mean():.4g}"),
            ("Median", f"{median:.4g}"),
            ("Std",    f"{series.std():.4g}"),
            ("Skew",   f"{series.skew():.3f}"),
            ("Kurt",   f"{series.kurt():.3f}"),
        ]):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                  <div class="metric-value" style="font-size:1.2rem">{val}</div>
                  <div class="metric-label">{lbl}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("")

        if plot_type == "Histogram":
            bins = st.slider("Bins", 5, 100, 30)
            fig = px.histogram(df, x=sel_num, nbins=bins,
                               color_discrete_sequence=["#818cf8"])
        elif plot_type == "Box Plot":
            color_by = st.selectbox("Color by (optional)",
                                    ["None"] + cat_cols, key="box_col")
            fig = px.box(df, y=sel_num,
                         color=None if color_by == "None" else color_by,
                         color_discrete_sequence=COLOR_SEQ)
        elif plot_type == "Violin":
            color_by = st.selectbox("Group by",
                                    ["None"] + cat_cols, key="vio_col")
            fig = px.violin(df, y=sel_num,
                            color=None if color_by == "None" else color_by,
                            box=True, color_discrete_sequence=COLOR_SEQ)
        elif plot_type == "ECDF":
            fig = px.ecdf(df, x=sel_num, color_discrete_sequence=["#38bdf8"])
        else:  # Rug Plot
            fig = go.Figure(go.Box(x=series, name=sel_num,
                                   marker_color="#818cf8",
                                   boxpoints="all", jitter=0.3,
                                   pointpos=-1.8))

        fig.update_layout(**PLOTLY_LAYOUT, height=420,
                          title=f"{plot_type} — {sel_num}")
        st.plotly_chart(fig, use_container_width=True)

        # Outlier detection
        st.markdown('<p class="section-title">Outlier Analysis (IQR method)</p>',
                    unsafe_allow_html=True)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers = df[(df[sel_num] < lower) | (df[sel_num] > upper)]
        st.markdown(f"""
        <div class="insight-box">
          📌 IQR bounds: <b>[{lower:.4g}, {upper:.4g}]</b> &nbsp;·&nbsp;
          <b>{len(outliers)}</b> outliers detected
          ({len(outliers)/len(df)*100:.1f}% of rows)
        </div>""", unsafe_allow_html=True)
        if not outliers.empty:
            st.dataframe(outliers.sort_values(sel_num, ascending=False).head(50),
                         use_container_width=True, height=240)

# ─── Tab 3 — Categoricals ─────────────────────────────────────────────────────
with tabs[3]:
    if not cat_cols:
        st.warning("No categorical columns found.")
    else:
        st.markdown('<p class="section-title">Categorical Column Explorer</p>',
                    unsafe_allow_html=True)

        sel_cat = st.selectbox("Select column", cat_cols, key="cat_sel")

        vc = df[sel_cat].value_counts().reset_index()
        vc.columns = [sel_cat, "count"]
        vc["pct"] = (vc["count"] / vc["count"].sum() * 100).round(2)

        sort_vc = st.selectbox("Sort by", [sel_cat, "count", "pct"], key="cat_sort")
        sort_vc_dir = st.radio("Direction", ["Descending ↓", "Ascending ↑"],
                               horizontal=True, key="cat_dir")
        vc = vc.sort_values(sort_vc, ascending=(sort_vc_dir == "Ascending ↑"))

        top_n = st.slider("Show top N categories", 5, min(50, len(vc)), min(20, len(vc)))
        vc_top = vc.head(top_n)

        chart_type = st.radio("Chart", ["Bar", "Horizontal Bar", "Pie", "Treemap"],
                              horizontal=True)

        if chart_type == "Bar":
            fig = px.bar(vc_top, x=sel_cat, y="count", text="pct",
                         color="count", color_continuous_scale="Purples")
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
        elif chart_type == "Horizontal Bar":
            fig = px.bar(vc_top, y=sel_cat, x="count", text="pct",
                         orientation="h",
                         color="count", color_continuous_scale="Blues")
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
        elif chart_type == "Pie":
            fig = px.pie(vc_top, names=sel_cat, values="count",
                         color_discrete_sequence=COLOR_SEQ, hole=0.35)
        else:
            fig = px.treemap(vc_top, path=[sel_cat], values="count",
                             color="count", color_continuous_scale="Purpor")

        fig.update_layout(**PLOTLY_LAYOUT, height=450)
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(vc, use_container_width=True, height=260)

# ─── Tab 4 — Correlations ─────────────────────────────────────────────────────
with tabs[4]:
    if len(num_cols) < 2:
        st.warning("Need at least 2 numeric columns for correlation analysis.")
    else:
        st.markdown('<p class="section-title">Correlation Matrix</p>',
                    unsafe_allow_html=True)

        method = st.radio("Method", ["pearson", "spearman", "kendall"],
                          horizontal=True)
        corr = df[num_cols].corr(method=method)

        # Sort by correlation to a reference column
        ref_col = st.selectbox("Sort by correlation to", num_cols, key="corr_ref")
        sort_corr = corr[ref_col].abs().sort_values(ascending=False)
        sorted_cols = sort_corr.index.tolist()
        corr_sorted = corr.loc[sorted_cols, sorted_cols]

        fig = px.imshow(
            corr_sorted, text_auto=".2f", aspect="auto",
            color_continuous_scale=[[0,"#1e1042"],[0.5,"#13151e"],[1,"#6366f1"]],
            zmin=-1, zmax=1
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Top correlations table
        st.markdown('<p class="section-title">Strongest Correlations</p>',
                    unsafe_allow_html=True)
        pairs = []
        for i in range(len(num_cols)):
            for j in range(i+1, len(num_cols)):
                pairs.append({
                    "Column A": num_cols[i],
                    "Column B": num_cols[j],
                    f"{method.capitalize()} r": round(corr.iloc[i, j], 4),
                    "|r|": round(abs(corr.iloc[i, j]), 4),
                })
        pairs_df = pd.DataFrame(pairs)
        sort_corr_col = st.selectbox("Sort pairs by",
                                     [f"{method.capitalize()} r", "|r|"],
                                     key="pair_sort")
        pairs_asc = st.radio("Order", ["Descending ↓", "Ascending ↑"],
                             horizontal=True, key="pair_dir")
        pairs_df = pairs_df.sort_values(sort_corr_col,
                                         ascending=(pairs_asc == "Ascending ↑"))
        st.dataframe(pairs_df, use_container_width=True, height=280)

        # Scatter matrix
        st.markdown('<p class="section-title">Scatter Matrix</p>',
                    unsafe_allow_html=True)
        scatter_cols = st.multiselect("Select columns (2-5)",
                                      num_cols, default=num_cols[:min(4, len(num_cols))],
                                      key="scatter_cols")
        color_col = st.selectbox("Color by", ["None"] + cat_cols, key="scatter_color")
        if len(scatter_cols) >= 2:
            fig = px.scatter_matrix(
                df, dimensions=scatter_cols,
                color=None if color_col == "None" else color_col,
                color_discrete_sequence=COLOR_SEQ, opacity=0.7
            )
            fig.update_layout(**PLOTLY_LAYOUT, height=600)
            st.plotly_chart(fig, use_container_width=True)

# ─── Tab 5 — Data Quality ─────────────────────────────────────────────────────
with tabs[5]:
    st.markdown('<p class="section-title">Missing Values Analysis</p>',
                unsafe_allow_html=True)

    miss = df.isnull().sum().reset_index()
    miss.columns = ["column", "missing_count"]
    miss["missing_pct"] = (miss["missing_count"] / len(df) * 100).round(2)
    miss["present_pct"] = 100 - miss["missing_pct"]

    sort_miss = st.selectbox("Sort by",
                             ["missing_count", "missing_pct", "column"],
                             key="miss_sort")
    miss_dir = st.radio("Order", ["Descending ↓", "Ascending ↑"],
                        horizontal=True, key="miss_dir")
    miss = miss.sort_values(sort_miss, ascending=(miss_dir == "Ascending ↑"))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=miss["column"], x=miss["missing_pct"],
        orientation="h", name="Missing",
        marker_color="#f472b6", text=miss["missing_pct"].map(lambda x: f"{x}%"),
        textposition="outside"
    ))
    fig.add_trace(go.Bar(
        y=miss["column"], x=miss["present_pct"],
        orientation="h", name="Present",
        marker_color="#34d399", opacity=0.3
    ))
    fig.update_layout(**PLOTLY_LAYOUT, barmode="stack",
                      height=max(300, len(df.columns) * 30 + 80),
                      title="Missing vs Present (%)")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(miss[miss["missing_count"] > 0], use_container_width=True)

    # Duplicates
    st.markdown('<p class="section-title">Duplicate Rows</p>',
                unsafe_allow_html=True)
    dups = df[df.duplicated(keep=False)]
    st.markdown(f"""
    <div class="insight-box">
      🔁 Found <b>{len(dups)}</b> duplicate rows
      ({len(dups)/len(df)*100:.1f}% of total)
    </div>""", unsafe_allow_html=True)
    if not dups.empty:
        st.dataframe(dups.head(50), use_container_width=True, height=240)

    # Zero / negative analysis
    st.markdown('<p class="section-title">Zero & Negative Values</p>',
                unsafe_allow_html=True)
    zn_rows = []
    for c in num_cols:
        zeros   = (df[c] == 0).sum()
        negs    = (df[c] < 0).sum()
        zn_rows.append({"column": c, "zeros": zeros,
                         "negatives": negs,
                         "zero_pct": round(zeros/len(df)*100, 2),
                         "neg_pct":  round(negs/len(df)*100, 2)})
    zn_df = pd.DataFrame(zn_rows)
    sort_zn = st.selectbox("Sort by", zn_df.columns.tolist(), key="zn_sort")
    zn_dir  = st.radio("Order", ["Descending ↓", "Ascending ↑"],
                       horizontal=True, key="zn_dir")
    zn_df   = zn_df.sort_values(sort_zn, ascending=(zn_dir == "Ascending ↑"))
    st.dataframe(zn_df, use_container_width=True)

# ─── Tab 6 — Custom Plot ──────────────────────────────────────────────────────
with tabs[6]:
    st.markdown('<p class="section-title">Custom Chart Builder</p>',
                unsafe_allow_html=True)

    all_cols = df.columns.tolist()
    c1, c2, c3 = st.columns(3)
    with c1:
        x_col = st.selectbox("X axis", all_cols, key="cx")
    with c2:
        y_col = st.selectbox("Y axis", ["None"] + num_cols, key="cy")
    with c3:
        color_c = st.selectbox("Color by", ["None"] + all_cols, key="cc")

    chart_choice = st.selectbox("Chart type", [
        "Scatter", "Line", "Bar", "Area", "Histogram",
        "Box", "Violin", "Density Heatmap", "Bubble"
    ])

    size_col = "None"
    if chart_choice == "Bubble" and num_cols:
        size_col = st.selectbox("Bubble size", num_cols, key="bs")

    color_arg = None if color_c == "None" else color_c
    y_arg     = None if y_col  == "None" else y_col

    try:
        if chart_choice == "Scatter":
            fig = px.scatter(df, x=x_col, y=y_arg, color=color_arg,
                             color_discrete_sequence=COLOR_SEQ, opacity=0.8)
        elif chart_choice == "Line":
            sort_for_line = st.selectbox("Sort X by", ["None"] + all_cols, key="lsort")
            pdf = df.sort_values(sort_for_line) if sort_for_line != "None" else df
            fig = px.line(pdf, x=x_col, y=y_arg, color=color_arg,
                          color_discrete_sequence=COLOR_SEQ)
        elif chart_choice == "Bar":
            fig = px.bar(df, x=x_col, y=y_arg, color=color_arg,
                         color_discrete_sequence=COLOR_SEQ)
        elif chart_choice == "Area":
            fig = px.area(df, x=x_col, y=y_arg, color=color_arg,
                          color_discrete_sequence=COLOR_SEQ)
        elif chart_choice == "Histogram":
            fig = px.histogram(df, x=x_col, color=color_arg,
                               color_discrete_sequence=COLOR_SEQ, nbins=30)
        elif chart_choice == "Box":
            fig = px.box(df, x=color_arg, y=x_col,
                         color=color_arg, color_discrete_sequence=COLOR_SEQ)
        elif chart_choice == "Violin":
            fig = px.violin(df, x=color_arg, y=x_col,
                            color=color_arg, box=True,
                            color_discrete_sequence=COLOR_SEQ)
        elif chart_choice == "Density Heatmap":
            fig = px.density_heatmap(df, x=x_col, y=y_arg,
                                     color_continuous_scale="Purpor")
        else:  # Bubble
            fig = px.scatter(df, x=x_col, y=y_arg,
                             size=None if size_col == "None" else size_col,
                             color=color_arg,
                             color_discrete_sequence=COLOR_SEQ, opacity=0.7)

        fig.update_layout(**PLOTLY_LAYOUT, height=520)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Could not render chart: {e}")
