# 🍬 Factory Reallocation & Shipping Optimization Recommendation System
### Nassau Candy Distributor — Supply Chain Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-RandomForest-F7931E?logo=scikitlearn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

---

## 📌 Overview

This project is an end-to-end **supply chain intelligence system** built for **Nassau Candy Distributor** — a U.S. and Canada-based candy distribution company. The system recommends optimal factory reallocation and shipping strategies by predicting shipment **lead times** using a trained **Random Forest Regressor** model.

The interactive **Streamlit dashboard** enables business analysts to simulate different operational scenarios, compare actual vs. optimized lead times, assess risks, and download ranked optimization reports — all through a real-time interface.

---

## 🚀 Live App Features

The Streamlit app (`app.py`) is organized into **4 interactive tabs**:

### 🏭 Tab 1 — Factory Simulator
- Predicts lead time for each product-region combination using the trained ML model
- Grouped bar chart of **Lead Time Predictions by Product & Region**
- Donut chart of **Sales by Division** (Chocolate, Sugar, Other)
- Stacked bar chart of **Operational Cost by Division**
- Scatter plot — **Sales vs. Gross Profit** (bubble size = Units sold)

### ⚖️ Tab 2 — What-If Analysis
- Four dynamic **KPI cards** with sparkbar trends:
  - **Lead Time Reduction %** — operational gain vs. current average
  - **Profit Impact Stability %** — items maintaining healthy margins
  - **Scenario Confidence Score %** — reliability based on prediction variance
  - **Recommendation Coverage %** — % of total inventory currently in filter
- **Funnel chart** — Actual vs. Optimized lead time comparison
- **Overlapping histogram** — distribution of actual vs. predicted lead times

### 📋 Tab 3 — Recommendations
- Products ranked by a **composite optimization score** combining:
  - Gross Profit weight `(1 - priority)`
  - Lead Time speed weight `(priority)`
- Adjustable via the **Priority Slider** (Profit ← → Speed)
- Top 10 scored routes visualized in a bar chart
- Full sortable, color-gradient ranked table
- **📩 Download** full optimization report as CSV

### 🚨 Tab 4 — Risk & Impact
- **Financial Safeguards** — flags items significantly below average profit margins
- **Operational Risk flags** — scenarios exceeding the 10-day lead time threshold
- **Risk Landscape Scatter** — Lead Time vs. Gross Profit per region, with risk zone overlays

### Sidebar Controls
- Filter by **Products**, **Regions**, and **Ship Modes**
- Adjust **Profit ↔ Speed priority** slider for recommendation scoring

---

## 📊 Dataset Description

### `Nassau Candy Distributor.csv` — Raw Dataset
**10,194 rows × 18 columns** | Coverage: United States & Canada | Date Range: 2025

| Column | Description |
|---|---|
| `Row ID` | Unique row identifier |
| `Order ID` | Unique order identifier |
| `Order Date` | Date the order was placed |
| `Ship Date` | Date the order was shipped |
| `Ship Mode` | Shipping method: `Standard Class`, `Second Class`, `First Class`, `Same Day` |
| `Customer ID` | Customer identifier |
| `Country/Region` | `United States` or `Canada` |
| `City` | Destination city |
| `State/Province` | Destination state or province |
| `Postal Code` | Destination postal code |
| `Division` | Product category: `Chocolate`, `Sugar`, `Other` |
| `Region` | Sales region: `Interior`, `Atlantic`, `Gulf`, `Pacific` |
| `Product ID` | Product SKU |
| `Product Name` | Product name (e.g., *Wonka Bar - Milk Chocolate*) — **15 unique products** |
| `Sales` | Revenue in USD |
| `Units` | Quantity of units sold |
| `Gross Profit` | Gross profit in USD |
| `Cost` | Cost of goods in USD |

---

### `NFD_Cleand.csv` — Cleaned Dataset
**9,881 rows × 18 columns** — processed version of the raw data with the engineered `lead_time` column added.

| Additional Column | Description |
|---|---|
| `lead_time` | Days between `Order Date` and `Ship Date` (engineered feature) |

---

## 📁 Repository Structure

