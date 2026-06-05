"""
data_cleaning.py

Loads raw India GHG emissions data, performs cleaning operations,
and exports processed data ready for analysis.

Usage:
    python src/data_cleaning.py

Outputs:
    data/processed/india_ghg_clean.csv - Cleaned dataset
    data/processed/dataset_info.json   - Metadata about the dataset
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# ── CONFIG ───────────────────────────────────────────────
RAW_CSV = Path("data/raw/india_ghg_data.csv")
OUTPUT_CSV = Path("data/processed/india_ghg_clean.csv")
OUTPUT_JSON = Path("data/processed/dataset_info.json")

print("=" * 60)
print("  INDIA ESG/GHG DATA CLEANING PIPELINE")
print("=" * 60)

# ── LOAD RAW DATA ────────────────────────────────────────
print(f"\n Loading raw data from: {RAW_CSV}")
df = pd.read_csv(RAW_CSV)
print(f"  → Loaded {len(df)} rows × {len(df.columns)} columns")

# ── BASIC INFO ──────────────────────────────────────────
print("\n--- Raw Data Info ---")
print(f"Columns: {list(df.columns)}")
print(f"Year range: {df['year'].min()} - {df['year'].max()}")
print(f"Shape: {df.shape}")
print(f"\nNull values per column:")
print(df.isnull().sum())
print(f"\nData types:")
print(df.dtypes)

# ── CLEANING OPERATIONS ─────────────────────────────────
print("\n--- Cleaning Operations ---")

# 1. No missing values expected, but handle just in case
missing_before = df.isnull().sum().sum()
if missing_before > 0:
    df = df.fillna(method='ffill')  # forward fill
    print(f"  → Forward-filled {missing_before} missing values")
else:
    print("  → No missing values found ✓")

# 2. Remove duplicates
duplicates = df.duplicated().sum()
if duplicates > 0:
    df = df.drop_duplicates()
    print(f"  → Removed {duplicates} duplicate rows")
else:
    print("  → No duplicates found ✓")

# 3. Sort by year
df = df.sort_values('year').reset_index(drop=True)
print("  → Sorted by year ✓")

# 4. Create derived features
print("\n--- Feature Engineering ---")

# Growth rates (year-over-year % change)
df['co2_growth'] = df['co2'].pct_change() * 100
df['coal_growth'] = df['coal_co2'].pct_change() * 100
df['gdp_growth'] = df['gdp'].pct_change() * 100

# Share of coal in total
df['coal_share'] = (df['coal_co2'] / df['co2']) * 100

# Energy intensity per GDP (very rough proxy)
df['energy_intensity'] = df['primary_energy_consumption'] / df['gdp'] * 1e9

# Decade grouping
df['decade'] = (df['year'] // 10) * 10

print("  → Added 'co2_growth' (YoY%)")
print("  → Added 'coal_share' (% of total)")
print("  → Added 'energy_intensity' proxy")
print("  → Added 'gdp_growth' (YoY%)")
print("  → Added 'decade' grouping")

# 5. Remove outliers (Z-score > 3 for key metrics)
from scipy import stats
print("\n--- Outlier Detection ---")
for col in ['co2_growth', 'coal_growth']:
    z = np.abs(stats.zscore(df[col].dropna()))
    outliers = (z > 3).sum()
    if outliers > 0:
        print(f"  → Found {outliers} outliers in '{col}' (Z > 3)")
    else:
        print(f"  → No outliers in '{col}' (Z > 3) ✓")

# ── SAVE CLEAN DATA ────────────────────────────────────
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)
print(f"\n Clean data saved to: {OUTPUT_CSV}")

# ── METADATA ────────────────────────────────────────────
info = {
    "title": "India ESG/GHG Emissions Dataset",
    "source": "Our World in Data (OWID)",
    "years": f"{int(df['year'].min())} - {int(df['year'].max())}",
    "total_records": len(df),
    "features": list(df.columns),
    "numeric_features": df.select_dtypes(include=[np.number]).columns.tolist(),
    "key_metrics": {
        "co2_range": [round(df['co2'].min(), 1), round(df['co2'].max(), 1)],
        "total_ghg_range": [round(df['total_ghg'].min(), 1), round(df['total_ghg'].max(), 1)],
        "co2_per_capita_range": [round(df['co2_per_capita'].min(), 3), round(df['co2_per_capita'].max(), 3)]
    }
}

with open(OUTPUT_JSON, 'w') as f:
    json.dump(info, f, indent=2)
print(f" Metadata saved to: {OUTPUT_JSON}")

# ── SUMMARY ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  CLEANING COMPLETE")
print("=" * 60)
print(f"  Rows: {len(df)}")
print(f"  Columns: {len(df.columns)}")
print(f"  Features added: co2_growth, coal_share, energy_intensity, gdp_growth, decade")
print(f"  Output: {OUTPUT_CSV}")
