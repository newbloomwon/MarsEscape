#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3 -m pip install -r requirements-dev.txt
python3 -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "EscapeFromMars" \
  main.py

echo "Standalone build complete: dist/EscapeFromMars.app"
