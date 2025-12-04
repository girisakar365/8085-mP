# PowerShell script for building backend on Windows
# Equivalent to build.sh for Windows CI/CD

$ErrorActionPreference = "Stop"

# ---------------------
#  CONFIG
# ---------------------

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR
$BACKEND_DIR = Join-Path $PROJECT_ROOT "Backend"
$RESOURCES_DIR = Join-Path $PROJECT_ROOT "src-tauri\resources"

$ENTRY_POINT = "Server"
$OUTPUT_DIR = "dist"

Write-Host "================================================"
Write-Host "  8085 Microprocessor Simulator - Backend Build Script (Windows)"
Write-Host "================================================"
Write-Host ""
Write-Host "Project Root: $PROJECT_ROOT"
Write-Host "Backend Dir:  $BACKEND_DIR"
Write-Host "Resources:    $RESOURCES_DIR"
Write-Host ""

# Clean old builds
Write-Host "Cleaning old builds..."
$pathsToClean = @(
    (Join-Path $BACKEND_DIR $OUTPUT_DIR),
    (Join-Path $BACKEND_DIR "build"),
    (Join-Path $BACKEND_DIR "*.dist"),
    (Join-Path $BACKEND_DIR "*.build")
)
foreach ($path in $pathsToClean) {
    if (Test-Path $path) {
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Building backend using Nuitka (onefile)..."
Write-Host ""

Set-Location $BACKEND_DIR

# Check if Nuitka is installed
try {
    python -m nuitka --version | Out-Null
} catch {
    Write-Host "Error: Nuitka is not installed."
    Write-Host "   Install it with: pip install nuitka"
    exit 1
}

# Build with Nuitka
python -m nuitka `
    --standalone `
    --onefile `
    --follow-imports `
    --enable-plugin=no-qt `
    --python-flag=-m `
    --assume-yes-for-downloads `
    --include-data-files=M8085/commands_property.yml=M8085/commands_property.yml `
    --include-data-files=M8085/docs.yml=M8085/docs.yml `
    --output-dir=$OUTPUT_DIR `
    $ENTRY_POINT

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Nuitka build failed"
    exit 1
}

Set-Location $PROJECT_ROOT

Write-Host ""
Write-Host "Nuitka build complete!"
Write-Host ""

# Create resources directory
$backendResourcesDir = Join-Path $RESOURCES_DIR "backend"
if (-not (Test-Path $backendResourcesDir)) {
    New-Item -ItemType Directory -Path $backendResourcesDir -Force | Out-Null
}

# Copy the server binary to resources
Write-Host "Copying server binary to resources..."

$SOURCE_BINARY = Join-Path $BACKEND_DIR "$OUTPUT_DIR\Server.exe"
$DEST_BINARY = Join-Path $backendResourcesDir "server.exe"

# Check if source binary exists
if (-not (Test-Path $SOURCE_BINARY)) {
    Write-Host "Error: Binary not found at $SOURCE_BINARY"
    Write-Host "   Looking for alternatives..."
    Get-ChildItem -Path (Join-Path $BACKEND_DIR $OUTPUT_DIR) -ErrorAction SilentlyContinue
    exit 1
}

# Copy binary
Copy-Item -Path $SOURCE_BINARY -Destination $DEST_BINARY -Force

Write-Host "Server binary copied to: $DEST_BINARY"

# Verify the binary
if (Test-Path $DEST_BINARY) {
    $size = (Get-Item $DEST_BINARY).Length / 1MB
    Write-Host "Server binary size: $([math]::Round($size, 2)) MB"
} else {
    Write-Host "Warning: Server binary may not exist at destination"
}

Write-Host ""
Write-Host "================================================"
Write-Host "  Build Summary"
Write-Host "================================================"
Write-Host ""
Write-Host "Backend binary:  $DEST_BINARY"
Write-Host "Resources dir:   $backendResourcesDir"
Write-Host ""
Write-Host "Next steps:"
Write-Host "   1. Run 'npm run tauri build' to create the bundled application"
Write-Host "   2. Find output in src-tauri\target\release\bundle\"
Write-Host ""
