#!/usr/bin/env bash
set -euo pipefail

# Always run from the project root, even if script is clicked from elsewhere
cd "$(dirname "$0")/.."

echo "Setting up Python virtual environment..."

# Create virtual environment if it does not already exist
if [[ ! -d ".venv" ]]; then
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install / update dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Running coral bleaching analysis pipeline..."

python scripts/run_analysis.py

echo "Pipeline complete."
echo "Figures saved to: outputs/figures/"
echo "Tables saved to: outputs/tables/"
echo "Reports saved to: outputs/reports/"