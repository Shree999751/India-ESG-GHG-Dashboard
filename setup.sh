#!/bin/bash
# setup.sh - One-command setup for the India ESG/GHG Data Science Project

echo "=============================================="
echo "  India ESG/GHG Data Science Project Setup"
echo "=============================================="
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "⚠ pip not found. Trying to install..."
    python3 -m ensurepip --upgrade 2>/dev/null || {
        echo "❌ Could not install pip. Try: sudo apt-get install python3-pip (Linux)"
        echo "   or download from https://bootstrap.pypa.io/get-pip.py"
        exit 1
    }
fi

echo "✓ pip found"

# Install dependencies
echo
echo "--- Installing dependencies ---"
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install packages. Try: pip3 install --user -r requirements.txt"
    exit 1
fi

echo "✓ Dependencies installed"

# Run the pipeline
echo
echo "--- Running Data Science Pipeline ---"
python3 src/data_cleaning.py
python3 src/eda.py
python3 src/modeling.py
python3 src/visualization.py

echo
echo "=============================================="
echo "  Setup Complete!"
echo "=============================================="
echo
echo "Project structure:"
echo "  data/raw/          - Raw data (CSV)"
echo "  data/processed/    - Cleaned data"
echo "  src/               - Python scripts"
echo "  reports/           - Analysis outputs"
echo "  notebooks/         - Jupyter notebooks (optional)"
echo
echo "To view the interactive dashboard:"
echo "  open index.html  (or double-click it)"
echo
echo "To explore interactively:"
echo "  jupyter notebook notebooks/"
echo
