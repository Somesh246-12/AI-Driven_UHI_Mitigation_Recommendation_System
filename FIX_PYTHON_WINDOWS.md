# Fix Python on Windows

## Problem

When you run `python`, you just see "Python" as output. This is because you have the Windows Store Python stub, which is not a full Python installation.

## Solution 1: Install Python from python.org (Recommended)

### Step 1: Download Python

1. Go to: https://www.python.org/downloads/
2. Download the latest Python 3.x (e.g., Python 3.11 or 3.12)
3. **IMPORTANT**: Choose the Windows installer (64-bit)

### Step 2: Install Python

1. Run the downloaded installer
2. **CRITICAL**: Check "Add Python to PATH" at the bottom of the installer
3. Click "Install Now"
4. Wait for installation to complete

### Step 3: Verify Installation

1. **Close and reopen PowerShell** (important!)
2. Run:
   ```powershell
   python --version
   ```
   You should see something like: `Python 3.11.0` or `Python 3.12.0`

3. Check pip:
   ```powershell
   python -m pip --version
   ```

### Step 4: Continue Setup

Once Python is installed correctly:

```powershell
# Navigate to backend directory
cd C:\Users\Admin\Desktop\UHI\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item .env.example .env

# Run backend
python run.py
```

## Solution 2: Install Python from Microsoft Store

### Step 1: Install Python from Store

1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Install"
4. Wait for installation to complete

### Step 2: Verify Installation

1. **Close and reopen PowerShell**
2. Run:
   ```powershell
   python --version
   ```

### Step 3: Continue Setup

Follow the same steps as Solution 1.

## Solution 3: Use Anaconda (Alternative)

### Step 1: Download Anaconda

1. Go to: https://www.anaconda.com/products/distribution
2. Download Anaconda for Windows
3. Install Anaconda

### Step 2: Use Anaconda Prompt

1. Open "Anaconda Prompt" (not regular PowerShell)
2. Navigate to backend:
   ```powershell
   cd C:\Users\Admin\Desktop\UHI\backend
   ```

3. Create virtual environment:
   ```powershell
   conda create -n uhi python=3.9
   conda activate uhi
   ```

4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

5. Create .env file:
   ```powershell
   Copy-Item .env.example .env
   ```

6. Run backend:
   ```powershell
   python run.py
   ```

## Quick Check: Is Python Installed Correctly?

Run this command:

```powershell
python --version
```

### Expected Output:
```
Python 3.11.0
```
or
```
Python 3.12.0
```

### If you see "Python" only:
- Python is NOT installed correctly
- Follow Solution 1 or Solution 2 above

### If you see an error:
- Python is not in PATH
- Reinstall Python and check "Add Python to PATH"
- Restart PowerShell after installation

## After Installing Python

### 1. Restart PowerShell

**IMPORTANT**: Close and reopen PowerShell after installing Python.

### 2. Verify Python

```powershell
python --version
python -m pip --version
```

### 3. Continue with Setup

```powershell
cd C:\Users\Admin\Desktop\UHI\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

## Troubleshooting

### Issue: Still seeing "Python" output

**Solution:**
1. Uninstall the Windows Store Python stub
2. Install Python from python.org (Solution 1)
3. Make sure to check "Add Python to PATH"
4. Restart your computer

### Issue: "python is not recognized"

**Solution:**
1. Reinstall Python from python.org
2. Check "Add Python to PATH" during installation
3. Restart PowerShell
4. If still not working, manually add Python to PATH:
   - Find Python installation (usually `C:\Python3x` or `C:\Users\YourName\AppData\Local\Programs\Python\Python3x`)
   - Add it to System Environment Variables PATH

### Issue: Virtual environment creation fails

**Solution:**
1. Make sure Python is installed correctly (see above)
2. Try using the full path:
   ```powershell
   C:\Python311\python.exe -m venv venv
   ```
3. Check if antivirus is blocking the operation

## Recommended: Install Python 3.11 or 3.12

1. Go to: https://www.python.org/downloads/
2. Download Python 3.11 or 3.12
3. **IMPORTANT**: Check "Add Python to PATH"
4. Install
5. **Restart PowerShell**
6. Verify: `python --version`
7. Continue with setup

## Next Steps

Once Python is installed correctly:

1. ✅ Verify Python: `python --version`
2. ✅ Create virtual environment: `python -m venv venv`
3. ✅ Activate: `.\venv\Scripts\Activate.ps1`
4. ✅ Install dependencies: `pip install -r requirements.txt`
5. ✅ Create .env: `Copy-Item .env.example .env`
6. ✅ Run backend: `python run.py`

Good luck! 🚀


