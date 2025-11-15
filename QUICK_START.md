# Quick Start Guide

## Prerequisites Check

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Mapbox account (free tier is sufficient)
- [ ] (Optional) OpenWeatherMap API key for real-time data

## Step 1: Backend Setup (5 minutes)

### Windows (PowerShell)

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item .env.example .env

# Edit .env file (optional - works without API key)
# Add your OpenWeatherMap API key if you have one

# Run the backend server
python run.py
```

### Linux/Mac

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file (optional - works without API key)
# Add your OpenWeatherMap API key if you have one

# Run the backend server
python run.py
```

The backend should now be running on `http://localhost:8000`

## Step 2: Frontend Setup (5 minutes)

### Windows (PowerShell)

```powershell
# Open a new PowerShell window
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
New-Item -Path .env -ItemType File

# Edit .env file and add your Mapbox token
# Get your token from: https://account.mapbox.com/
# Add these lines to .env:
# REACT_APP_MAPBOX_TOKEN=your_token_here
# REACT_APP_API_URL=http://localhost:8000

# Run the frontend
npm start
```

### Linux/Mac

```bash
# Open a new terminal window
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env file and add your Mapbox token
# Get your token from: https://account.mapbox.com/
# REACT_APP_MAPBOX_TOKEN=your_token_here
# REACT_APP_API_URL=http://localhost:8000

# Run the frontend
npm start
```

The frontend should now be running on `http://localhost:3000`

## Step 3: Test the Application

1. Open your browser and go to `http://localhost:3000`
2. You should see the UHI Mitigation System dashboard
3. The map should show a heatmap of Pune
4. Try adding interventions:
   - Click on a tool button (Trees, Cool Roof, Park, Green Roof)
   - Click on the map to place an intervention
   - Click "Simulate" to see the impact
5. Check the recommendations panel on the right
6. Scroll down to see health precautions

## Step 4: Test the API (Optional)

```bash
# In the backend directory, run the test script
python test_api.py
```

This will test all API endpoints and verify they're working correctly.

## Troubleshooting

### Windows-Specific Issues

**Problem**: `source` command not found (PowerShell)
**Solution**: Use `.\venv\Scripts\Activate.ps1` instead of `source venv/bin/activate`

**Problem**: Execution policy error
**Solution**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Problem**: `.env.example` not found
**Solution**: The file should exist in `backend/.env.example`. If not, create it manually or use `Copy-Item` command

**Problem**: `cp` command not found (PowerShell)
**Solution**: Use `Copy-Item` instead of `cp` on Windows PowerShell

### Backend Issues

**Problem**: Port 8000 already in use
**Solution**: Change the port in `backend/.env` or stop the process using port 8000:
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Problem**: Module not found errors
**Solution**: Make sure you're in the virtual environment and run `pip install -r requirements.txt` again

**Problem**: CORS errors
**Solution**: Check that `http://localhost:3000` is in the CORS origins list in `backend/app/main.py`

**Problem**: Python/pip not found
**Solution**: Make sure Python is installed and added to PATH. Try `py` instead of `python` on Windows

### Frontend Issues

**Problem**: Map not loading
**Solution**: 
- Check that your Mapbox token is correct in `frontend/.env`
- Verify the token has the right permissions
- Check the browser console for errors

**Problem**: API errors
**Solution**: 
- Make sure the backend is running on port 8000
- Check the browser console for specific error messages
- Verify the API URL in `frontend/.env`

**Problem**: Module not found errors
**Solution**: Run `npm install` again in the frontend directory

**Problem**: Cannot create .env file
**Solution**: Use `New-Item -Path .env -ItemType File` in PowerShell, or create it manually in a text editor

### Mapbox Issues

**Problem**: Token errors
**Solution**: 
- Verify your token at https://account.mapbox.com/
- Make sure the token is pasted correctly in `frontend/.env`
- Check that the token has the necessary scopes

**Problem**: Style errors
**Solution**: The default style should work, but you can change it in `frontend/src/components/MapContainer.js`

## Getting API Keys

### Mapbox Token (Required)

1. Go to https://account.mapbox.com/
2. Sign up for a free account
3. Go to your account page
4. Copy your default public token
5. Paste it in `frontend/.env` as `REACT_APP_MAPBOX_TOKEN`

### OpenWeatherMap API Key (Optional)

1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to `backend/.env` as `OPENWEATHER_API_KEY`

**Note**: The application works without the OpenWeatherMap API key. It will use synthetic data that simulates realistic UHI patterns.

## Next Steps

1. Explore the interactive map and add interventions
2. Test different intervention types and see their impact
3. Check the AI recommendations
4. Review the health precautions based on climate data
5. Customize the application for your needs

## Project Structure

```
UHI/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── README.md          # Main documentation
├── SETUP.md           # Detailed setup instructions
├── QUICK_START.md     # This file
└── PROJECT_SUMMARY.md # Project overview
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the SETUP.md for detailed instructions
3. Check the browser console for errors
4. Verify all environment variables are set correctly

## Features to Try

- **Heatmap Visualization**: View the thermal heatmap of Pune
- **Add Interventions**: Click tools and place interventions on the map
- **Simulate Impact**: See predicted temperature reduction and other metrics
- **AI Recommendations**: Check the recommendations panel for suggested actions
- **Health Precautions**: Scroll down to see health advice based on climate data
- **Dark Mode**: Toggle dark/light mode using the switch in the header

Enjoy building your UHI Mitigation System! 🚀

