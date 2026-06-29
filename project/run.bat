@echo off
REM Double-click this file (or run it in a terminal) to start the NexForge site.
cd /d "%~dp0"
echo Starting NexForge dev server...
echo Open http://127.0.0.1:8000/ in your browser once it says "Starting development server".
echo Press Ctrl+C in this window to stop.
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
pause
