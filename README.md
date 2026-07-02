### Customer Retention & Churn Analysis Dashboard

A fully interactive, browser-based churn analysis system built with **Python**, **Streamlit**, and **Plotly**. Upload any customer or subscription dataset and instantly get retention insights, cohort analysis, survival curves, CLV breakdowns, and actionable recommendations — all in a dark-themed, animated dashboard.

---

## 🚀 Live Features

| Tab | What You Get |
|-----|-------------|
| **Overview** | Churn donut chart, tenure violin, monthly charge box plot, scatter of tenure vs charges |
| **Cohort & Survival** | Monthly cohort retention line, churn rate trend (dual-axis), Kaplan-Meier style survival curve |
| **CLV Analysis** | Customer Lifetime Value distribution, CLV by segment, revenue lost to churn estimate |
| **Segment Drill-Down** | Stacked churn vs retention bar charts for any categorical column |
| **Correlations** | Feature–churn Pearson correlation bar, full numeric heatmap, correlation table |
| **Insights & Recs** | Auto-generated data-driven insights + 8 strategic retention recommendations, export to `.txt` / `.csv` |
| **Data Quality** | Missing values, duplicates, per-column quality badges, descriptive statistics, data preview |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — web app framework
- **Plotly** — interactive charts with GPU-composited animations
- **Pandas / NumPy** — data wrangling
- **pdfplumber** *(optional)* — PDF table extraction

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/churn-analysis-dashboard.git
cd churn-analysis-dashboard

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## 📦 Requirements

Create a `requirements.txt` with:

```
streamlit>=1.32.0
plotly>=5.20.0
pandas>=2.0.0
numpy>=1.26.0
openpyxl>=3.1.0
pdfplumber>=0.10.0
statsmodels>=0.14.0
```

---

## 📁 Supported File Formats

| Format | Notes |
|--------|-------|
| `.csv` | Auto-detects encoding (UTF-8, Latin-1, CP1252) |
| `.xlsx` / `.xls` | Reads via openpyxl / xlrd |
| `.pdf` | Extracts tables using pdfplumber |

If no file is uploaded, the app loads a built-in synthetic dataset of 1,500 customers for instant demo use.

---

## 🗂️ Dataset Requirements

Your dataset should contain at minimum:

- A **churn column** — binary (`0/1`, `Yes/No`, `True/False`)
- Ideally a **tenure column** — numeric (months active)
- Ideally a **signup/cohort column** — date or year-month string
- Any additional numeric or categorical columns (charges, contract type, region, etc.)

The app auto-detects column roles using keyword matching, with manual override dropdowns in the sidebar.

### Recommended Public Datasets

- [Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- [SaaS Subscription & Churn Analytics — Kaggle](https://www.kaggle.com/datasets/rivalytics/saas-subscription-and-churn-analytics-dataset)
- [E-Commerce Behavior Data — Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store)

---

## 📊 Key Metrics Computed

- **Churn Rate** — percentage of customers lost
- **Retention Rate** — cohort-level month-by-month retention
- **Customer Lifetime Value (CLV)** — tenure × monthly charges
- **Survival Probability** — Kaplan-Meier style survival curve with 95% CI
- **Feature Correlations** — absolute Pearson r against churn label
- **Segment Churn Rates** — per-category breakdown for any categorical feature

---

## 🎨 Dashboard Design

- Dark theme (`#0F0E0E` background) with blue accent (`#4d9fff`)
- Smooth CSS entry animations using `fadeRight` / `fadeUp` keyframes
- `will-change: transform, opacity` for GPU-composited, jank-free motion
- Plotly figures use a 600ms `cubic-in-out` transition on data updates
- Hover micro-interactions on metric cards, insight boxes, and recommendation cards

---

## 📤 Exports

From the **Insights & Recs** tab you can download:

- `churn_report.txt` — full text report with metrics, insights, and recommendations
- `cleaned_data.csv` — the auto-cast, cleaned version of your uploaded dataset
- `cohort_table.csv` — monthly cohort retention table *(requires signup + tenure columns)*

---

## 📂 Project Structure

```
churn-analysis-dashboard/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── sample_data/            # (Optional) place your own CSVs here
```

---

## 💡 Business Context

Customer churn is one of the highest-impact problems in SaaS, fintech, edtech, and subscription businesses. Reducing churn by even 1–2 percentage points can significantly improve revenue. This dashboard simulates the type of retention analytics work done by data analysts in product, growth, and CX teams — covering everything from cohort diagnostics to actionable retention strategy.

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).