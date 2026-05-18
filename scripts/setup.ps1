$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    $PyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($PyLauncher) {
        py -3 -m venv .venv
    } else {
        python -m venv .venv
    }
}

& .\.venv\Scripts\python.exe -m pip install --upgrade pip

if (Test-Path pyproject.toml) {
    & .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
} elseif (Test-Path requirements.txt) {
    & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
} else {
    Write-Host "No pyproject.toml or requirements.txt found; venv created only."
}

Write-Host "Environment is ready."
