@echo off
setlocal enabledelayedexpansion
title Autonomous Assessment Agent - Universal Deployer
color 0A

cls
echo ==============================================================================
echo   AUTONOMOUS SCREEN-AWARE AGENT - UNIVERSAL DEPLOYER
echo ==============================================================================
echo.

:: 1. CHECK AND INSTALL PYTHON
echo [*] Step 1/5: Checking Python Runtime...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed on this system.
    echo [*] Downloading and installing official Python 3.12 runtime automatically...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe', $env:TEMP + '\python_setup.exe'); Start-Process -FilePath ($env:TEMP + '\python_setup.exe') -ArgumentList '/quiet', 'InstallAllUsers=1', 'PrependPath=1', 'Include_pip=1' -Wait; Remove-Item ($env:TEMP + '\python_setup.exe')"
    echo [OK] Python installation complete!
    set "PATH=%ProgramFiles%\Python312;%ProgramFiles%\Python312\Scripts;%LocalAppData%\Programs\Python\Python312;%LocalAppData%\Programs\Python\Python312\Scripts;%PATH%"
) else (
    for /f "tokens=*" %%v in ('python --version') do echo [OK] Found %%v
)
echo.

:: 2. VERIFY AND INSTALL DEPENDENCIES
echo [*] Step 2/5: Verifying AI Agent Dependencies (Playwright, Groq)...
python -m pip install --quiet playwright groq
echo [OK] All required packages installed and verified.
echo.

:: 3. STRICT GROQ API KEY CONFIGURATION
echo [*] Step 3/5: Groq AI Inference Key Configuration
echo ------------------------------------------------------------------------------
:ASK_API_KEY
set "USER_API_KEY="
set /p USER_API_KEY="Enter Groq API Key (starts with gsk_...): "

if "%USER_API_KEY%"=="" (
    echo [!] Error: API Key cannot be empty. Please enter a valid key to proceed.
    echo.
    goto ASK_API_KEY
)

set "GROQ_API_KEY=%USER_API_KEY%"
echo GROQ_API_KEY=%GROQ_API_KEY% > .env
echo [OK] API Key saved to .env and loaded successfully.
echo.

:: 4. LAUNCH CLEAN CHROME ON PORT 9222 (NO PRESET DUMMY URL)
echo [*] Step 4/5: Initializing Chrome CDP on Port 9222...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 1 /nobreak >nul

set "CHROME_BIN="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set "CHROME_BIN=C:\Program Files\Google\Chrome\Application\chrome.exe"
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set "CHROME_BIN=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) else if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" (
    set "CHROME_BIN=%LocalAppData%\Google\Chrome\Application\chrome.exe"
)

if "%CHROME_BIN%"=="" (
    echo [!] Starting default Chrome on port 9222...
    start "" chrome --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile" "about:blank"
) else (
    start "" "%CHROME_BIN%" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile" "about:blank"
)
echo [OK] Clean Chrome window opened on Port 9222 (about:blank).
echo.

:: 5. INTERACTIVE TARGET URL SETUP
echo [*] Step 5/5: Ready for Target Assessment
echo ==============================================================================
echo  1. In the opened Chrome window, navigate to ANY test, quiz, or exam portal.
echo  2. Open the questions on screen.
echo  3. Return to this window when ready.
echo ==============================================================================
echo.
echo Press ANY KEY to unleash the Autonomous Solver Agent...
pause >nul
echo.
echo [*] Starting Autonomous Screen-Aware Agent...
echo ==============================================================================
python execute_agent.py

echo.
echo ==============================================================================
echo [OK] Session ended. Press any key to exit.
pause >nul
