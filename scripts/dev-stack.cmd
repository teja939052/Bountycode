@echo off
REM Start the local dev stack: MongoDB (portable mongod) + FastAPI backend.
REM Frontend is started separately with: cd frontend && npm run dev
REM
REM Why this exists: `make dev` expects Docker Compose, which is not installed
REM on this machine, so the backend and database were simply not running and the
REM UI reported "Request failed" for every login attempt.
REM
REM Port probing uses the backend venv's Python instead of netstat, because
REM netstat is not available on every Windows shell here (it aborts silently).

setlocal
set "MONGO_BIN=%LOCALAPPDATA%\mongodb\server\mongodb-win32-x86_64-windows-7.0.14\bin\mongod.exe"
set "MONGO_DATA=%LOCALAPPDATA%\mongodb\data"
set "MONGO_LOG=%LOCALAPPDATA%\mongodb\log\mongod.log"
set "BACKEND_PY=%~dp0..\backend\.venv\Scripts\python.exe"
set "BACKEND_DIR=%~dp0..\backend"

if not exist "%MONGO_BIN%" (
  echo [x] mongod.exe not found at "%MONGO_BIN%"
  echo     Download: https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.14.zip
  echo     Extract so that ...\mongodb-win32-x86_64-windows-7.0.14\bin\mongod.exe exists.
  exit /b 1
)

if not exist "%BACKEND_PY%" (
  echo [x] Backend venv not found: "%BACKEND_PY%"
  echo     Create it: cd backend + python -m venv .venv + .venv\Scripts\pip install -r requirements.txt
  exit /b 1
)

REM ---- MongoDB ----
call :port_open 27017
if %ERRORLEVEL% equ 0 goto mongo_ready
echo [^>] Starting mongod on 127.0.0.1:27017
if not exist "%MONGO_DATA%" mkdir "%MONGO_DATA%"
if not exist "%LOCALAPPDATA%\mongodb\log" mkdir "%LOCALAPPDATA%\mongodb\log"
start "mongod" /min "%MONGO_BIN%" --dbpath "%MONGO_DATA%" --port 27017 --bind_ip 127.0.0.1 --logpath "%MONGO_LOG%" --logappend
"%SystemRoot%\System32\timeout.exe" /t 3 /nobreak >nul
goto mongo_ready
:mongo_ready
call :port_open 27017
if %ERRORLEVEL% neq 0 (
  echo [x] MongoDB did not start. See "%MONGO_LOG%"
  exit /b 1
)
echo [=] MongoDB is up on 127.0.0.1:27017

REM ---- Backend ----
call :port_open 8000
if %ERRORLEVEL% equ 0 goto backend_ready
echo [^>] Starting FastAPI backend on http://127.0.0.1:8000
start "backend" /d "%BACKEND_DIR%" /min "%BACKEND_PY%" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
:backend_ready
call :port_open 8000
if %ERRORLEVEL% equ 0 (
  echo [=] Backend is up on http://127.0.0.1:8000
) else (
  echo [.] Backend still starting ^(it loads the question bank at boot, ~20s^).
  echo     Check http://127.0.0.1:8000/api/v1/health/live in a moment.
)

echo.
echo API:      http://127.0.0.1:8000/api/v1/health/live
echo Frontend: http://localhost:5173  (cd frontend + npm run dev)
endlocal
exit /b 0

:port_open
"%BACKEND_PY%" -c "import socket,sys;s=socket.socket();s.settimeout(1);sys.exit(0 if s.connect_ex(('127.0.0.1',%1))==0 else 1)"
exit /b %ERRORLEVEL%
