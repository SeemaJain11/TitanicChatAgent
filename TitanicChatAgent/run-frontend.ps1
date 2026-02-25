# Run Frontend Only
# Use this if the backend is already running

Write-Host "🎨 Starting Titanic Chat Agent Frontend..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Green
    & ".venv\Scripts\Activate.ps1"
}

# Check if backend is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 2 -UseBasicParsing
    Write-Host "✅ Backend is running on port 8000" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Warning: Backend doesn't seem to be running on port 8000" -ForegroundColor Yellow
    Write-Host "   Make sure to start the backend first!" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "🚀 Starting frontend server..." -ForegroundColor Green
Write-Host "   URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""

cd frontend
streamlit run app.py
