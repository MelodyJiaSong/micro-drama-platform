param([switch]$Inspect)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$Python = Join-Path $RepoRoot '.venv/Scripts/python.exe'
Push-Location $RepoRoot
try {
    if ($Inspect) { & $Python -m projects.suno_browser_service.apps.login.main --inspect }
    else { & $Python -m projects.suno_browser_service.apps.login.main }
    if ($LASTEXITCODE -ne 0) { throw 'Login or inspection failed; stop the service before using this command.' }
} finally { Pop-Location }
