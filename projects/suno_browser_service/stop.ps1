$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$DataDir = Join-Path $RepoRoot '.audit/service_requests/suno_browser_service'
$Record = Join-Path $DataDir 'server.json'
if (-not (Test-Path -LiteralPath $Record)) { Write-Output 'Not running'; exit 0 }
$Current = Get-Content -LiteralPath $Record -Raw | ConvertFrom-Json
$Running = Get-CimInstance Win32_Process -Filter "ProcessId=$($Current.pid)" -ErrorAction SilentlyContinue
if (-not $Running) { Write-Output 'Not running'; exit 0 }
if ($Running.CommandLine -notmatch 'projects\.suno_browser_service\.apps\.api\.main') { throw 'PID now belongs to another process; refusing to stop it.' }
Set-Content -LiteralPath (Join-Path $DataDir 'shutdown.request') -Value 'stop' -Encoding ascii
for ($Attempt = 0; $Attempt -lt 30; $Attempt++) {
    if (-not (Get-Process -Id $Current.pid -ErrorAction SilentlyContinue)) { Write-Output 'Stopped'; exit 0 }
    Start-Sleep -Seconds 1
}
Write-Output 'Shutdown requested. The service will close its current browser operation safely; no new jobs will start.'
