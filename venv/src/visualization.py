"""
visualization.py

Generate publication-quality charts for the India ESG/GHG analysis.
Creates: time series, source breakdown, forecasts, and correlation heatmap.

Usage:
    python src/visualization.py

Requirements: matplotlib (optional - falls back to CSV output)

Outputs:
    reports/figures/*.png - Chart images
    reports/figures/*.csv - Chart data for external tools
"""

import csv
import json
from pathlib import Path

# Try to import matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ── LOAD DATA ──────────────────────────────────────────
data = []
with open("data/processed/india_ghg_clean.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({k: float(v) if k != 'year' and k != 'decade' else int(float(v)) for k, v in row.items()})

years = [d['year'] for d in data]

Path("reports/figures").mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("  VISUALIZATION GENERATION")
print("=" * 60)

if not MATPLOTLIB_AVAILABLE:
    print("\n⚠ matplotlib not available. Generating chart data as CSV for external plotting.")
    # Export chart data as CSV for use in Excel/Tableau/etc.
    for chart_name, fields in [
        ("co2_trend", ['year', 'co2', 'total_ghg', 'co2_per_capita']),
        ("source_breakdown", ['year', 'coal_co2', 'oil_co2', 'gas_co2', 'cement_co2']),
        ("intensity", ['year', 'co2_per_capita', 'gdp'])
    ]:
        with open(f"reports/figures/{chart_name}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for d in data:
                writer.writerow({k: d[k] for k in fields})
        print(f"  → Exported {chart_name}.csv")
    print("\nOpen these CSVs in Excel to create charts.")
    print("Or install matplotlib: pip install matplotlib")
else:
    plt.style.use('seaborn-v0_8-whitegrid')

    # ── CHART 1: CO2 Time Series with Trend ─────────────────
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(years, [d['co2'] for d in data], marker='o', linewidth=2, markersize=5,
            color='#2563eb', label='Total CO₂')
    ax.fill_between(years, 0, [d['co2'] for d in data], alpha=0.1, color='#2563eb')
    ax.set_xlabel('Year', fontweight='bold')
    ax.set_ylabel('CO₂ Emissions (Mt)', fontweight='bold')
    ax.set_title('India Total CO₂ Emissions (2000-2024)', fontweight='bold', fontsize=14)
    ax.legend()
    ax.set_xlim(2000, 2024)
    plt.tight_layout()
    plt.savefig("reports/figures/co2_trend.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  ✓ reports/figures/co2_trend.png")

    # ── CHART 2: Source Breakdown (Stacked Area) ───────────
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.stackplot(years,
                 [d['coal_co2'] for d in data],
                 [d['oil_co2'] for d in data],
                 [d['gas_co2'] for d in data],
                 [d['cement_co2'] for d in data],
                 labels=['Coal', 'Oil', 'Gas', 'Cement'],
                 colors=['#ef4444', '#f59e0b', '#22c55e', '#8b5cf6'],
                 alpha=0.8)
    ax.set_xlabel('Year', fontweight='bold')
    ax.set_ylabel('CO₂ (Mt)', fontweight='bold')
    ax.set_title('CO₂ Emissions by Source', fontweight='bold', fontsize=14)
    ax.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig("reports/figures/source_breakdown.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  ✓ reports/figures/source_breakdown.png")

    # ── CHART 3: Per Capita vs GDP ────────────────────────
    fig, ax1 = plt.subplots(figsize=(10, 5))
    color1, color2 = '#2563eb', '#0d9488'
    ax1.plot(years, [d['co2_per_capita'] for d in data], color=color1, marker='o', label='CO₂/capita (t)')
    ax1.set_xlabel('Year', fontweight='bold')
    ax1.set_ylabel('CO₂ per Capita (t)', color=color1, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax2 = ax1.twinx()
    gdp_norm = [d['gdp'] / 1e12 for d in data]  # Trillions
    ax2.plot(years, gdp_norm, color=color2, marker='s', label='GDP (Trillion $)', linestyle='--')
    ax2.set_ylabel('GDP (Trillion USD)', color=color2, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color2)
    fig.suptitle('CO₂ per Capita vs GDP', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig("reports/figures/per_capita_gdp.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  ✓ reports/figures/per_capita_gdp.png")

    # ── CHART 4: GHG Composition (Latest Year) ──────────
    last = data[-1]
    labels = ['CO₂', 'Methane', 'N₂O']
    sizes = [last['co2'], last['methane'], last['nitrous_oxide']]
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                       colors=['#2563eb', '#f59e0b', '#22c55e'],
                                       startangle=90, textprops={'fontweight': 'bold'})
    ax.set_title(f'GHG Composition (2024)\nTotal: {sum(sizes):.0f} MtCO₂e', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig("reports/figures/ghg_composition.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  ✓ reports/figures/ghg_composition.png")

    # ── CHART 5: Forecast Comparison ────────────────────────
    try:
        with open("reports/forecasts.json") as f:
            forecasts = json.load(f)
        forecast_years = forecasts['forecast']['years']
        forecast_lin = forecasts['forecast']['linear']
        forecast_quad = forecasts['forecast']['quadratic']
        forecast_exp = forecasts['forecast']['exponential']

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(years, [d['co2'] for d in data], 'ko-', label='Historical', markersize=4)
        ax.plot([y for y in forecast_years], forecast_lin, 'b-', label='Linear', alpha=0.7)
        ax.plot([y for y in forecast_years], forecast_quad, 'g--', label='Quadratic', alpha=0.7)
        ax.plot([y for y in forecast_years], forecast_exp, 'r:', label='Exponential', alpha=0.7)
        ax.axvline(x=2024, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('Year', fontweight='bold')
        ax.set_ylabel('CO₂ (Mt)', fontweight='bold')
        ax.set_title('CO₂ Emissions Forecast to 2034', fontweight='bold', fontsize=14)
        ax.legend()
        plt.tight_layout()
        plt.savefig("reports/figures/forecast.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("  ✓ reports/figures/forecast.png")
    except FileNotFoundError:
        print("  ⚠ Forecast data not found. Run modeling.py first.")

print("\n" + "=" * 60)
print("  VISUALIZATION COMPLETE")
print("=" * 60)
