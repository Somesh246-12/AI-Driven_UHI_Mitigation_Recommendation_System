# Windows Setup Script for UHI Frontend
# Run this script in PowerShell: .\setup_windows.ps1

Write-Host "UHI Frontend Setup for Windows" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green
Write-Host ""

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Node.js not found! Please install Node.js 16+ from nodejs.org" -ForegroundColor Red
    exit 1
}

# Check if npm is installed
Write-Host ""
Write-Host "Checking npm installation..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version 2>&1
    Write-Host "npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "npm not found! Please install Node.js (npm comes with Node.js)" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "Error installing dependencies" -ForegroundColor Red
    Write-Host "Try running: npm install --legacy-peer-deps" -ForegroundColor Yellow
    exit 1
}

# Create .env file
Write-Host ""
Write-Host "Creating .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env file already exists" -ForegroundColor Yellow
} else {
    @"
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
REACT_APP_API_URL=http://localhost:8000
"@ | Out-File -FilePath .env -Encoding utf8
    Write-Host ".env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: Edit .env file and add your Mapbox token!" -ForegroundColor Red
    Write-Host "Get your token from: https://account.mapbox.com/" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Don't forget to:" -ForegroundColor Yellow
Write-Host "  1. Edit .env file and add your Mapbox token" -ForegroundColor Cyan
Write-Host "  2. Make sure the backend server is running on port 8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the frontend:" -ForegroundColor Yellow
Write-Host "  npm start" -ForegroundColor Cyan
Write-Host ""


