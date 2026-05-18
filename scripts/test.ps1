$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    & .\scripts\setup.ps1
}

& .\.venv\Scripts\python.exe -m pytest
