@echo off
setlocal enabledelayedexpansion
title Autonomous Assessment Agent - Local Laptop Installer
color 0A

cls
echo ==============================================================================
echo   AUTONOMOUS ASSESSMENT AGENT - LOCAL LAPTOP INSTALLER
echo ==============================================================================
echo.
echo [*] Step 1/3: Locating active Desktop...

set "DESKTOP_PATH="
for /f "usebackq delims=" %%D in (`powershell -NoProfile -Command "[Environment]::GetFolderPath('Desktop')"`) do set "DESKTOP_PATH=%%D"

if "%DESKTOP_PATH%"=="" (
    if exist "%USERPROFILE%\OneDrive\Desktop" (
        set "DESKTOP_PATH=%USERPROFILE%\OneDrive\Desktop"
    ) else (
        set "DESKTOP_PATH=%USERPROFILE%\Desktop"
    )
)

set "TARGET_DIR=%DESKTOP_PATH%\Autonomous_Exam_Agent"
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

echo [*] Target Directory: %TARGET_DIR%
echo.
echo [*] Step 2/3: Copying full autonomous suite from USB to Desktop...

:: Robust copy using PowerShell
powershell -NoProfile -Command "Get-ChildItem -Path '%~dp0' -Exclude '.git','.vercel','__pycache__','*.pyc','install_to_laptop.bat' | Copy-Item -Destination '%TARGET_DIR%' -Recurse -Force"

echo [OK] All agent modules, solvers, and dependencies copied successfully!
echo.
echo ==============================================================================
echo [OK] SUCCESS: Entire autonomous system is now on your Desktop!
echo.
echo  👉 YOU CAN NOW SAFELY UNPLUG THE USB DRIVE!
echo ==============================================================================
echo.
echo Press ANY KEY to launch the Autonomous Agent directly from your Desktop...
pause >nul

cd /d "%TARGET_DIR%"
start "" cmd /c "run_agent.bat"
exit
