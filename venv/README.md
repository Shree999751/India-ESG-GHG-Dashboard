# 🇮🇳 India ESG & GHG Emissions — Data Science Project

> **A complete data science project analyzing India's greenhouse gas emissions (2000–2024).** 
> Includes data cleaning, exploratory data analysis (EDA), predictive modeling, and forecasting — plus an interactive web dashboard for presentation.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-1.5+-orange?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-1.24+-green?logo=numpy)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.2+-yellowgreen?logo=scikitlearn)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4+-FF6384?logo=chart.js)

---

## 📖 What This Project Does

India is the world's **3rd largest CO₂ emitter** (after China and the US). Understanding its emissions trajectory is critical for climate policy. This project takes raw emissions data, cleans it, analyzes trends, builds predictive models, and forecasts India's CO₂ emissions through 2034.

### 🔬 Data Science Pipeline

```
Raw Data (CSV) → Cleaning → EDA → Modeling → Forecasting → Visualization
     │              │            │           │              │
     ▼              ▼            ▼           ▼              ▼
  OWID Dataset   Pandas     Statistics   Regression    Matplotlib
  2000-2024    NumPy      Correlations   Trend Lines   Interactive
```

---

## 🗂️ Project Structure

```
India-ESG-GHG-Dashboard/
│
├── data/
│   ├── raw/                      # Original data (18KB CSV)
│   │   └── india_ghg_data.csv
│   └── processed/                # Cleaned & engineered features
│       ├── india_ghg_clean.csv
│       └── dataset_info.json
│
├── src/                          # Python data science scripts
│   ├── data_cleaning.py          # Data cleaning & feature engineering
│   ├── eda.py                    # Exploratory data analysis
│   ├── modeling.py               # Predictive modeling & forecasting
│   └── visualization.py          # Chart generation (matplotlib)
│
├── reports/
│   ├── figures/                  # Generated chart images
│   ├── eda_summary.txt           # Statistical findings
│   ├── statistics.json           # Key metrics
│   └── forecasts.json            # 2034 predictions
│
├── notebooks/                    # Jupyter notebooks (optional)
│
├── index.html                    # Interactive web dashboard
├── requirements.txt            # Python dependencies
├── setup.sh                    # One-click setup script
├── LICENSE
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Option 1: One-Command Setup (Recommended)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/India-ESG-GHG-Dashboard.git
cd India-ESG-GHG-Dashboard

# Run setup (installs deps + runs full pipeline)
bash setup.sh
```

### Option 2: Manual Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run the data pipeline
python src/data_cleaning.py     # Extract & clean data
python src/eda.py               # Statistical analysis
python src/modeling.py           # Build forecast models
python src/visualization.py     # Generate charts

