@echo off
setlocal enabledelayedexpansion
title Autonomous Zero-Tolerance Agent - Universal USB Deployer
color 0A

cls
echo ==============================================================================
echo   AUTONOMOUS ZERO-TOLERANCE AGENT - UNIVERSAL USB DEPLOYER
echo ==============================================================================
echo.

:: 1. CHECK PYTHON INSTALLATION
echo [*] Step 1/5: Checking Python Runtime...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed on this system.
    echo [*] Downloading and installing Python 3.12 automatically...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe', $env:TEMP + '\python_setup.exe'); Start-Process -FilePath ($env:TEMP + '\python_setup.exe') -ArgumentList '/quiet', 'InstallAllUsers=1', 'PrependPath=1', 'Include_pip=1' -Wait; Remove-Item ($env:TEMP + '\python_setup.exe')"
    echo [OK] Python installation complete!
    set "PATH=%ProgramFiles%\Python312;%ProgramFiles%\Python312\Scripts;%LocalAppData%\Programs\Python\Python312;%LocalAppData%\Programs\Python\Python312\Scripts;%PATH%"
) else (
    for /f "tokens=*" %%v in ('python --version') do echo [OK] Found %%v
)
echo.

:: 2. PROMPT FOR API KEY
echo [*] Step 2/5: Groq AI Inference Key Configuration
echo ------------------------------------------------------------------------------
if defined GROQ_API_KEY (
    echo [OK] Detected existing GROQ_API_KEY in environment.
) else (
    echo Enter your Groq API Key:
    set /p USER_API_KEY="API Key: "
    set "GROQ_API_KEY=!USER_API_KEY!"
)
if "!GROQ_API_KEY!"=="" (
    echo [!] Note: No key typed, checking for .env file...
) else (
    echo GROQ_API_KEY=!GROQ_API_KEY! > .env
    echo [OK] API Key saved to .env
)
echo.

:: 3. INSTALL PYTHON LIBRARIES
echo [*] Step 3/5: Verifying AI Agent Dependencies...
python -m pip install --quiet playwright groq
echo [OK] Required packages verified.
echo.

:: 4. LOCATE AND LAUNCH CHROME ON PORT 9222
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

if "!CHROME_BIN!"=="" (
    echo [!] Launching default Chrome...
    start "" chrome --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile" "https://secure-online-exam-portal-zt.vercel.app/"
) else (
    start "" "!CHROME_BIN!" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile" "https://secure-online-exam-portal-zt.vercel.app/"
)
echo [OK] Chrome launched on port 9222 connected to live exam portal!
echo.

:: 5. LAUNCH AUTONOMOUS SOLVER AGENT
echo [*] Step 5/5: Starting Autonomous Screen-Aware Agent...
echo ==============================================================================
timeout /t 2 /nobreak >nul
python execute_agent.py

echo.
echo ==============================================================================
echo [OK] Execution session complete. Press any key to exit.
pause >nul
