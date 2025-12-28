#!/usr/bin/env bash
set -euo pipefail

# Ensure jupytext exists
if ! command -v jupytext >/dev/null 2>&1; then
  echo "Error: jupytext is not installed."
  echo "Install with: pip install jupytext"
  exit 1
fi

echo "Scanning for .py files..."

find . -type f -name "*.py" \
  -not -path "*/.venv/*" \
  -not -path "*/venv/*" \
  -not -path "*/.git/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/.ipynb_checkpoints/*" \
  -print | while IFS= read -r f; do

    echo "Processing $f"

    # Pair formats (percent -> ipynb)
    jupytext --quiet --set-formats "py:percent,ipynb" "$f"

    # Create / update notebook next to it
    jupytext --quiet --to ipynb "$f"

    echo "✓ ${f%.py}.ipynb created"
done

echo "All done."
