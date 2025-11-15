# Windows Troubleshooting Guide

## Issue: Python Not Working Properly

If you see "Python" as output or Python commands don't work, follow these steps:

### Step 1: Check Python Installation

1. **Check if Python is installed:**
   ```powershell
   python --version
   ```
   
   If this doesn't work, try:
   ```powershell
   py --version
   ```
   
   Or check in Windows:
   - Press `Win + R`
   - Type `appwiz.cpl` and press Enter
   - Look for "Python" in the list

2. **If Python is NOT installed:**
   - Download Python from: https://www.python.org/downloads/
   - **IMPORTANT**: During installation, check "Add Python to PATH"
   - After installation, restart PowerShell

3. **If Python IS installed but not working:**
   - Reinstall Python and make sure to check "Add Python to PATH"
   - Or manually add Python to PATH:
     - Find Python installation path (usually `C:\Python3x` or `C:\Users\YourName\AppData\Local\Programs\Python\Python3x`)
     - Add it to PATH in System Environment Variables

### Step 2: Verify Python Installation

After installing/reinstalling Python:

```powershell
# Restart PowerShell, then run:
python --version
```

You should see something like: `Python 3.11.0` or similar.

### Step 3: Create Virtual Environment

Once Python is working:

```powershell
# Navigate to backend directory
cd C:\Users\Admin\Desktop\UHI\backend

# Create virtual environment
python -m venv venv

# Wait for it to complete (may take 30-60 seconds)
```

### Step 4: Activate Virtual Environment

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**

```powershell
# Run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
.\venv\Scripts\Activate.ps1
```

**Alternative: Use Command Prompt (CMD)**

If PowerShell doesn't work, use Command Prompt:

```cmd
cd C:\Users\Admin\Desktop\UHI\backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python run.py
```

### Step 5: Install Dependencies

```powershell
# Make sure virtual environment is activated (you should see (venv) in prompt)
pip install -r requirements.txt
```

### Step 6: Create .env File

```powershell
# Create .env file
Copy-Item .env.example .env

# Or create manually:
New-Item -Path .env -ItemType File
```

Then edit `.env` file with:
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=uhi_db
OPENWEATHER_API_KEY=your_openweather_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
```

### Step 7: Run Backend

```powershell
python run.py
```

## Common Issues and Solutions

### Issue 1: "python is not recognized"

**Solution:**
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart PowerShell after installation

### Issue 2: "pip is not recognized"

**Solution:**
- Make sure Python is installed correctly
- Try: `python -m pip` instead of `pip`
- Or reinstall Python with "Add Python to PATH" checked

### Issue 3: "Execution policy error"

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 4: Virtual environment activation fails

**Solution:**
- Try using Command Prompt instead: `venv\Scripts\activate.bat`
- Or check if the venv folder exists: `Test-Path venv`

### Issue 5: Port 8000 already in use

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace <PID> with the actual PID)
taskkill /PID <PID> /F
```

### Issue 6: Module not found errors

**Solution:**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check that you're in the backend directory

## Manual Setup (If Scripts Don't Work)

### Backend Setup

1. **Open PowerShell in backend directory:**
   ```powershell
   cd C:\Users\Admin\Desktop\UHI\backend
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Create .env file:**
   - Create a new file named `.env` in the backend directory
   - Add the following content:
     ```
     MONGODB_URI=mongodb://localhost:27017
     MONGODB_DB=uhi_db
     OPENWEATHER_API_KEY=your_openweather_api_key_here
     API_HOST=0.0.0.0
     API_PORT=8000
     ```

6. **Run backend:**
   ```powershell
   python run.py
   ```

## Alternative: Use Command Prompt (CMD)

If PowerShell gives you trouble, use Command Prompt:

1. **Open Command Prompt (CMD)**
2. **Navigate to backend:**
   ```cmd
   cd C:\Users\Admin\Desktop\UHI\backend
   ```

3. **Create virtual environment:**
   ```cmd
   python -m venv venv
   ```

4. **Activate virtual environment:**
   ```cmd
   venv\Scripts\activate.bat
   ```

5. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

6. **Create .env file:**
   ```cmd
   copy .env.example .env
   ```

7. **Run backend:**
   ```cmd
   python run.py
   ```

## Verify Python Installation

Run these commands to verify Python is working:

```powershell
# Check Python version
python --version

# Check pip
python -m pip --version

# Check Python location
where.exe python
```

## Still Having Issues?

1. **Check Python installation:**
   - Go to https://www.python.org/downloads/
   - Download latest Python 3.x
   - During installation, check "Add Python to PATH"
   - Restart your computer after installation

2. **Check PATH variable:**
   - Press `Win + X` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Check if Python is in the PATH

3. **Try reinstalling Python:**
   - Uninstall Python
   - Download fresh Python installer
   - Install with "Add Python to PATH" checked
   - Restart computer

4. **Use Anaconda (Alternative):**
   - Download Anaconda from: https://www.anaconda.com/products/distribution
   - Install Anaconda
   - Use Anaconda Prompt instead of PowerShell
   - Create virtual environment: `conda create -n uhi python=3.9`
   - Activate: `conda activate uhi`

## Quick Test

Run this to test if everything is working:

```powershell
# Test Python
python --version

# Test pip
python -m pip --version

# Test virtual environment creation
python -m venv test_venv
Remove-Item -Recurse -Force test_venv
```

If all these work, you're good to go!


