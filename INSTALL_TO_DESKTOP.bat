@echo off
setlocal enabledelayedexpansion
title Deploying Agent to Local System...
color 0B

cls
echo ==============================================================================
echo   AUTONOMOUS ASSESSMENT AGENT - LOCAL HARD DRIVE DEPLOYER
echo ==============================================================================
echo.
echo [*] Target Installation Directory:
echo     %USERPROFILE%\Desktop\Autonomous_Exam_Agent
echo.

set "DEST=%USERPROFILE%\Desktop\Autonomous_Exam_Agent"

if not exist "%DEST%" (
    mkdir "%DEST%"
)

echo [*] Copying all agent runtime files from USB to local hard drive...
robocopy "%~dp0." "%DEST%" /E /XD .git .vercel __pycache__ /XF *.pyc /R:1 /W:1 >nul

:: Ensure LAUNCH_AGENT.bat exists in destination
copy /Y "%~dp0run_from_usb.bat" "%DEST%\LAUNCH_AGENT.bat" >nul 2>&1

echo.
echo ==============================================================================
echo [✓] SUCCESS: Autonomous Agent successfully deployed to this laptop!
echo.
echo 👉 1. YOU CAN NOW SAFELY UNPLUG AND REMOVE THIS USB DRIVE!
echo 👉 2. Open the 'Autonomous_Exam_Agent' folder on your Desktop.
echo 👉 3. Double-click 'LAUNCH_AGENT.bat' to run entirely from this laptop.
echo ==============================================================================
echo.
explorer "%DEST%"
echo Press any key to finish installer...
pause >nul
