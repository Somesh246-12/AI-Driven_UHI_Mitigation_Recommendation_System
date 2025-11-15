# Quick Fix for Python Issue

## Problem
When you run `python`, you just see "Python" as output. This means Python is not installed correctly.

## Quick Solution

### Step 1: Install Python

1. **Download Python from python.org:**
   - Go to: https://www.python.org/downloads/
   - Download Python 3.11 or 3.12
   - **IMPORTANT**: During installation, check "Add Python to PATH"
   - Install Python

2. **Restart PowerShell:**
   - Close PowerShell completely
   - Open a new PowerShell window

3. **Verify Python:**
   ```powershell
   python --version
   ```
   You should see: `Python 3.11.0` or similar (NOT just "Python")

### Step 2: Setup Backend

```powershell
# Navigate to backend
cd C:\Users\Admin\Desktop\UHI\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item .env.example .env

# Run backend
python run.py
```

## Alternative: Use Command Prompt (CMD)

If PowerShell doesn't work, use Command Prompt:

```cmd
cd C:\Users\Admin\Desktop\UHI\backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
python run.py
```

## Still Having Issues?

See `FIX_PYTHON_WINDOWS.md` for detailed troubleshooting.


