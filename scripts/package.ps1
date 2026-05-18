$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    & .\scripts\setup.ps1
}

& .\.venv\Scripts\python.exe -m PyInstaller --noconfirm --windowed --name BuddySoundboardStudioTest run_app.py

Write-Host "Package built at dist\BuddySoundboardStudioTest"
