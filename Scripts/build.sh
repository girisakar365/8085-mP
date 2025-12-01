#!/usr/bin/env bash
set -e

# ---------------------
#  CONFIG
# ---------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate to the project root (parent of Scripts folder)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
# Navigate to Backend folder
BACKEND_DIR="$PROJECT_ROOT/Backend"
RESOURCES_DIR="$PROJECT_ROOT/src-tauri/resources"

ENTRY_POINT="Server"
OUTPUT_DIR="dist"

# Clean old builds
rm -rf "$BACKEND_DIR/$OUTPUT_DIR" "$BACKEND_DIR/build" "$BACKEND_DIR"/*.dist "$BACKEND_DIR"/*.build 2> /dev/null || true

echo "🔨 Building backend using Nuitka (onefile)..."

cd "$BACKEND_DIR"

python3 -m nuitka \
  --standalone \
  --onefile \
  --follow-imports \
  --enable-plugin=no-qt \
  --python-flag=-m \
  --include-data-files=M8085/commands_property.yml=M8085/commands_property.yml \
  --output-dir=${OUTPUT_DIR} \
  $ENTRY_POINT

cd "$PROJECT_ROOT"

echo "🎉 Build complete!"
echo "➡️ Binary is inside the folder: $BACKEND_DIR/$OUTPUT_DIR/"

# Create resources directory
mkdir -p "$RESOURCES_DIR"

# Copy the server binary to resources
echo "📦 Copying server binary to resources..."
cp "$BACKEND_DIR/$OUTPUT_DIR/Server.bin" "$RESOURCES_DIR/server"

# Ensure execute permissions
chmod +x "$RESOURCES_DIR/server"

echo "✅ Server binary copied to: $RESOURCES_DIR/server"

# Verify the binary
if [ -x "$RESOURCES_DIR/server" ]; then
    echo "✓ Server binary is executable"
else
    echo "✗ Warning: Server binary may not be executable"
fi

echo ""
echo "🚀 Next steps:"
echo "   Run 'npm run tauri build' to create the bundled application"