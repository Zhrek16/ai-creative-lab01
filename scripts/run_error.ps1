$ErrorActionPreference = "Continue"

if (-not (Test-Path ".\src\generate_error.py")) {
    Copy-Item ".\src\generate_once.py" ".\src\generate_error.py"
}

Write-Host "CUDA availability:"
& .\.venv\Scripts\python.exe -c "import torch; print(torch.cuda.is_available())"

Write-Host ""
Write-Host "Before running, edit src\generate_error.py:"
Write-Host 'replace torch.Generator(device="cpu") with torch.Generator(device="cuda")'
Write-Host ""

& .\.venv\Scripts\python.exe src\generate_error.py --run-id error_run 2>&1 |
    Tee-Object reports\error.log
