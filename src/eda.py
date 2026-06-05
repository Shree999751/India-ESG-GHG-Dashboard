"""
eda.py

Exploratory Data Analysis for India ESG/GHG Emissions.
Generates statistical summaries, correlations, and trend analyses.

Usage:
    python src/eda.py

Outputs:
    reports/eda_summary.txt   - Text summary of findings
    reports/statistics.json    - Descriptive statistics
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# ── LOAD CLEAN DATA ─────────────────────────────────────
INPUT = Path("data/processed/india_ghg_clean.csv")
df = pd.read_csv(INPUT)

print("=" * 60)
print("  EXPLORATORY DATA ANALYSIS")
print("=" * 60)

results = []

# ── 1. DESCRIPTIVE STATISTICS ──────────────────────────
print("\n--- Descriptive Statistics ---")
desc = df.describe()
print(desc[['co2', 'total_ghg', 'co2_per_capita', 'gdp']].to_string())

results.append("=== 1. DESCRIPTIVE STATISTICS ===")
results.append(f"CO2 emissions: mean={df['co2'].mean():.1f}, std={df['co2'].std():.1f}")
results.append(f"Total GHG: mean={df['total_ghg'].mean():.1f}, std={df['total_ghg'].std():.1f}")
results.append(f"CO2 per capita: mean={df['co2_per_capita'].mean():.3f}")
results.append(f"GDP (billions): mean={df['gdp'].mean()/1e9:.1f}B")

# ── 2. TREND ANALYSIS ───────────────────────────────────
print("\n--- Trend Analysis ---")
co2_2000, co2_2024 = df[df['year'] == 2000]['co2'].values[0], df[df['year'] == 2024]['co2'].values[0]
growth = ((co2_2024 / co2_2000) ** (1/24) - 1) * 100

results.append(f"\n=== 2. TREND ANALYSIS ===")
results.append(f"CO2 in 2000: {co2_2000:.1f} Mt")
results.append(f"CO2 in 2024: {co2_2024:.1f} Mt")
results.append(f"CAGR (Compound Annual Growth Rate): {growth:.2f}%")

# Period-wise growth
periods = {
    '2000-2005': (2000, 2005),
    '2005-2010': (2005, 2010),
    '2010-2015': (2010, 2015),
    '2015-2020': (2015, 2020),
    '2020-2024': (2020, 2024)
}

print("\nPeriod-wise CO2 Growth:")
for period, (start, end) in periods.items():
    v1 = df[df['year'] == start]['co2'].values[0]
    v2 = df[df['year'] == end]['co2'].values[0]
    cagr = ((v2/v1)**(1/(end-start)) - 1) * 100
    print(f"  {period}: {cagr:+.2f}% CAGR")

# ── 3. SOURCE BREAKDOWN ANALYSIS ────────────────────────
print("\n--- Source Breakdown (2024) ---")
last = df[df['year'] == 2024].iloc[0]
sources = {'Coal': last['coal_co2'], 'Oil': last['oil_co2'],
           'Gas': last['gas_co2'], 'Cement': last['cement_co2']}
for source, value in sources.items():
    pct = (value / last['co2']) * 100
    print(f"  {source}: {value:.1f} Mt ({pct:.1f}%)")

# Coal share evolution
df['coal_pct'] = (df['coal_co2'] / df['co2']) * 100
coal_2000 = df[df['year'] == 2000]['coal_pct'].values[0]
coal_2024 = df[df['year'] == 2024]['coal_pct'].values[0]
print(f"\nCoal share: {coal_2000:.1f}% (2000) → {coal_2024:.1f}% (2024)")

results.append(f"\n=== 3. SOURCE BREAKDOWN ===")
results.append(f"Coal dominance: {coal_2024:.1f}% of total CO2 in 2024")
results.append(f"Coal share change: {coal_2024 - coal_2000:+.1f} percentage points since 2000")

# ── 4. CORRELATION ANALYSIS ─────────────────────────────
print("\n--- Correlation Matrix (Key Variables) ---")
cols = ['co2', 'coal_co2', 'oil_co2', 'gas_co2', 'cement_co2',
        'co2_per_capita', 'total_ghg', 'gdp', 'primary_energy_consumption']
corr = df[cols].corr()
print(corr['co2'].sort_values(ascending=False).to_string())

# Strongest correlations with total CO2
co2_corr = corr['co2'].drop('co2').sort_values(ascending=False)
results.append(f"\n=== 4. CORRELATION WITH TOTAL CO2 ===")
for var, val in co2_corr.head(5).items():
    results.append(f"{var}: r = {val:.3f}")

# ── 5. PER CAPITA ANALYSIS ──────────────────────────────
print("\n--- Per Capita & GDP Intensity ---")
df['gdp_billion'] = df['gdp'] / 1e9
df['co2_per_gdp'] = (df['co2'] / df['gdp_billion']) * 1000  # kg CO2 per $1000 GDP

pcap_2000 = df[df['year'] == 2000]['co2_per_capita'].values[0]
pcap_2024 = df[df['year'] == 2024]['co2_per_capita'].values[0]
print(f"Per capita CO2: {pcap_2000:.2f} (2000) → {pcap_2024:.2f} (2024)")
print(f"Change: +{((pcap_2024/pcap_2000)-1)*100:.1f}%")

intensity_2000 = df[df['year'] == 2000]['co2_per_gdp'].values[0]
intensity_2024 = df[df['year'] == 2024]['co2_per_gdp'].values[0]
print(f"CO2 intensity: {intensity_2000:.2f} (2000) → {intensity_2024:.2f} (2024) kg/$1000GDP")
print(f"Intensity improvement: {((intensity_2000/intensity_2024)-1)*100:.1f}%")

results.append(f"\n=== 5. EFFICIENCY METRICS ===")
results.append(f"CO2 per capita growth: +{((pcap_2024/pcap_2000)-1)*100:.1f}%")
results.append(f"Carbon intensity improvement: {((intensity_2000/intensity_2024)-1)*100:.1f}%")

# ── 6. GHG COMPOSITION ──────────────────────────────────
print("\n--- GHG Composition (2024) ---")
last_row = df.iloc[-1]
total = last_row['total_ghg']
co2_only = last_row['co2']
ch4 = last_row['methane']
n2o = last_row['nitrous_oxide']

print(f"  CO2: {co2_only:.1f} Mt ({co2_only/total*100:.1f}%)")
print(f"  Methane (CO2e): {ch4:.1f} Mt ({ch4/total*100:.1f}%)")
print(f"  N2O (CO2e): {n2o:.1f} Mt ({n2o/total*100:.1f}%)")

results.append(f"\n=== 6. GHG COMPOSITION (2024) ===")
results.append(f"Total GHG: {total:.1f} MtCO2e")
results.append(f"CO2: {co2_only/total*100:.1f}% | Methane: {ch4/total*100:.1f}% | N2O: {n2o/total*100:.1f}%")

# Save
with open("reports/eda_summary.txt", "w") as f:
    f.write("\n".join(results))
print("\n  EDA summary saved to: reports/eda_summary.txt")

# Statistics JSON
stats = {
    "records": len(df),
    "year_range": f"{int(df['year'].min())}-{int(df['year'].max())}",
    "co2_cagr_2000_2024": growth,
    "coal_share_2024": float(coal_2024),
    "co2_per_capita_2024": float(pcap_2024),
    "carbon_intensity_2024": float(intensity_2024),
    "total_ghg_2024": float(total)
}
with open("reports/statistics.json", "w") as f:
    json.dump(stats, f, indent=2)

print("\n" + "=" * 60)
print("  EDA COMPLETE")
print("=" * 60)
