@echo off
title National Public Grievance Redressal & Complaint Management Portal
cd /d "%~dp0"

echo ======================================================================
echo   NATIONAL GOVERNMENT COMPLAINT MANAGEMENT SYSTEM
echo   All-in-One Digital Public Grievance Redressal Platform
echo ======================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed or not in system PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

if not exist complaints.db (
    echo [INFO] First-time setup: Initializing and seeding realistic government complaints...
    python seed_data.py
    echo [OK] Database seeded successfully!
)

echo.
echo [STARTING] Launching National Grievance Portal Web Server...
echo [INFO] Citizen Home:       http://127.0.0.1:5000/
echo [INFO] Register Complaint: http://127.0.0.1:5000/register.html
echo [INFO] Track Grievance:    http://127.0.0.1:5000/track.html
echo [INFO] Officer Dashboard:  http://127.0.0.1:5000/admin.html
echo [INFO] Transparency Board: http://127.0.0.1:5000/transparency.html
echo.
echo [INFO] Press CTRL+C in this window at any time to stop the server.
echo.

start http://127.0.0.1:5000/
python app.py

pause
