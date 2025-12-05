#!/usr/bin/env bash
set -e

# ---------------------
#  CONFIG
# ---------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/Backend"
RESOURCES_DIR="$PROJECT_ROOT/src-tauri/resources"

ENTRY_POINT="Server"
OUTPUT_DIR="dist"

echo "================================================"
echo "  8085 Microprocessor Simulator - Backend Build Script"
echo "================================================"
echo ""
echo "Project Root: $PROJECT_ROOT"
echo "Backend Dir:  $BACKEND_DIR"
echo "Resources:    $RESOURCES_DIR"
echo ""

# Clean old builds
echo "🧹 Cleaning old builds..."
rm -rf "$BACKEND_DIR/$OUTPUT_DIR" "$BACKEND_DIR/build" "$BACKEND_DIR"/*.dist "$BACKEND_DIR"/*.build 2> /dev/null || true

echo "🔨 Building backend using Nuitka (onefile)..."
echo ""

cd "$BACKEND_DIR"

# Check if Nuitka is installed
if ! python3 -m nuitka --version > /dev/null 2>&1; then
    echo "❌ Error: Nuitka is not installed."
    echo "   Install it with: pip install nuitka"
    exit 1
fi

# Check for required system dependencies
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! command -v patchelf &> /dev/null; then
        echo "❌ Error: patchelf is not installed."
        echo "   Install it with: sudo apt-get install patchelf"
        exit 1
    fi
fi

# Build with Nuitka
python3 -m nuitka \
  --standalone \
  --onefile \
  --follow-imports \
  --enable-plugin=no-qt \
  --python-flag=-m \
  --assume-yes-for-downloads \
  --include-data-files=M8085/commands_property.yml=M8085/commands_property.yml \
  --include-data-files=M8085/docs.yml=M8085/docs.yml \
  --output-dir=${OUTPUT_DIR} \
  $ENTRY_POINT

cd "$PROJECT_ROOT"

echo ""
echo "🎉 Nuitka build complete!"
echo ""

# Create resources directory
mkdir -p "$RESOURCES_DIR/backend"

# Copy the server binary to resources
echo "📦 Copying server binary to resources..."

# Detect OS and set correct binary name
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    SOURCE_BINARY="$BACKEND_DIR/$OUTPUT_DIR/Server.exe"
    DEST_BINARY="$RESOURCES_DIR/backend/server.exe"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    SOURCE_BINARY="$BACKEND_DIR/$OUTPUT_DIR/Server.bin"
    DEST_BINARY="$RESOURCES_DIR/backend/server"
else
    SOURCE_BINARY="$BACKEND_DIR/$OUTPUT_DIR/Server.bin"
    DEST_BINARY="$RESOURCES_DIR/backend/server"
fi

# Check if source binary exists
if [ ! -f "$SOURCE_BINARY" ]; then
    echo "❌ Error: Binary not found at $SOURCE_BINARY"
    echo "   Looking for alternatives..."
    ls -la "$BACKEND_DIR/$OUTPUT_DIR/" 2>/dev/null || echo "   Output directory does not exist"
    exit 1
fi

# Copy and set permissions
cp "$SOURCE_BINARY" "$DEST_BINARY"
chmod +x "$DEST_BINARY"

echo "✅ Server binary copied to: $DEST_BINARY"

# Verify the binary
if [ -x "$DEST_BINARY" ]; then
    echo "✓ Server binary is executable"
    # Show binary size
    SIZE=$(du -h "$DEST_BINARY" | cut -f1)
    echo "✓ Binary size: $SIZE"
else
    echo "⚠️  Warning: Server binary may not be executable"
fi

echo ""
echo "================================================"
echo "  Build Summary"
echo "================================================"
echo ""
echo "Backend binary:  $DEST_BINARY"
echo "Resources dir:   $RESOURCES_DIR/backend/"
echo ""
echo "🚀 Next steps:"
echo "   1. Run 'npm run tauri build' to create the bundled application"
echo "   2. Find output in src-tauri/target/release/bundle/"
echo ""
echo "📝 For development, run:"
echo "   - Backend: ./src-tauri/resources/backend/server"
echo "   - Frontend: npm run dev"
echo "   - Tauri:    npm run tauri dev"
echo ""