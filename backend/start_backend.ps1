# Backend startup script for PlacementPro
# Run from anywhere: .\backend\start_backend.ps1
$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $PSScriptRoot

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & "venv\Scripts\Activate.ps1"
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Dependency installation failed. Cannot start server." -ForegroundColor Red
        exit 1
    }
    Write-Host "Dependencies installed" -ForegroundColor Green
}

# Verify .env exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env not found. Copy .env.example to .env and fill in values." -ForegroundColor Red
    exit 1
}

# Start server
Write-Host "Starting FastAPI on http://localhost:8000" -ForegroundColor Cyan
uvicorn app.main:app --reload --port 8000
