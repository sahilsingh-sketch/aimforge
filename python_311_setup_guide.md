# AimForge Python 3.11 Setup Guide

Since Python 3.13 is too new for major AI dependencies like `PaddleOCR`, `Ultralytics` (YOLO), and `psycopg2` (which currently require building from source on Windows), we are migrating the AimForge backend to **Python 3.11**, which natively supports pre-compiled Windows binaries.

This guide will walk you through creating a clean Python 3.11 virtual environment and installing all dependencies.

---

## 1. Install Python 3.11

If you haven't already installed Python 3.11 alongside your existing Python 3.13, you can install it seamlessly using the official Windows installer or Windows Package Manager (`winget`).

**Via Winget (Recommended):**
Open a new PowerShell window as Administrator and run:
```powershell
winget install -e --id Python.Python.3.11
```
*(You may need to restart your terminal after this completes so Windows registers the `py` command properly).*

---

## 2. Create a Python 3.11 Virtual Environment

Navigate into the `backend` folder of your project where your `requirements.txt` is located.
```powershell
cd C:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend
```

Create a brand new virtual environment specifically using the Python 3.11 executable. We will name this environment `venv311` to differentiate it from any existing environments.
```powershell
# The 'py -3.11' command forces the Windows Python Launcher to use the exact version
py -3.11 -m venv venv311
```

---

## 3. Activate the Environment

You must activate the new environment every time you want to run or test the backend.

**In PowerShell:**
```powershell
.\venv311\Scripts\Activate.ps1
```
*(You should see `(venv311)` appear at the start of your terminal prompt. If you get an ExecutionPolicy error, run `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` first).*

---

## 4. Install Dependencies

The `requirements.txt` file has been strictly updated and pinned to ensure NumPy 1.x is used (since NumPy 2.0 breaks Paddle), guaranteeing a smooth installation.

Run:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

> [!TIP]
> This command will download large pre-compiled wheel files for `paddlepaddle`, `ultralytics`, and `psycopg2-binary`. Unlike Python 3.13, this will *not* require any C++ Build Tools or local compilation!

---

## 5. Verify the Backend

Once the installation finishes, you can start the FastAPI backend exactly as before:

```powershell
python -m uvicorn backend.main:app --port 8000 --reload
```

Your background video processing pipeline (Frame Extraction -> OCR -> YOLO) is now fully operational! Uploading a real BGMI video through the React frontend will seamlessly trigger the AI engines.
