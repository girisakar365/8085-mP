#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the project root (parent of Scripts folder)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
# Navigate to Backend folder
BACKEND_DIR="$PROJECT_ROOT/Backend"

cd "$BACKEND_DIR" || { echo "Failed to navigate to Backend directory"; exit 1; }

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt