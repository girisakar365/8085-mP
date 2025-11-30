#!/bin/bash

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the project root (parent of Scripts folder)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
# Backend folder
BACKEND_DIR="$PROJECT_ROOT/Backend"

echo "=========================================="
echo "   8085 ASM Studio - Development Setup   "
echo "=========================================="

# ----- Pre-flight checks -----
echo ""
echo "[1/6] Running pre-flight checks..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed"
    exit 1
fi
echo "  ✓ python3 found: $(python3 --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    exit 1
fi
echo "  ✓ npm found: $(npm --version)"

# Check if cargo (Rust) is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ Error: Rust/Cargo is not installed"
    echo "  Install Rust from: https://rustup.rs/"
    exit 1
fi
echo "  ✓ cargo found: $(cargo --version)"

# Check if tauri-cli is available (optional but recommended)
if ! command -v cargo-tauri &> /dev/null && ! cargo tauri --version &> /dev/null 2>&1; then
    echo "  ⚠ Warning: tauri-cli not found globally, will use npx @tauri-apps/cli"
fi

# Check if project root exists
if [ ! -d "$PROJECT_ROOT" ]; then
    echo "❌ Error: Project root directory not found: $PROJECT_ROOT"
    exit 1
fi
echo "  ✓ Project root found: $PROJECT_ROOT"

# Check if Backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Error: Backend directory not found: $BACKEND_DIR"
    exit 1
fi
echo "  ✓ Backend directory found"

# Check if package.json exists
if [ ! -f "$PROJECT_ROOT/package.json" ]; then
    echo "❌ Error: package.json not found in project root"
    exit 1
fi
echo "  ✓ package.json found"

# Check if requirements.txt exists
if [ ! -f "$BACKEND_DIR/requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found in Backend directory"
    exit 1
fi
echo "  ✓ requirements.txt found"

# ----- Backend Setup -----
echo ""
echo "[2/6] Setting up Python virtual environment..."
cd "$BACKEND_DIR" || { echo "❌ Failed to navigate to Backend directory"; exit 1; }

if [ ! -d ".venv" ]; then
    python3 -m venv .venv || { echo "❌ Failed to create virtual environment"; exit 1; }
    echo "  ✓ Virtual environment created"
else
    echo "  ✓ Virtual environment already exists"
fi

echo ""
echo "[3/6] Activating virtual environment..."
source .venv/bin/activate || { echo "❌ Failed to activate virtual environment"; exit 1; }
echo "  ✓ Virtual environment activated"

echo ""
echo "[4/6] Installing Python dependencies..."
pip install --upgrade pip -q || { echo "❌ Failed to upgrade pip"; exit 1; }
pip install -r requirements.txt -q || { echo "❌ Failed to install Python dependencies"; exit 1; }
echo "  ✓ Python dependencies installed"

# ----- Frontend Setup -----
echo ""
echo "[5/6] Setting up Frontend..."
cd "$PROJECT_ROOT" || { echo "❌ Failed to navigate to project directory"; exit 1; }

npm ci || { echo "❌ Failed to install npm dependencies"; exit 1; }
echo "  ✓ npm dependencies installed"

# ----- Done -----
echo ""
echo "[6/6] Setup complete!"
echo ""
echo "=========================================="
echo "   Ready to develop! 🚀                  "
echo "=========================================="
echo ""
