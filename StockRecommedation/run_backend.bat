@echo off
echo Starting Stock Recommendation Backend Server...
REM cd backend
uvicorn backend.main:app --reload --port 8000
pause
