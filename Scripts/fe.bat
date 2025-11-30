@echo off
setlocal enabledelayedexpansion

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
:: Remove trailing backslash
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
:: Navigate to the project root (parent of Scripts folder)
for %%i in ("%SCRIPT_DIR%") do set "PROJECT_ROOT=%%~dpi"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

cd /d "%PROJECT_ROOT%" || (
    echo Failed to navigate to project directory
    exit /b 1
)

npm ci

endlocal
