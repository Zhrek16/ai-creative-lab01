$ErrorActionPreference = "Stop"

Write-Host "Creating Python 3.14 virtual environment..."
py -3.14 -m venv .venv

Write-Host "Activating environment..."
& .\.venv\Scripts\python.exe -m pip install --upgrade pip

Write-Host "Installing dependencies..."
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Saving environment..."
& .\.venv\Scripts\python.exe -m pip freeze | Out-File -Encoding utf8 reports\environment.txt

Write-Host ""
Write-Host "Installation finished."
Write-Host "Activate with:"
Write-Host ".\.venv\Scripts\Activate.ps1"
