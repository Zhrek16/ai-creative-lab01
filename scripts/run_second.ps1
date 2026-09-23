$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\artifacts\run_001\result.png")) {
    throw "Run 001 is missing. Complete the first run before repeating it."
}

& .\.venv\Scripts\python.exe src\generate_once.py --run-id run_002 2>&1 |
    Tee-Object reports\run_002.log

& .\.venv\Scripts\python.exe src\verify_artifacts.py |
    Tee-Object reports\sha256_comparison.txt