```
Factory-Reallocation-Shipping-Optimization.../
│
├── Nassau Candy Distributor.csv    # Raw transactional dataset (10,194 rows)
├── NFD_Cleand.csv                  # Cleaned dataset with lead_time column (9,881 rows)
├── Final Data Process.ipynb        # Full ML pipeline — EDA, preprocessing, model training
├── data_scaler.pkl.gz              # Trained Random Forest Regressor model (compressed)
├── app.py                          # Streamlit dashboard application
├── logo.png                        # Nassau Candy Distributor brand logo
├── Professional_Research_Paper.pdf # Research paper documenting methodology & findings
├── requirements.txt                # Python dependencies
├── LICENSE                         # MIT License
└── README.md
```

---

## 🤖 Machine Learning Model

**Model:** `RandomForestRegressor` &nbsp;|&nbsp; **Saved as:** `data_scaler.pkl.gz`

### Target Variable
- `lead_time` — number of days between order placement and shipment

### Models Compared During Training

| Model | Notes |
|---|---|
| Linear Regression | Baseline |
| **Random Forest Regressor** ✅ | **Selected — best R² with OOB validation enabled** |
| Gradient Boosting Regressor | Evaluated, not selected |


---

## 🔄 Data Processing Pipeline

Fully documented in `Final Data Process.ipynb`:

1. **Load** — Read `Nassau Candy Distributor.csv`
2. **Handle Missing Values** — Fill missing `Postal Code` with column mode
3. **Drop Columns** — Remove `Row ID`
4. **Parse Dates** — Convert `Order Date` and `Ship Date` to `datetime64`
5. **Remove Duplicates** — Drop duplicate rows (10,194 → 9,881 rows)
6. **Feature Engineering** — Compute `lead_time = Ship Date − Order Date` (days)
7. **Export** — Save cleaned data to `NFD_Cleand.csv`
8. **Label Encoding** — Encode: `Ship Mode`, `Region`, `Division`, `Product Name`, `Country/Region`, `City`, `State/Province`
9. **Standard Scaling** — Scale: `Sales`, `Units`, `Cost`, `Gross Profit`
10. **Outlier Clipping** — Clip `lead_time` at the 5th percentile (lower bound)
11. **Model Training** — Compare Linear Regression, Random Forest, Gradient Boosting
12. **Model Export** — Serialize best model via `joblib` as `data_scaler.pkl.gz`

---

## 🛠 Technologies Used

| Library | Purpose |
|---|---|
| `streamlit` | Interactive web dashboard |
| `pandas` | Data manipulation & cleaning |
| `numpy` | Numerical operations |
| `scikit-learn` | ML model training, encoding, scaling |
| `plotly` | Interactive charts & visualizations |
| `matplotlib` | EDA plots in notebook |
| `seaborn` | Statistical plots (boxplots) in notebook |
| `joblib` | Model serialization and loading |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/vm17-lab/Factory-Reallocation-Shipping-Optimization-Recommendation-System-for-Nassau-Candy-Distributor.git
cd Factory-Reallocation-Shipping-Optimization-Recommendation-System-for-Nassau-Candy-Distributor
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App
```bash
streamlit run app.py
```
The dashboard will open at `http://localhost:8501`

### 5. (Optional) Explore the ML Notebook
```bash
jupyter notebook "Final Data Process.ipynb"
```

---

## 📈 Key Insights

- 🍫 **Three product divisions** — Chocolate, Sugar, Other — across 4 regional zones: Interior, Atlantic, Gulf, Pacific
- 🚚 **Four shipping modes** — Standard Class, Second Class, First Class, Same Day
- 🌎 **Two countries** — United States and Canada
- 🎯 **15 unique candy products** tracked (including multiple Wonka Bar variants)
- 📦 **9,881 cleaned orders** used for model training after duplicate removal
- ⚡ Priority-weighted recommendations let users optimize for **profit** or **speed** via a real-time slider
- 🚨 Automatic risk alerts flag routes exceeding 10-day lead time or products below 50% of average profit margin
- 📩 Full ranked optimization report downloadable as CSV directly from the dashboard

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

> ⭐ If you found this project useful, consider giving it a star on [GitHub](https://github.com/vm17-lab/Factory-Reallocation-Shipping-Optimization-Recommendation-System-for-Nassau-Candy-Distributor)!
