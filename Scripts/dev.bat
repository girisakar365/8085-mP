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

echo ==========================================
echo    8085 Microprocessor Simulator - Development Setup   
echo ==========================================
echo.

:: ----- Pre-flight checks -----
echo [1/6] Running pre-flight checks...

:: Check if python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo X Error: python is not installed
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo   √ python found: %%i

:: Check if npm is installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo X Error: npm is not installed
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version 2^>^&1') do echo   √ npm found: %%i

:: Check if cargo (Rust) is installed
where cargo >nul 2>nul
if %errorlevel% neq 0 (
    echo X Error: Rust/Cargo is not installed
    echo   Install Rust from: https://rustup.rs/
    exit /b 1
)
for /f "tokens=*" %%i in ('cargo --version 2^>^&1') do echo   √ cargo found: %%i

:: Check if tauri-cli is available
where cargo-tauri >nul 2>nul
if %errorlevel% neq 0 (
    echo   ! Warning: tauri-cli not found globally, will use npx @tauri-apps/cli
)

:: Check if project root exists
if not exist "%PROJECT_ROOT%" (
    echo X Error: Project root directory not found: %PROJECT_ROOT%
    exit /b 1
)
echo   √ Project root found: %PROJECT_ROOT%

:: Check if Backend directory exists
if not exist "%BACKEND_DIR%" (
    echo X Error: Backend directory not found: %BACKEND_DIR%
    exit /b 1
)
echo   √ Backend directory found

:: Check if package.json exists
if not exist "%PROJECT_ROOT%\package.json" (
    echo X Error: package.json not found in project root
    exit /b 1
)
echo   √ package.json found

:: Check if requirements.txt exists
if not exist "%BACKEND_DIR%\requirements.txt" (
    echo X Error: requirements.txt not found in Backend directory
    exit /b 1
)
echo   √ requirements.txt found

:: ----- Backend Setup -----
echo.
echo [2/6] Setting up Python virtual environment...
cd /d "%BACKEND_DIR%" || (
    echo X Failed to navigate to Backend directory
    exit /b 1
)

if not exist ".venv" (
    python -m venv .venv || (
        echo X Failed to create virtual environment
        exit /b 1
    )
    echo   √ Virtual environment created
) else (
    echo   √ Virtual environment already exists
)

echo.
echo [3/6] Activating virtual environment...
call .venv\Scripts\activate.bat || (
    echo X Failed to activate virtual environment
    exit /b 1
)
echo   √ Virtual environment activated

echo.
echo [4/6] Installing Python dependencies...
pip install --upgrade pip -q || (
    echo X Failed to upgrade pip
    exit /b 1
)
pip install -r requirements.txt -q || (
    echo X Failed to install Python dependencies
    exit /b 1
)
echo   √ Python dependencies installed

:: ----- Frontend Setup -----
echo.
echo [5/6] Setting up Frontend...
cd /d "%PROJECT_ROOT%" || (
    echo X Failed to navigate to project directory
    exit /b 1
)

call npm ci || (
    echo X Failed to install npm dependencies
    exit /b 1
)
echo   √ npm dependencies installed

:: ----- Done -----
echo.
echo [6/6] Setup complete!
echo.
echo ==========================================
echo    Ready to develop!                     
echo ==========================================
echo.

endlocal
