$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup_windows.ps1 first."
}

& .\.venv\Scripts\python.exe src\generate_once.py --run-id run_001 2>&1 |
    Tee-Object reports\run_001.log
