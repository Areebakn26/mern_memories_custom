# run_local.ps1 - PowerShell script for local testing
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "RUNNING SELENIUM TESTS LOCALLY" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Install dependencies if needed
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`nStarting tests..." -ForegroundColor Green
Write-Host "Make sure your MERN app is running on http://localhost:3000" -ForegroundColor Yellow
Write-Host "Press any key to continue or Ctrl+C to cancel..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

# Run tests
python run_tests.py

# Deactivate virtual environment
deactivate

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "TESTS COMPLETED" -ForegroundColor Cyan
Write-Host "Check test_report.html for results" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan