# Backend startup script for PlacementPro
# Run from project root: .\backend\start_backend.ps1

Set-Location -LiteralPath "D:\Project-Fremen\backend"

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & "venv\Scripts\Activate.ps1"
    pip install -r requirements.txt
    Write-Host "Dependencies installed" -ForegroundColor Green
}

# Check .env exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env not found. Copy .env.example to .env and fill in values." -ForegroundColor Red
    exit 1
}

# Start server
Write-Host "Starting FastAPI on http://localhost:8000" -ForegroundColor Cyan
uvicorn app.main:app --reload --port 8000