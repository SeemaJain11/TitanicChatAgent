# Titanic Chat Agent Startup Script
# This script starts both the backend (FastAPI) and frontend (Streamlit) servers

Write-Host "🚢 Starting Titanic Chat Agent..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "⚠️  Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Green
& ".venv\Scripts\Activate.ps1"

# Check if dependencies are installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Green
$pipList = pip list
if ($pipList -notmatch "fastapi") {
    Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Red
    Write-Host "Please create a .env file with your OPENAI_API_KEY" -ForegroundColor Red
    Write-Host "You can copy .env.example to .env and add your key" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "✅ Starting servers..." -ForegroundColor Green
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the servers" -ForegroundColor Yellow
Write-Host ""

# Start backend in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '.venv\Scripts\Activate.ps1'; cd backend; Write-Host '🔧 Starting Backend Server...' -ForegroundColor Green; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend in current window
cd frontend
Write-Host "🎨 Starting Frontend Server..." -ForegroundColor Green
streamlit run app.py
