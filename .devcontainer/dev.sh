#!/bin/bash
set -e

echo "=== Setting up 8085-mP Dev Environment ==="

# Python setup
echo ">>> Setting up Python environment..."
cd Backend

# Remove old/broken venv if it exists
if [ -d ".venv" ]; then
    echo "Removing existing .venv (may be from different Python version)..."
    rm -rf .venv
fi

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Node setup
echo ">>> Setting up Node.js environment..."
cd ..
npm ci

echo "=== Setup Complete ==="
echo "Python venv: Backend/.venv (activate with: source Backend/.venv/bin/activate)"
echo "To run: python -m Server & npm run tauri dev"
