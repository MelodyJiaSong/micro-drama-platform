param([switch]$Foreground)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$Python = Join-Path $RepoRoot '.venv/Scripts/python.exe'
$DataDir = Join-Path $RepoRoot '.audit/service_requests/suno_browser_service'
$Record = Join-Path $DataDir 'server.json'
# The service works in the always-open window; open it too unless attach mode is off (SUNO_BROWSER_ATTACH_PORT=0).
function Open-SunoWindow {
    if ($env:SUNO_BROWSER_ATTACH_PORT -eq '0' -or $env:SUNO_BROWSER_WS) { return }
    & $Python -m projects.suno_browser_service.apps.window.main
    if ($LASTEXITCODE -ne 0) { Write-Warning 'Service is running but the Suno window did not open; run open-window.ps1.' }
}
Push-Location $RepoRoot
try {
    & $Python -c 'from projects.suno_browser_service.libs.common.settings import Settings; from projects.suno_browser_service.libs.infrastructure.writers.private_directory__writer import PrivateDirectoryWriter; PrivateDirectoryWriter.ensure(Settings.from_env().data_dir)'
    if ($LASTEXITCODE -ne 0) { throw 'Cannot initialize private service directory' }
    if (Test-Path -LiteralPath $Record) {
        $Previous = Get-Content -LiteralPath $Record -Raw | ConvertFrom-Json
        $Running = Get-CimInstance Win32_Process -Filter "ProcessId=$($Previous.pid)" -ErrorAction SilentlyContinue
        if ($Running -and $Running.CommandLine -match 'projects\.suno_browser_service\.apps\.api\.main') {
            Write-Output "Already running: http://127.0.0.1:$($Previous.port)/ui/ (API docs: /docs)"
            Open-SunoWindow
            exit 0
        }
    }
    if ($Foreground) { & $Python -m projects.suno_browser_service.apps.api.main; exit $LASTEXITCODE }
    $ServiceProcess = Start-Process -FilePath $Python -ArgumentList '-m', 'projects.suno_browser_service.apps.api.main' -WorkingDirectory $RepoRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $DataDir 'server.log') -RedirectStandardError (Join-Path $DataDir 'server-error.log')
    for ($Attempt = 0; $Attempt -lt 20; $Attempt++) {
        Start-Sleep -Milliseconds 500
        if ($ServiceProcess.HasExited) { throw 'Service exited; see .audit/service_requests/suno_browser_service/server-error.log' }
        if (Test-Path -LiteralPath $Record) {
            $Current = Get-Content -LiteralPath $Record -Raw | ConvertFrom-Json
            $ServerProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$($Current.pid)" -ErrorAction SilentlyContinue
            if ($ServerProcess -and ($Current.pid -eq $ServiceProcess.Id -or $ServerProcess.ParentProcessId -eq $ServiceProcess.Id) -and $ServerProcess.CommandLine -match 'projects\.suno_browser_service\.apps\.api\.main') {
                try {
                    $Health = Invoke-RestMethod "http://127.0.0.1:$($Current.port)/health" -TimeoutSec 5
                    if ($Health.status -eq 'ok') {
                        Write-Output "Running: http://127.0.0.1:$($Current.port)/ui/ (API docs: /docs; PID $($Current.pid))"
                        Open-SunoWindow
                        exit 0
                    }
                } catch { }
            }
        }
    }
    throw 'Service is still starting; inspect the service logs.'
} finally { Pop-Location }
