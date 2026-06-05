# 🔬 DataLens EDA Studio

A professional, interactive **Exploratory Data Analysis** app built with Streamlit and Plotly.

---

## ✨ Features

| Feature | Details |
|---|---|
| **6 Built-in Datasets** | Titanic, Iris, Tips, Gapminder, Car Crashes, Penguins |
| **File Upload** | CSV, Excel, JSON, Parquet |
| **Global Filters** | Numeric range sliders, multi-select categorical filters |
| **Sorting** | Sort any column in any tab, ascending or descending |
| **Data Table** | Column search, sortable schema view, CSV export |
| **Statistical Summary** | Full describe() with sortable columns |
| **Numeric Analysis** | Histogram, Box, Violin, ECDF, Rug + outlier detection (IQR) |
| **Categorical Analysis** | Bar, Pie, Treemap + frequency table |
| **Correlation** | Pearson/Spearman/Kendall heatmap + scatter matrix |
| **Data Quality** | Missing value chart, duplicate detection, zero/negative analysis |
| **Custom Chart Builder** | Scatter, Line, Bar, Area, Box, Violin, Density Heatmap, Bubble |

---

## 🚀 Local Setup

```bash
# Clone / copy this folder, then:
pip install -r requirements.txt
streamlit run app.py
```

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this folder to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch (`main`), and set **Main file path** = `app.py`
4. Click **Deploy** — live in ~2 minutes!

> Streamlit Cloud reads `requirements.txt` automatically.

---

## 🐳 Deploy with Docker

```bash
docker build -t datalens .
docker run -p 8501:8501 datalens
# Open http://localhost:8501
```

---

## 🏗️ Project Structure

```
eda_project/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker deployment
└── README.md         # This file
```
