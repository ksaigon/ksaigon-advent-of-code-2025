#!/usr/bin/env bash
set -euo pipefail

if ! command -v jupytext >/dev/null 2>&1; then
  echo "Error: jupytext is not installed."
  echo "Install with: pip install jupytext"
  exit 1
fi

echo "Scanning for day*.py files..."

find ./day?? -type f -name "day*.py" ...
  -not -path "*/.venv/*" \
  -not -path "*/venv/*" \
  -not -path "*/.git/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/.ipynb_checkpoints/*" \
  -print | while IFS= read -r f; do

    echo "Processing $f"

    # Pair percent-format .py with .ipynb
    jupytext --quiet --set-formats "py:percent,ipynb" "$f"

    # Create/update the notebook
    jupytext --quiet --to ipynb "$f"

    echo "✓ ${f%.py}.ipynb"
done

echo "All done."
