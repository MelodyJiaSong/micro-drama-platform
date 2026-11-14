# Opens the always-open Suno window (ordinary Chrome, service profile, debugging port on 127.0.0.1 only).
# Keep it open: the service works in its own tab there; log in and finish verifications in the same window.
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$Python = Join-Path $RepoRoot '.venv/Scripts/python.exe'
Push-Location $RepoRoot
try {
    & $Python -m projects.suno_browser_service.apps.window.main
    if ($LASTEXITCODE -ne 0) { throw 'Could not open the Suno window; see the message above.' }
} finally { Pop-Location }
