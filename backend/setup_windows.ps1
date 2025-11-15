# Windows Setup Script for UHI Backend
# Run this script in PowerShell: .\setup_windows.ps1

Write-Host "UHI Backend Setup for Windows" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found! Please install Python 3.8+ from python.org" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "Error activating virtual environment" -ForegroundColor Red
    Write-Host "Try running: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Write-Host "Then run this script again" -ForegroundColor Yellow
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "Error installing dependencies" -ForegroundColor Red
    exit 1
}

# Create .env file
Write-Host ""
Write-Host "Creating .env file..." -ForegroundColor Yellow
if (Test-Path ".env.example") {
    if (Test-Path ".env") {
        Write-Host ".env file already exists" -ForegroundColor Yellow
    } else {
        Copy-Item .env.example .env
        Write-Host ".env file created from .env.example" -ForegroundColor Green
        Write-Host "Edit .env file to add your OpenWeatherMap API key (optional)" -ForegroundColor Yellow
    }
} else {
    Write-Host ".env.example not found, creating .env file manually..." -ForegroundColor Yellow
    @"
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=uhi_db
OPENWEATHER_API_KEY=your_openweather_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
"@ | Out-File -FilePath .env -Encoding utf8
    Write-Host ".env file created" -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the backend server:" -ForegroundColor Yellow
Write-Host "  python run.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Or:" -ForegroundColor Yellow
Write-Host "  uvicorn app.main:app --reload --port 8000" -ForegroundColor Cyan
Write-Host ""