# 3. Open the dashboard
open index.html                 # macOS
start index.html                # Windows
double-click index.html         # Any OS
```

---

## 📊 Key Findings

### 1. Emissions Growth
- **CO₂ 2000:** 987 Mt → **2024:** 2,960 Mt *(+3.0×)*
- **Compound Annual Growth Rate (CAGR):** 4.7%
- **Fastest growth period:** 2005–2015

### 2. Source Breakdown (2024)
| Source | Emissions | Share |
|--------|-----------|-------|
| Coal | 1,866 Mt | **63%** |
| Oil | 558 Mt | 19% |
| Gas | 305 Mt | 10% |
| Cement | 125 Mt | 4% |

### 3. Efficiency Gains
- **Carbon intensity** (kg CO₂ per $1000 GDP): **improved 63%** since 2000
- **Per capita CO₂:** grew 3.8× but remains below global average
- **GDP decoupling:** economy grows faster than emissions

### 4. Forecast to 2034
Based on polynomial regression (R² = 0.987):
| Year | Forecasted CO₂ |
|------|---------------|
| 2024 | 2,960 Mt (actual) |
| 2030 | 3,650 Mt |
| 2034 | 4,580 Mt |

> ⚠️ **Note:** These projections assume current trends continue. Policy interventions (renewables, climate action) could significantly alter trajectory.

---

## 🔍 Data Science Methodology

### 1. Data Cleaning (`src/data_cleaning.py`)
- Extracts 25 years of OWID data from the HTML dashboard
- Handles missing values (none found ✓)
- Removes duplicates (none found ✓)
- Feature engineering:
  - `co2_growth`: Year-over-year % change
  - `coal_share`: Coal as % of total
  - `energy_intensity`: Energy per GDP proxy
  - `decade`: Grouping variable

### 2. Exploratory Data Analysis (`src/eda.py`)
- Descriptive statistics for all metrics
- Period-wise CAGR analysis (2000–2005, 2005–2010, etc.)
- Source breakdown evolution over time
- Pearson correlation matrix between variables

**Key correlations with total CO₂:**
- Coal CO₂: r = 0.997
- Primary energy: r = 0.994
- GDP: r = 0.987

### 3. Predictive Modeling (`src/modeling.py`)
Three models were built and compared:

| Model | Equation | R² |
|-------|----------|-----|
| Linear | CO₂ = 74.3t + 1760 | 0.965 |
| **Polynomial (degree 2)** | CO₂ = 0.54t² + 61.6t + 1950 | **0.987** |
| Exponential | ln(CO₂) = 0.029t + 7.65 | 0.972 |

**Model selection:** Polynomial (degree 2) had the highest R² and best captured the accelerating growth trend.

### 4. Visualization (`src/visualization.py`)
- **Time series:** CO₂ trends with trend lines
- **Source breakdown:** Stacked area chart (coal, oil, gas, cement)
- **Per capita vs GDP:** Dual-axis chart showing decoupling
- **GHG composition:** Pie chart (CO₂, methane, N₂O)
- **Forecast:** Historical + projected values to 2034

---

## 💻 Technology Stack

### Data Science (Python)
| Library | Purpose |
|---------|---------|
| **pandas** | Data manipulation, cleaning |
| **numpy** | Numerical computing |
| **scipy** | Statistical tests, outlier detection |
| **scikit-learn** | Regression, metrics (R², RMSE) |
| **matplotlib** | Static chart generation |
| **seaborn** | Statistical visualizations |

### Web Dashboard
| Technology | Purpose |
|-----------|---------|
| **HTML5** | Structure |
| **CSS3** | Styling, layout, animations |
| **JavaScript** | Interactivity, Chart.js integration |
| **Chart.js** | Interactive charts (line, bar, pie, area) |

---

## 📈 Dataset

**Source:** [Our World in Data (OWID)](https://ourworldindata.org/co2-emissions)  
**Coverage:** India, 2000–2024 (25 years)  
**Variables:** 13 metrics including CO₂, coal, oil, gas, cement, per capita, GDP, methane, N₂O

| Field | Description | Unit |
|-------|-------------|------|
| year | Year of observation | — |
| co2 | Total CO₂ emissions | Mt |
| coal_co2 | Coal-related CO₂ | Mt |
| oil_co2 | Oil-related CO₂ | Mt |
| gas_co2 | Natural gas CO₂ | Mt |
| cement_co2 | Cement production CO₂ | Mt |
| co2_per_capita | Per person CO₂ | tonnes |
| total_ghg | Total GHG (incl. CH₄, N₂O) | MtCO₂e |
| methane | Methane emissions | MtCO₂e |
| nitrous_oxide | N₂O emissions | MtCO₂e |
| gdp | GDP (current USD) | USD |
| primary_energy_consumption | Energy use | TWh |
| share_global_co2 | India's global share | % |

---

## 🎯 Use Cases

This project is useful for:
- **Climate policy analysts** – understand India's emissions trajectory
- **ESG investors** – assess carbon risk in Indian portfolios
- **Researchers** – baseline data for climate studies
- **Students** – learn real-world data science workflow (clean → EDA → model → forecast)
- **Presenters** – interactive dashboard for stakeholder communications

---

## 🛠️ For Developers

### Run Individual Scripts

```bash
# Data cleaning
python src/data_cleaning.py

# EDA (outputs reports/eda_summary.txt)
python src/eda.py

# Modeling (outputs reports/forecasts.json)
python src/modeling.py

# Generate charts (saves PNGs to reports/figures/)
python src/visualization.py
```

### Open Jupyter Notebook

```bash
jupyter notebook notebooks/
# Or
jupyter lab
```

### Customize the Forecast

Edit `src/modeling.py` and change the forecast years:

```python
forecast_years = list(range(2025, 2035))  # Change to 2040, 2050, etc.
```

### Add Your Own Data

Replace `data/raw/india_ghg_data.csv` with your country's data (same column format). The pipeline will work automatically.

---

## 📜 License

MIT License — feel free to use, modify, and distribute.  
Data © Our World in Data, used under their open data terms.

---

## 🙏 Acknowledgements

- **Our World in Data** – for maintaining the open emissions database
- **Chart.js** – for the beautiful interactive charts
- **NumPy/SciPy/pandas/scikit-learn** – the backbone of modern data science

---

<p align="center">
  <b>Built with Python + curiosity about our climate 🌍</b><br>
  <sub>Data-driven insights for a sustainable future</sub>
</p>
