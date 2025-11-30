@echo off
setlocal enabledelayedexpansion

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
:: Remove trailing backslash
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
:: Navigate to the project root (parent of Scripts folder)
for %%i in ("%SCRIPT_DIR%") do set "PROJECT_ROOT=%%~dpi"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
:: Backend folder
set "BACKEND_DIR=%PROJECT_ROOT%\Backend"

cd /d "%BACKEND_DIR%" || (
    echo Failed to navigate to Backend directory
    exit /b 1
)

python -m venv .venv
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

endlocal
