@echo off
setlocal enabledelayedexpansion
title Autonomous Agent - Laptop Local Installer
color 0A

cls
echo ==============================================================================
echo   AUTONOMOUS ASSESSMENT AGENT - LOCAL LAPTOP INSTALLER
echo ==============================================================================
echo.
echo [*] Step 1/3: Preparing target installation directory on this computer...
set "TARGET_DIR=%USERPROFILE%\Desktop\Autonomous_Exam_Agent"

if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

echo [*] Target Directory: %TARGET_DIR%
echo.
echo [*] Step 2/3: Copying full autonomous suite from USB to local hard drive...
set "USB_SOURCE=%~dp0"

robocopy "%USB_SOURCE%" "%TARGET_DIR%" /E /XD .git .vercel __pycache__ /XF *.pyc install_to_laptop.bat >nul 2>&1

echo [OK] All agent modules, solvers, and dependencies copied successfully!
echo.
echo ==============================================================================
echo [OK] SUCCESS: Entire autonomous system is now installed on this laptop!
echo.
echo  👉 YOU CAN NOW SAFELY UNPLUG THE USB DRIVE!
echo ==============================================================================
echo.
echo Press ANY KEY to launch the Autonomous Agent directly from this laptop...
pause >nul

cd /d "%TARGET_DIR%"
start "" cmd /c "run_from_usb.bat"
exit
