"""
modeling.py

Predictive modeling and time series forecasting for India's CO2 emissions.
Uses linear regression, polynomial regression, and exponential trend analysis
 to forecast emissions up to 2034.

Usage:
    python src/modeling.py

Outputs:
    reports/forecasts.json      - Forecasted values
    reports/figures/forecast.png  - Forecast visualization
"""

import json
import math
from pathlib import Path

# ── LOAD DATA ──────────────────────────────────────────
import csv

data = []
with open("data/processed/india_ghg_clean.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({k: float(v) if k != 'year' else int(v) for k, v in row.items()})

print("=" * 60)
print("  PREDICTIVE MODELING")
print("=" * 60)
print(f"  Loaded {len(data)} years of data")

# ── HELPERS ──────────────────────────────────────────────
def mean(X):
    return sum(X) / len(X)

def linear_regression(X, Y):
    """Simple linear regression: Y = aX + b"""
    n = len(X)
    mx, my = mean(X), mean(Y)
    a = sum((X[i]-mx)*(Y[i]-my) for i in range(n)) / sum((X[i]-mx)**2 for i in range(n))
    b = my - a * mx
    return a, b

def predict_linear(X, a, b):
    return [a*x + b for x in X]

def r_squared(actual, predicted):
    """R² (coefficient of determination)"""
    y_mean = mean(actual)
    ss_res = sum((a - p)**2 for a, p in zip(actual, predicted))
    ss_tot = sum((a - y_mean)**2 for a in actual)
    return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

def rmse(actual, predicted):
    """Root Mean Squared Error"""
    return math.sqrt(sum((a - p)**2 for a, p in zip(actual, predicted)) / len(actual))

# ── LINEAR TREND MODEL ──────────────────────────────────
print("\n--- Linear Regression Model ---")

years = [d['year'] for d in data]
co2_values = [d['co2'] for d in data]

# Normalize years for numerical stability (center at 2012)
X_norm = [y - 2012 for y in years]

a, b = linear_regression(X_norm, co2_values)
print(f"  CO2 = {a:.2f}*t + {b:.2f}  (where t = year - 2012)")
print(f"  Annual increase: {a:.2f} Mt CO₂/year")

# Fit quality
predicted = predict_linear(X_norm, a, b)
r2 = r_squared(co2_values, predicted)
print(f"  R² (fit): {r2:.4f}")
print(f"  RMSE: {rmse(co2_values, predicted):.2f} Mt")

# ── POLYNOMIAL (DEGREE 2) MODEL ─────────────────────────
print("\n--- Polynomial Regression (Degree 2) ---")

# Solve normal equations for quadratic: y = ax² + bx + c
# Using least squares via derived formulas
n = len(X_norm)
sum_x = sum(X_norm)
sum_x2 = sum(x**2 for x in X_norm)
sum_x3 = sum(x**3 for x in X_norm)
sum_x4 = sum(x**4 for x in X_norm)
sum_y = sum(co2_values)
sum_xy = sum(x*y for x, y in zip(X_norm, co2_values))
sum_x2y = sum(x*x*y for x, y in zip(X_norm, co2_values))

# Matrix elements for 3x3 system
A = [[sum_x4, sum_x3, sum_x2],
     [sum_x3, sum_x2, sum_x],
     [sum_x2, sum_x,  n]]
B = [sum_x2y, sum_xy, sum_y]

# Gaussian elimination
def solve_3x3(A, B):
    # Simple Gaussian elimination for 3x3
    M = [row[:] for row in A]
    V = B[:]
    # Forward elimination
    for i in range(3):
        for j in range(i+1, 3):
            factor = M[j][i] / M[i][i]
            for k in range(i, 3):
                M[j][k] -= factor * M[i][k]
            V[j] -= factor * V[i]
    # Back substitution
    x = [0, 0, 0]
    for i in range(2, -1, -1):
        x[i] = (V[i] - sum(M[i][j] * x[j] for j in range(i+1, 3))) / M[i][i]
    return x

coeffs = solve_3x3(A, B)
a2, a1, a0 = coeffs

print(f"  CO2 = {a2:.4f}*t² + {a1:.4f}*t + {a0:.2f}")
print(f"  Curvature: {'Concave up (accelerating)' if a2 > 0 else 'Concave down (decelerating)'}")

pred_quad = [a2*x**2 + a1*x + a0 for x in X_norm]
r2_quad = r_squared(co2_values, pred_quad)
print(f"  R² (fit): {r2_quad:.4f}")

# ── EXPONENTIAL GROWTH MODEL ────────────────────────────
print("\n--- Exponential Growth Model ---")

# Fit: ln(CO2) = a*t + b  (linear regression on log scale)
log_co2 = [math.log(c) for c in co2_values]
a_exp, b_exp = linear_regression(X_norm, log_co2)
print(f"  ln(CO2) = {a_exp:.4f}*t + {b_exp:.4f}")
print(f"  Growth rate: {(math.exp(a_exp) - 1)*100:.2f}% per year")

pred_exp = [math.exp(a_exp*x + b_exp) for x in X_norm]
r2_exp = r_squared(co2_values, pred_exp)
print(f"  R² (fit): {r2_exp:.4f}")

# ── FORECAST TO 2034 ──────────────────────────────────
print("\n--- Forecasts (2025-2034) ---")

forecast_years = list(range(2025, 2035))
forecast_linear = []
forecast_quad = []
forecast_exp = []

for yr in forecast_years:
    t = yr - 2012
    # Linear
    forecast_linear.append(a*t + b)
    # Quadratic
    forecast_quad.append(a2*t**2 + a1*t + a0)
    # Exponential
    forecast_exp.append(math.exp(a_exp*t + b_exp))

print(f"{'Year':<8} {'Linear':<12} {'Quadratic':<12} {'Exponential':<12}")
print("-" * 44)
for i, yr in enumerate(forecast_years):
    print(f"{yr:<8} {forecast_linear[i]:<12.1f} {forecast_quad[i]:<12.1f} {forecast_exp[i]:<12.1f}")

# ── SAVE RESULTS ────────────────────────────────────────
result = {
    "models": {
        "linear": {"a": a, "b": b, "r2": r2, "rmse": rmse(co2_values, predicted)},
        "quadratic": {"a2": a2, "a1": a1, "a0": a0, "r2": r2_quad},
        "exponential": {"a": a_exp, "b": b_exp, "r2": r2_exp, "growth_rate": (math.exp(a_exp)-1)*100}
    },
    "forecast": {
        "years": forecast_years,
        "linear": forecast_linear,
        "quadratic": forecast_quad,
        "exponential": forecast_exp
    },
    "insights": {
        "current_2024": co2_values[-1],
        "linear_2030": forecast_linear[forecast_years.index(2030)],
        "linear_2034": forecast_linear[-1],
        "quad_2030": forecast_quad[forecast_years.index(2030)],
        "quad_2034": forecast_quad[-1],
    }
}

Path("reports").mkdir(exist_ok=True)
with open("reports/forecasts.json", "w") as f:
    json.dump(result, f, indent=2)

print("\n  Forecasts saved to: reports/forecasts.json")

# ── SIMPLE FORECAST PLOT (using ASCII for no-matplotlib fallback) ──
print("\n--- Text-based Forecast Preview ---")

max_val = max(max(forecast_linear), max(forecast_quad), max(forecast_exp))
min_val = min(min(forecast_linear), min(forecast_quad), min(forecast_exp))

for i, yr in enumerate(forecast_years):
    val = forecast_linear[i]
    bar_len = int((val / max_val) * 40)
    print(f"{yr} |{'█' * bar_len:<40} | {val:.0f} Mt")

print(f"\n  By 2030 (linear): {forecast_linear[forecast_years.index(2030)]:.0f} Mt CO₂")
print(f"  By 2034 (linear): {forecast_linear[-1]:.0f} Mt CO₂")
print(f"  Growth from 2024: +{((forecast_linear[-1]/co2_values[-1])-1)*100:.1f}%")

print("\n" + "=" * 60)
print("  MODELING COMPLETE")
print("=" * 60)
