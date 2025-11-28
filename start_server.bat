@echo off
title Genesis Bible Visualizer Server
cd /d "%~dp0"

echo ============================================================
echo    Genesis Bible Visualizer - Server Launcher
echo ============================================================
echo.
echo Starting servers...
echo    Static files: http://localhost:8005
echo    API server:   http://localhost:8003
echo.
echo Press Ctrl+C to stop the servers.
echo ============================================================
echo.

python api_server.py

pause
