# Windows Setup Guide

This guide is specifically for Windows users using PowerShell.

## Prerequisites

1. **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
   - Verify installation: `python --version`

2. **Node.js 16+** - Download from [nodejs.org](https://nodejs.org/)
   - Verify installation: `node --version` and `npm --version`

3. **Mapbox Account** - Sign up at [mapbox.com](https://account.mapbox.com/)

## Step 1: Backend Setup

### 1. Open PowerShell in the backend directory

```powershell
cd C:\Users\Admin\Desktop\UHI\backend
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

**Note**: If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Create .env file

```powershell
# Copy the example file
Copy-Item .env.example .env

# Or create it manually
New-Item -Path .env -ItemType File
```

Then edit `.env` file and add:
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=uhi_db
OPENWEATHER_API_KEY=your_openweather_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
```

**Note**: The `OPENWEATHER_API_KEY` is optional. Leave it as is if you don't have one.

### 6. Run the backend server

```powershell
python run.py
```

Or:
```powershell
uvicorn app.main:app --reload --port 8000
```

The backend should now be running on `http://localhost:8000`

## Step 2: Frontend Setup

### 1. Open a NEW PowerShell window

Keep the backend running in the first window.

### 2. Navigate to the frontend directory

```powershell
cd C:\Users\Admin\Desktop\UHI\frontend
```

### 3. Install dependencies

```powershell
npm install
```

### 4. Create .env file

```powershell
# Create the .env file
New-Item -Path .env -ItemType File
```

Then edit `.env` file and add:
```
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
REACT_APP_API_URL=http://localhost:8000
```

### 5. Get your Mapbox token

1. Go to https://account.mapbox.com/
2. Sign up for a free account
3. Go to your account page
4. Copy your default public token
5. Paste it in `frontend/.env` as `REACT_APP_MAPBOX_TOKEN`

### 6. Run the frontend

```powershell
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

## Troubleshooting

### Python Issues

**Problem**: `python` command not found
**Solution**: 
- Make sure Python is installed and added to PATH
- Try `py` instead of `python` on Windows
- Reinstall Python and check "Add Python to PATH"

**Problem**: `pip` command not found
**Solution**: 
- Try `python -m pip` instead
- Or `py -m pip` on Windows
- Make sure Python is installed correctly

**Problem**: Virtual environment activation fails
**Solution**: 
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then try: `.\venv\Scripts\Activate.ps1`
- Alternative: Use `.\venv\Scripts\activate.bat` (CMD style)

### Node.js Issues

**Problem**: `npm` command not found
**Solution**: 
- Make sure Node.js is installed
- Restart PowerShell after installation
- Verify with: `node --version` and `npm --version`

**Problem**: Module installation fails
**Solution**: 
- Try: `npm install --legacy-peer-deps`
- Or: `npm cache clean --force` then `npm install`

### Backend Issues

**Problem**: Port 8000 already in use
**Solution**: 
- Change the port in `backend/.env`: `API_PORT=8001`
- Or stop the process using port 8000:
  ```powershell
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```

**Problem**: Module not found errors
**Solution**: 
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check that you're in the backend directory

### Frontend Issues

**Problem**: Map not loading
**Solution**: 
- Check that your Mapbox token is correct in `frontend/.env`
- Verify the token at https://account.mapbox.com/
- Check browser console for errors

**Problem**: API errors
**Solution**: 
- Make sure backend is running on port 8000
- Check `frontend/.env` has correct API URL
- Verify CORS is configured correctly

### File Issues

**Problem**: `.env.example` not found
**Solution**: 
- The file should be in `backend/.env.example`
- If not, create it manually with the content above
- Or copy from the example in the documentation

**Problem**: Cannot create .env file
**Solution**: 
- Use PowerShell: `New-Item -Path .env -ItemType File`
- Or create it manually in a text editor
- Make sure you're in the correct directory

## Quick Commands Reference

### Backend (PowerShell)

```powershell
# Navigate to backend
cd C:\Users\Admin\Desktop\UHI\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item .env.example .env

# Run server
python run.py
```

### Frontend (PowerShell)

```powershell
# Navigate to frontend
cd C:\Users\Admin\Desktop\UHI\frontend

# Install dependencies
npm install

# Create .env file
New-Item -Path .env -ItemType File

# Run frontend
npm start
```

## Alternative: Using Command Prompt (CMD)

If PowerShell doesn't work, you can use Command Prompt:

### Backend (CMD)

```cmd
cd C:\Users\Admin\Desktop\UHI\backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
python run.py
```

### Frontend (CMD)

```cmd
cd C:\Users\Admin\Desktop\UHI\frontend
npm install
echo REACT_APP_MAPBOX_TOKEN=your_token_here > .env
echo REACT_APP_API_URL=http://localhost:8000 >> .env
npm start
```

## Getting Help

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Make sure virtual environment is activated (backend)
4. Check that both backend and frontend are running
5. Check browser console for errors
6. Check PowerShell/CMD for error messages

## Next Steps

Once everything is running:

1. Explore the interactive map
2. Add interventions and see their impact
3. Check AI recommendations
4. Review health precautions
5. Test dark/light mode toggle

Good luck! 🚀


