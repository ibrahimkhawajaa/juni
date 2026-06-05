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
COLOR_SEQUENCE = px.colors.qualitative.Pastel

# ── Data loader ────────────────────────────────────────────────────────────────
@st.cache_data
def load_builtin_dataset(dataset_name):
    if dataset_name == "Titanic 🚢":
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        return pd.read_csv(url)
    elif dataset_name == "Iris 🌸":
        from sklearn.datasets import load_iris
        iris_data = load_iris(as_frame=True)
        dataframe = iris_data.frame.copy()
        dataframe["species"] = iris_data.target_names[dataframe["target"]]
        return dataframe.drop("target", axis=1)
    elif dataset_name == "Tips 🍽️":
        return px.data.tips()
    elif dataset_name == "Gapminder 🌍":
        return px.data.gapminder().query("year == 2007").drop("year", axis=1)
    elif dataset_name == "Car Crashes 🚗":
        return sns.load_dataset("car_crashes")
    elif dataset_name == "Penguins 🐧":
        return sns.load_dataset("penguins")
    return None

@st.cache_data
def parse_uploaded_file(uploaded_file):
    filename_lower = uploaded_file.name.lower()
    if filename_lower.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif filename_lower.endswith((".xls", ".xlsx")):
        return pd.read_excel(uploaded_file)
    elif filename_lower.endswith(".json"):
        return pd.read_json(uploaded_file)
    elif filename_lower.endswith(".parquet"):
        return pd.read_parquet(uploaded_file)
    return None

def create_type_badge(data_type):
    type_string = str(data_type)
    if "int" in type_string or "float" in type_string:
        return '<span class="badge badge-num">numeric</span>'
    elif "datetime" in type_string:
        return '<span class="badge badge-date">datetime</span>'
    elif "bool" in type_string:
        return '<span class="badge badge-bool">bool</span>'
    else:
        return '<span class="badge badge-cat">categorical</span>'

def apply_sorting_to_dataframe(dataframe, sorting_column, is_ascending):
    if sorting_column and sorting_column in dataframe.columns:
        return dataframe.sort_values(sorting_column, ascending=is_ascending)
    return dataframe

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:Space Mono,monospace;font-size:1.1rem;
                color:#818cf8;padding:0.5rem 0 1rem;letter-spacing:0.05em'>
      🔬 DATALENS
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Data Source**")
    selected_data_source = st.radio("", ["Built-in Dataset", "Upload File"], label_visibility="collapsed")

    dataframe = None
    dataset_name = ""

    if selected_data_source == "Built-in Dataset":
        dataset_name = st.selectbox(
            "Choose dataset",
            ["Titanic 🚢", "Iris 🌸", "Tips 🍽️", "Gapminder 🌍",
             "Car Crashes 🚗", "Penguins 🐧"]
        )
        dataframe = load_builtin_dataset(dataset_name)
    else:
        uploaded_file = st.file_uploader("Upload CSV / Excel / JSON / Parquet",
                                    type=["csv","xlsx","xls","json","parquet"])
        if uploaded_file:
            dataframe = parse_uploaded_file(uploaded_file)
            dataset_name = uploaded_file.name

    st.divider()

    if dataframe is not None:
        st.markdown("**Global Filters**")
        numeric_columns = dataframe.select_dtypes(include=np.number).columns.tolist()
        categorical_columns = dataframe.select_dtypes(include="object").columns.tolist()

        # Row limit
        maximum_rows_to_display = st.slider("Max rows to display", 10, min(5000, len(dataframe)),
                              min(500, len(dataframe)), step=10)

        # Numeric filter
        if numeric_columns:
            selected_numeric_filter_column = st.selectbox("Filter by numeric column", ["None"] + numeric_columns)
            if selected_numeric_filter_column != "None":
                column_minimum_value = float(dataframe[selected_numeric_filter_column].min())
                column_maximum_value = float(dataframe[selected_numeric_filter_column].max())
                selected_range = st.slider(f"{selected_numeric_filter_column} range", column_minimum_value, column_maximum_value, (column_minimum_value, column_maximum_value))
                dataframe = dataframe[(dataframe[selected_numeric_filter_column] >= selected_range[0]) & (dataframe[selected_numeric_filter_column] <= selected_range[1])]

        # Categorical filter
        if categorical_columns:
            selected_category_filter_column = st.selectbox("Filter by category column", ["None"] + categorical_columns)
            if selected_category_filter_column != "None":
                available_category_values = dataframe[selected_category_filter_column].dropna().unique().tolist()
                selected_category_values = st.multiselect(f"{selected_category_filter_column} values", available_category_values, default=available_category_values)
                if selected_category_values:
                    dataframe = dataframe[dataframe[selected_category_filter_column].isin(selected_category_values)]

        dataframe = dataframe.head(maximum_rows_to_display)

        st.divider()
        st.markdown("**Sorting**")
        sort_column_selected = st.selectbox("Sort by column", ["None"] + dataframe.columns.tolist())
        sort_direction = st.radio("Direction", ["Ascending ↑", "Descending ↓"],
                            horizontal=True)
        is_ascending_order = sort_direction == "Ascending ↑"
        if sort_column_selected != "None":
            dataframe = apply_sorting_to_dataframe(dataframe, sort_column_selected, is_ascending_order)

