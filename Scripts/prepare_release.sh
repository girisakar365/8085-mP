#!/usr/bin/env bash
set -e

# ---------------------
# Prepare Release Files Script
# Collects all built artifacts into a single release-files directory
# ---------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default artifacts directory (can be overridden by first argument)
ARTIFACTS_DIR="${1:-$PROJECT_ROOT/artifacts}"
RELEASE_DIR="${2:-$PROJECT_ROOT/release-files}"

echo "================================================"
echo "  Preparing Release Files"
echo "================================================"
echo ""
echo "Artifacts Dir: $ARTIFACTS_DIR"
echo "Release Dir:   $RELEASE_DIR"
echo ""

# Create release directory
mkdir -p "$RELEASE_DIR"

# Find and copy all release files
echo "Collecting release artifacts..."

# Linux artifacts
find "$ARTIFACTS_DIR" -type f -name "*.deb" -exec cp {} "$RELEASE_DIR/" \; 2>/dev/null || true
find "$ARTIFACTS_DIR" -type f -name "*.rpm" -exec cp {} "$RELEASE_DIR/" \; 2>/dev/null || true
find "$ARTIFACTS_DIR" -type f -name "*.AppImage" -exec cp {} "$RELEASE_DIR/" \; 2>/dev/null || true

# Windows artifacts
find "$ARTIFACTS_DIR" -type f -name "*.msi" -exec cp {} "$RELEASE_DIR/" \; 2>/dev/null || true
find "$ARTIFACTS_DIR" -type f -name "*.exe" -exec cp {} "$RELEASE_DIR/" \; 2>/dev/null || true

# macOS artifacts
find "$ARTIFACTS_DIR" -type f -name "*.dmg" -exec cp {} "$RELEASE_DIR/" \; 2>/dev/null || true

echo ""
echo "================================================"
echo "  Release Files"
echo "================================================"
echo ""
ls -la "$RELEASE_DIR/"

FILE_COUNT=$(find "$RELEASE_DIR" -type f | wc -l)
echo ""
echo "Total files: $FILE_COUNT"
echo ""
