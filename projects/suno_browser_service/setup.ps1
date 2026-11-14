$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$Python = Join-Path $RepoRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $Python)) {
    python -m venv (Join-Path $RepoRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Cannot create Python environment' }
}
& $Python -m ensurepip --upgrade
if ($LASTEXITCODE -ne 0) { throw 'Cannot install pip' }
& $Python -m pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
Push-Location (Join-Path $PSScriptRoot 'apps/ui')
try {
    & npm ci
    if ($LASTEXITCODE -ne 0) { throw 'UI dependency installation failed; Node.js and npm are required.' }
    & npm run build
    if ($LASTEXITCODE -ne 0) { throw 'UI build failed.' }
} finally { Pop-Location }
Write-Output 'Setup complete. Chrome is used by default. Run login.ps1 once, then start.ps1. UI: http://127.0.0.1:8770/ui/'
