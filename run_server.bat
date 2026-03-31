@echo off
set PUBLIC_URL=https://pyme-survey.onrender.com
cd /d "%~dp0"
.venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8777