# ── Main content ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
  <p class="hero-title">DataLens EDA Studio</p>
  <p class="hero-sub">Exploratory Data Analysis · {dataset_name or 'No dataset loaded'}</p>
</div>
""", unsafe_allow_html=True)

if dataframe is None:
    st.info("👈 Select a built-in dataset or upload your own file to get started.")
    st.stop()

# ── Key metrics ────────────────────────────────────────────────────────────────
numeric_columns = dataframe.select_dtypes(include=np.number).columns.tolist()
categorical_columns = dataframe.select_dtypes(include="object").columns.tolist()
total_missing_values = dataframe.isnull().sum().sum()
missing_percentage = round(total_missing_values / dataframe.size * 100, 1)
total_duplicate_rows = dataframe.duplicated().sum()

metric_column_1, metric_column_2, metric_column_3, metric_column_4, metric_column_5, metric_column_6 = st.columns(6)
all_metrics = [
    (len(dataframe), "Rows"),
    (len(dataframe.columns), "Columns"),
    (len(numeric_columns), "Numeric"),
    (len(categorical_columns), "Categorical"),
    (f"{missing_percentage}%", "Missing"),
    (total_duplicate_rows, "Duplicates"),
]
for metric_column, (metric_value, metric_label) in zip([metric_column_1,metric_column_2,metric_column_3,metric_column_4,metric_column_5,metric_column_6], all_metrics):
    with metric_column:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-value">{metric_value}</div>
          <div class="metric-label">{metric_label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("")

# ── Tabs ───────────────────────────────────────────────────────────────────────
all_tabs = st.tabs([
    "📋 Data Table",
    "📊 Overview",
    "🔢 Numerics",
    "🏷️ Categoricals",
    "🔗 Correlations",
    "🚨 Data Quality",
    "📈 Custom Plot",
])

# ─── Tab 0 — Data Table ────────────────────────────────────────────────────────
with all_tabs[0]:
    st.markdown('<p class="section-title">Dataset Preview</p>', unsafe_allow_html=True)

    search_column_input, sort_by_column, sort_direction_selector = st.columns([3, 2, 1])
    with search_column_input:
        column_search_text = st.text_input("🔍 Search column name", "")
    with sort_by_column:
        table_sort_column = st.selectbox("Sort by", ["None"] + dataframe.columns.tolist(), key="tab_sort")
    with sort_direction_selector:
        table_sort_direction = st.selectbox("Dir", ["↑ Asc", "↓ Desc"], key="tab_dir")

    preview_dataframe = dataframe.copy()
    if column_search_text:
        matching_columns = [column for column in preview_dataframe.columns if column_search_text.lower() in column.lower()]
        preview_dataframe = preview_dataframe[matching_columns]
    if table_sort_column != "None" and table_sort_column in preview_dataframe.columns:
        preview_dataframe = preview_dataframe.sort_values(table_sort_column, ascending=(table_sort_direction == "↑ Asc"))

    st.dataframe(preview_dataframe, use_container_width=True, height=420)

    # Column schema
    st.markdown('<p class="section-title">Column Schema</p>', unsafe_allow_html=True)
    schema_information = []
    for column_name in dataframe.columns:
        schema_information.append({
            "Column": column_name,
            "Type": str(dataframe[column_name].dtype),
            "Non-Null": dataframe[column_name].count(),
            "Null": dataframe[column_name].isnull().sum(),
            "Unique": dataframe[column_name].nunique(),
            "Sample": str(dataframe[column_name].dropna().iloc[0]) if not dataframe[column_name].dropna().empty else "—",
        })
    schema_dataframe = pd.DataFrame(schema_information)
    st.dataframe(schema_dataframe, use_container_width=True, height=300)

    # Download
    csv_bytes = dataframe.to_csv(index=False).encode()
    st.download_button("⬇️ Download filtered CSV", csv_bytes,
                       "filtered_data.csv", "text/csv")

# ─── Tab 1 — Overview ─────────────────────────────────────────────────────────
with all_tabs[1]:
    st.markdown('<p class="section-title">Statistical Summary</p>', unsafe_allow_html=True)

    sort_statistics_by = st.selectbox("Sort summary by", ["None"] + dataframe.describe().columns.tolist(), key="stat_sort")
    statistics_sort_direction = st.radio("Order", ["Ascending ↑", "Descending ↓"], horizontal=True, key="stat_dir")

    statistics_summary = dataframe.describe(include="all").T.reset_index().rename(columns={"index":"column"})
    if sort_statistics_by != "None" and sort_statistics_by in statistics_summary.columns:
        statistics_summary = statistics_summary.sort_values(sort_statistics_by, ascending=(statistics_sort_direction == "Ascending ↑"))
    st.dataframe(statistics_summary, use_container_width=True, height=380)

    st.markdown('<p class="section-title">Shape of Numeric Distributions</p>', unsafe_allow_html=True)
    if numeric_columns:
        total_numeric_count = len(numeric_columns)
        columns_per_row = 3
        total_subplot_rows = (total_numeric_count + columns_per_row - 1) // columns_per_row
        histogram_figure = make_subplots(rows=total_subplot_rows, cols=columns_per_row,
                            subplot_titles=numeric_columns)
        for column_index, column_name in enumerate(numeric_columns):
            row_index, column_index_in_row = divmod(column_index, columns_per_row)
            histogram_figure.add_trace(
                go.Histogram(x=dataframe[column_name].dropna(), name=column_name,
                             marker_color="#818cf8", opacity=0.8,
                             showlegend=False),
                row=row_index+1, col=column_index_in_row+1
            )
        histogram_figure.update_layout(**PLOTLY_LAYOUT, height=max(300, total_subplot_rows * 220))
        st.plotly_chart(histogram_figure, use_container_width=True)

# ─── Tab 2 — Numerics ─────────────────────────────────────────────────────────
with all_tabs[2]:
    if not numeric_columns:
        st.warning("No numeric columns found.")
    else:
        st.markdown('<p class="section-title">Numeric Column Explorer</p>',
                    unsafe_allow_html=True)

        left_section, right_section = st.columns(2)
        with left_section:
            selected_numeric_column = st.selectbox("Select column", numeric_columns, key="num_sel")
        with right_section:
            selected_chart_type = st.selectbox("Chart type",
                                     ["Histogram", "Box Plot", "Violin",
                                      "ECDF", "Rug Plot"])

        numeric_data_series = dataframe[selected_numeric_column].dropna()

        # Stats strip
        percentile_25, percentile_50, percentile_75 = np.percentile(numeric_data_series, [25, 50, 75])
        stats_display_columns = st.columns(5)
        statistics_info = [
            ("Mean",   f"{numeric_data_series.mean():.4g}"),
            ("Median", f"{percentile_50:.4g}"),
            ("Std",    f"{numeric_data_series.std():.4g}"),
            ("Skew",   f"{numeric_data_series.skew():.3f}"),
            ("Kurt",   f"{numeric_data_series.kurt():.3f}"),
        ]
        for column_area, (stat_label, stat_value) in zip(stats_display_columns, statistics_info):
            with column_area:
                st.markdown(f"""
                <div class="metric-card">
                  <div class="metric-value" style="font-size:1.2rem">{stat_value}</div>
                  <div class="metric-label">{stat_label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("")

        if selected_chart_type == "Histogram":
            number_of_bins = st.slider("Bins", 5, 100, 30)
            chart_figure = px.histogram(dataframe, x=selected_numeric_column, nbins=number_of_bins,
                               color_discrete_sequence=["#818cf8"])
        elif selected_chart_type == "Box Plot":
            color_by_column = st.selectbox("Color by (optional)",
                                    ["None"] + categorical_columns, key="box_col")
            chart_figure = px.box(dataframe, y=selected_numeric_column,
                         color=None if color_by_column == "None" else color_by_column,
                         color_discrete_sequence=COLOR_SEQUENCE)
        elif selected_chart_type == "Violin":
            group_by_column = st.selectbox("Group by",
                                    ["None"] + categorical_columns, key="vio_col")
            chart_figure = px.violin(dataframe, y=selected_numeric_column,
                            color=None if group_by_column == "None" else group_by_column,
                            box=True, color_discrete_sequence=COLOR_SEQUENCE)
        elif selected_chart_type == "ECDF":
            chart_figure = px.ecdf(dataframe, x=selected_numeric_column, color_discrete_sequence=["#38bdf8"])
        else:  # Rug Plot
            chart_figure = go.Figure(go.Box(x=numeric_data_series, name=selected_numeric_column,
                                   marker_color="#818cf8",
                                   boxpoints="all", jitter=0.3,
                                   pointpos=-1.8))

        chart_figure.update_layout(**PLOTLY_LAYOUT, height=420,
                          title=f"{selected_chart_type} — {selected_numeric_column}")
        st.plotly_chart(chart_figure, use_container_width=True)

        # Outlier detection
        st.markdown('<p class="section-title">Outlier Analysis (IQR method)</p>',
                    unsafe_allow_html=True)
        interquartile_range = percentile_75 - percentile_25
        lower_outlier_bound = percentile_25 - 1.5 * interquartile_range
        upper_outlier_bound = percentile_75 + 1.5 * interquartile_range
        outlier_rows = dataframe[(dataframe[selected_numeric_column] < lower_outlier_bound) | (dataframe[selected_numeric_column] > upper_outlier_bound)]
        st.markdown(f"""
        <div class="insight-box">
          📌 IQR bounds: <b>[{lower_outlier_bound:.4g}, {upper_outlier_bound:.4g}]</b> &nbsp;·&nbsp;
          <b>{len(outlier_rows)}</b> outliers detected
          ({len(outlier_rows)/len(dataframe)*100:.1f}% of rows)
        </div>""", unsafe_allow_html=True)
        if not outlier_rows.empty:
            st.dataframe(outlier_rows.sort_values(selected_numeric_column, ascending=False).head(50),
                         use_container_width=True, height=240)

# ─── Tab 3 — Categoricals ─────────────────────────────────────────────────────
with all_tabs[3]:
    if not categorical_columns:
        st.warning("No categorical columns found.")
    else:
        st.markdown('<p class="section-title">Categorical Column Explorer</p>',
                    unsafe_allow_html=True)

        selected_category_column = st.selectbox("Select column", categorical_columns, key="cat_sel")

        category_value_counts = dataframe[selected_category_column].value_counts().reset_index()
        category_value_counts.columns = [selected_category_column, "count"]
        category_value_counts["percentage"] = (category_value_counts["count"] / category_value_counts["count"].sum() * 100).round(2)

        sort_by_metric = st.selectbox("Sort by", [selected_category_column, "count", "percentage"], key="cat_sort")
        sort_direction_metric = st.radio("Direction", ["Descending ↓", "Ascending ↑"],
                               horizontal=True, key="cat_dir")
        category_value_counts = category_value_counts.sort_values(sort_by_metric, ascending=(sort_direction_metric == "Ascending ↑"))

        number_of_categories_display = st.slider("Show top N categories", 5, min(50, len(category_value_counts)), min(20, len(category_value_counts)))
        top_categories_data = category_value_counts.head(number_of_categories_display)

        selected_visualization_type = st.radio("Chart", ["Bar", "Horizontal Bar", "Pie", "Treemap"],
                              horizontal=True)

        if selected_visualization_type == "Bar":
            chart_figure = px.bar(top_categories_data, x=selected_category_column, y="count", text="percentage",
                         color="count", color_continuous_scale="Purples")
            chart_figure.update_traces(texttemplate="%{text}%", textposition="outside")
        elif selected_visualization_type == "Horizontal Bar":
            chart_figure = px.bar(top_categories_data, y=selected_category_column, x="count", text="percentage",
                         orientation="h",
                         color="count", color_continuous_scale="Blues")
            chart_figure.update_traces(texttemplate="%{text}%", textposition="outside")
        elif selected_visualization_type == "Pie":
            chart_figure = px.pie(top_categories_data, names=selected_category_column, values="count",
                         color_discrete_sequence=COLOR_SEQUENCE, hole=0.35)
        else:
            chart_figure = px.treemap(top_categories_data, path=[selected_category_column], values="count",
                             color="count", color_continuous_scale="Purpor")

        chart_figure.update_layout(**PLOTLY_LAYOUT, height=450)
        st.plotly_chart(chart_figure, use_container_width=True)

        st.dataframe(category_value_counts, use_container_width=True, height=260)

# ─── Tab 4 — Correlations ─────────────────────────────────────────────────────
with all_tabs[4]:
    if len(numeric_columns) < 2:
        st.warning("Need at least 2 numeric columns for correlation analysis.")
    else:
        st.markdown('<p class="section-title">Correlation Matrix</p>',
                    unsafe_allow_html=True)

        correlation_method_selected = st.radio("Method", ["pearson", "spearman", "kendall"],
                          horizontal=True)
        correlation_matrix = dataframe[numeric_columns].corr(method=correlation_method_selected)

        # Sort by correlation to a reference column
        reference_column_name = st.selectbox("Sort by correlation to", numeric_columns, key="corr_ref")
        sorted_correlation_values = correlation_matrix[reference_column_name].abs().sort_values(ascending=False)
        sorted_column_list = sorted_correlation_values.index.tolist()
        sorted_correlation_matrix = correlation_matrix.loc[sorted_column_list, sorted_column_list]

        heatmap_figure = px.imshow(
            sorted_correlation_matrix, text_auto=".2f", aspect="auto",
            color_continuous_scale=[[0,"#1e1042"],[0.5,"#13151e"],[1,"#6366f1"]],
            zmin=-1, zmax=1
        )
        heatmap_figure.update_layout(**PLOTLY_LAYOUT, height=500)
        st.plotly_chart(heatmap_figure, use_container_width=True)

        # Top correlations table
        st.markdown('<p class="section-title">Strongest Correlations</p>',
                    unsafe_allow_html=True)
        correlation_pairs_list = []
        for first_index in range(len(numeric_columns)):
            for second_index in range(first_index+1, len(numeric_columns)):
                correlation_pairs_list.append({
                    "Column A": numeric_columns[first_index],
                    "Column B": numeric_columns[second_index],
                    f"{correlation_method_selected.capitalize()} r": round(correlation_matrix.iloc[first_index, second_index], 4),
                    "|r|": round(abs(correlation_matrix.iloc[first_index, second_index]), 4),
                })
        correlation_pairs_dataframe = pd.DataFrame(correlation_pairs_list)
        sort_pairs_column = st.selectbox("Sort pairs by",
                                     [f"{correlation_method_selected.capitalize()} r", "|r|"],
                                     key="pair_sort")
        pairs_sort_order = st.radio("Order", ["Descending ↓", "Ascending ↑"],
                             horizontal=True, key="pair_dir")
        correlation_pairs_dataframe = correlation_pairs_dataframe.sort_values(sort_pairs_column,
                                         ascending=(pairs_sort_order == "Ascending ↑"))
        st.dataframe(correlation_pairs_dataframe, use_container_width=True, height=280)

        # Scatter matrix
        st.markdown('<p class="section-title">Scatter Matrix</p>',
                    unsafe_allow_html=True)
        selected_scatter_columns_list = st.multiselect("Select columns (2-5)",
                                      numeric_columns, default=numeric_columns[:min(4, len(numeric_columns))],
                                      key="scatter_cols")
        scatter_color_by = st.selectbox("Color by", ["None"] + categorical_columns, key="scatter_color")
        if len(selected_scatter_columns_list) >= 2:
            scatter_figure = px.scatter_matrix(
                dataframe, dimensions=selected_scatter_columns_list,
                color=None if scatter_color_by == "None" else scatter_color_by,
                color_discrete_sequence=COLOR_SEQUENCE, opacity=0.7
            )
            scatter_figure.update_layout(**PLOTLY_LAYOUT, height=600)
            st.plotly_chart(scatter_figure, use_container_width=True)

# ─── Tab 5 — Data Quality ─────────────────────────────────────────────────────
with all_tabs[5]:
    st.markdown('<p class="section-title">Missing Values Analysis</p>',
                unsafe_allow_html=True)

    missing_values_analysis = dataframe.isnull().sum().reset_index()
    missing_values_analysis.columns = ["column", "missing_count"]
    missing_values_analysis["missing_percentage"] = (missing_values_analysis["missing_count"] / len(dataframe) * 100).round(2)
    missing_values_analysis["present_percentage"] = 100 - missing_values_analysis["missing_percentage"]

    sort_missing_by_column = st.selectbox("Sort by",
                             ["missing_count", "missing_percentage", "column"],
                             key="miss_sort")
    missing_sort_direction = st.radio("Order", ["Descending ↓", "Ascending ↑"],
                        horizontal=True, key="miss_dir")
    missing_values_analysis = missing_values_analysis.sort_values(sort_missing_by_column, ascending=(missing_sort_direction == "Ascending ↑"))

    missing_figure = go.Figure()
    missing_figure.add_trace(go.Bar(
        y=missing_values_analysis["column"], x=missing_values_analysis["missing_percentage"],
        orientation="h", name="Missing",
        marker_color="#f472b6", text=missing_values_analysis["missing_percentage"].map(lambda x: f"{x}%"),
        textposition="outside"
    ))
    missing_figure.add_trace(go.Bar(
        y=missing_values_analysis["column"], x=missing_values_analysis["present_percentage"],
        orientation="h", name="Present",
        marker_color="#34d399", opacity=0.3
    ))
    missing_figure.update_layout(**PLOTLY_LAYOUT, barmode="stack",
                      height=max(300, len(dataframe.columns) * 30 + 80),
                      title="Missing vs Present (%)")
    st.plotly_chart(missing_figure, use_container_width=True)
    st.dataframe(missing_values_analysis[missing_values_analysis["missing_count"] > 0], use_container_width=True)

    # Duplicates
    st.markdown('<p class="section-title">Duplicate Rows</p>',
                unsafe_allow_html=True)
    duplicate_rows_data = dataframe[dataframe.duplicated(keep=False)]
    st.markdown(f"""
    <div class="insight-box">
      🔁 Found <b>{len(duplicate_rows_data)}</b> duplicate rows
      ({len(duplicate_rows_data)/len(dataframe)*100:.1f}% of total)
    </div>""", unsafe_allow_html=True)
    if not duplicate_rows_data.empty:
        st.dataframe(duplicate_rows_data.head(50), use_container_width=True, height=240)

    # Zero / negative analysis
    st.markdown('<p class="section-title">Zero & Negative Values</p>',
                unsafe_allow_html=True)
    zero_negative_analysis = []
    for column_name in numeric_columns:
        zero_value_count = (dataframe[column_name] == 0).sum()
        negative_value_count = (dataframe[column_name] < 0).sum()
        zero_negative_analysis.append({
            "column": column_name, 
            "zero_count": zero_value_count,
            "negative_count": negative_value_count,
            "zero_percentage": round(zero_value_count/len(dataframe)*100, 2),
            "negative_percentage": round(negative_value_count/len(dataframe)*100, 2)
        })
    zero_negative_dataframe = pd.DataFrame(zero_negative_analysis)
    sort_zero_negative_by = st.selectbox("Sort by", zero_negative_dataframe.columns.tolist(), key="zn_sort")
    zero_negative_sort_direction = st.radio("Order", ["Descending ↓", "Ascending ↑"],
                       horizontal=True, key="zn_dir")
    zero_negative_dataframe = zero_negative_dataframe.sort_values(sort_zero_negative_by, ascending=(zero_negative_sort_direction == "Ascending ↑"))
    st.dataframe(zero_negative_dataframe, use_container_width=True)

# ─── Tab 6 — Custom Plot ──────────────────────────────────────────────────────
with all_tabs[6]:
    st.markdown('<p class="section-title">Custom Chart Builder</p>',
                unsafe_allow_html=True)

    all_columns_list = dataframe.columns.tolist()
    x_axis_area, y_axis_area, color_area = st.columns(3)
    with x_axis_area:
        x_axis_column_name = st.selectbox("X axis", all_columns_list, key="cx")
    with y_axis_area:
        y_axis_column_name = st.selectbox("Y axis", ["None"] + numeric_columns, key="cy")
    with color_area:
        color_column_name = st.selectbox("Color by", ["None"] + all_columns_list, key="cc")

    custom_chart_type = st.selectbox("Chart type", [
        "Scatter", "Line", "Bar", "Area", "Histogram",
        "Box", "Violin", "Density Heatmap", "Bubble"
    ])

    bubble_size_column_name = "None"
    if custom_chart_type == "Bubble" and numeric_columns:
        bubble_size_column_name = st.selectbox("Bubble size", numeric_columns, key="bs")

    color_argument = None if color_column_name == "None" else color_column_name
    y_axis_argument = None if y_axis_column_name == "None" else y_axis_column_name

    try:
        if custom_chart_type == "Scatter":
            custom_figure = px.scatter(dataframe, x=x_axis_column_name, y=y_axis_argument, color=color_argument,
                             color_discrete_sequence=COLOR_SEQUENCE, opacity=0.8)
        elif custom_chart_type == "Line":
            line_sort_column = st.selectbox("Sort X by", ["None"] + all_columns_list, key="lsort")
            line_plot_dataframe = dataframe.sort_values(line_sort_column) if line_sort_column != "None" else dataframe
            custom_figure = px.line(line_plot_dataframe, x=x_axis_column_name, y=y_axis_argument, color=color_argument,
                          color_discrete_sequence=COLOR_SEQUENCE)
        elif custom_chart_type == "Bar":
            custom_figure = px.bar(dataframe, x=x_axis_column_name, y=y_axis_argument, color=color_argument,
                         color_discrete_sequence=COLOR_SEQUENCE)
        elif custom_chart_type == "Area":
            custom_figure = px.area(dataframe, x=x_axis_column_name, y=y_axis_argument, color=color_argument,
                          color_discrete_sequence=COLOR_SEQUENCE)
        elif custom_chart_type == "Histogram":
            custom_figure = px.histogram(dataframe, x=x_axis_column_name, color=color_argument,
                               color_discrete_sequence=COLOR_SEQUENCE, nbins=30)
        elif custom_chart_type == "Box":
            custom_figure = px.box(dataframe, x=color_argument, y=x_axis_column_name,
                         color=color_argument, color_discrete_sequence=COLOR_SEQUENCE)
        elif custom_chart_type == "Violin":
            custom_figure = px.violin(dataframe, x=color_argument, y=x_axis_column_name,
                            color=color_argument, box=True,
                            color_discrete_sequence=COLOR_SEQUENCE)
        elif custom_chart_type == "Density Heatmap":
            custom_figure = px.density_heatmap(dataframe, x=x_axis_column_name, y=y_axis_argument,
                                     color_continuous_scale="Purpor")
        else:  # Bubble
            custom_figure = px.scatter(dataframe, x=x_axis_column_name, y=y_axis_argument,
                             size=None if bubble_size_column_name == "None" else bubble_size_column_name,
                             color=color_argument,
                             color_discrete_sequence=COLOR_SEQUENCE, opacity=0.7)

        custom_figure.update_layout(**PLOTLY_LAYOUT, height=520)
        st.plotly_chart(custom_figure, use_container_width=True)

    except Exception as error_message:
        st.error(f"Could not render chart: {error_message}")
