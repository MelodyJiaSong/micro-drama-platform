$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    $downloadPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $downloadPython)) {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Python 3.11+ is required.' }
    }
    & $downloadPython -c "import importlib.util; raise SystemExit(0 if all(importlib.util.find_spec(name) for name in ['yt_dlp', 'dependency_injector', 'yt_dlp_ejs']) else 1)"
    if ($LASTEXITCODE -ne 0) {
        & $downloadPython -m pip install -r requirements.txt
        if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
    }
    & $downloadPython -m apps.desktop.main
    if ($LASTEXITCODE -ne 0) { throw 'The downloader could not start.' }
} finally {
    Pop-Location
}
