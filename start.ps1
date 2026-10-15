<#
.SYNOPSIS
    Restart a project's backend and frontend dev server in the background.

.DESCRIPTION
    Stops any previous backend / frontend of the project (processes this script
    started, plus whatever is listening on the project's ports), then starts the
    backend and the Vite dev server as hidden background processes with logs in
    projects\<Project>\logs\. Run it again to restart; use -Stop to only stop.

.EXAMPLE
    .\start.ps1                  # restart ai_video_management backend + frontend
    .\start.ps1 -NoReload        # backend without uvicorn auto-reload
    .\start.ps1 -BackendOnly     # backend only (serves the built static bundle)
    .\start.ps1 -Stop            # stop both
#>
param(
    [ValidateSet('ai_video_management', 'spec_driven')]
    [string]$Project = 'ai_video_management',
    [switch]$NoReload,
    [ValidateRange(1, 65535)]
    [int]$Port = 8766,
    [switch]$BackendOnly,
    [switch]$Stop
)

$ErrorActionPreference = 'Stop'

# Backend / Vite dev-server ports per project. FrontendPort $null = no dev server.
# -Port only applies to ai_video_management (its backend and Vite proxy read BACKEND_PORT).
$projectConfig = @{
    'ai_video_management'  = @{ BackendPort = $Port; FrontendPort = 5174; BackendArgs = @() }
    'spec_driven'          = @{ BackendPort = 8765;  FrontendPort = 5173; BackendArgs = @() }
}
$config = $projectConfig[$Project]
if ($Project -eq 'ai_video_management' -and $NoReload) { $config.BackendArgs = @('--no-reload') }

$projectPath = Join-Path $PSScriptRoot "projects\$Project"
$uiPath = Join-Path $projectPath 'apps\ui'
$logDir = Join-Path $projectPath 'logs'
$pidFile = Join-Path $logDir 'start.pids'
$backendPattern = 'apps\.api\.main|multiprocessing'
$frontendPattern = 'vite|npm'

function Get-ProcessInfo([int]$ProcessId) {
    Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId" -ErrorAction SilentlyContinue
}

# Climb from a port owner to the outermost launcher (venv python redirector,
# uvicorn reloader, npm/cmd wrapper) so killing that tree leaves nothing behind.
function Get-LaunchRoot([int]$ProcessId, [string]$Pattern) {
    $current = Get-ProcessInfo $ProcessId
    if (-not $current) { return $null }
    while ($true) {
        $parent = Get-ProcessInfo $current.ParentProcessId
        if (-not $parent) { break }
        if ($parent.Name -notin @('python.exe', 'node.exe', 'cmd.exe')) { break }
        if ($parent.CommandLine -notmatch $Pattern) { break }
        $current = $parent
    }
    return $current
}

function Get-ListeningPids([int]$LocalPort) {
    Get-NetTCPConnection -State Listen -LocalPort $LocalPort -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique |
        Where-Object { $_ -gt 0 }
}

function Wait-PortFree([int]$LocalPort, [int]$TimeoutSeconds = 10) {
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if (-not (Get-ListeningPids $LocalPort)) { return $true }
        Start-Sleep -Milliseconds 250
    }
    return -not (Get-ListeningPids $LocalPort)
}

function Stop-Tree([int]$ProcessId, [string]$Label) {
    $info = Get-ProcessInfo $ProcessId
    if (-not $info) { return }
    Write-Host "Stopping $Label (PID $ProcessId, $($info.Name))"
    & taskkill.exe /PID $ProcessId /T /F 2>&1 | Out-Null
}

function Stop-Previous {
    $roots = @{}
    # 1. Processes recorded by the previous run (skip if the PID was reused).
    if (Test-Path -LiteralPath $pidFile) {
        foreach ($line in Get-Content -LiteralPath $pidFile) {
            $parts = $line -split '\s+'
            if ($parts.Count -lt 2) { continue }
            $pattern = if ($parts[0] -eq 'backend') { $backendPattern } else { $frontendPattern }
            $info = Get-ProcessInfo ([int]$parts[1])
            if ($info -and $info.CommandLine -match $pattern) { $roots[[int]$parts[1]] = $parts[0] }
        }
        Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
    }
    # 2. Anything still listening on the project's ports (e.g. started by hand).
    $ports = @(@{ Port = $config.BackendPort; Label = 'backend'; Pattern = $backendPattern })
    if ($config.FrontendPort) {
        $ports += @{ Port = $config.FrontendPort; Label = 'frontend'; Pattern = $frontendPattern }
    }
    foreach ($entry in $ports) {
        foreach ($owner in Get-ListeningPids $entry.Port) {
            $root = Get-LaunchRoot $owner $entry.Pattern
            if (-not $root) { continue }
            if ($root.CommandLine -notmatch $entry.Pattern) {
                throw "Port $($entry.Port) is held by an unrelated process (PID $($root.ProcessId), $($root.Name)); not stopping it. Free the port or use -Port."
            }
            $roots[[int]$root.ProcessId] = $entry.Label
        }
    }
    foreach ($processId in $roots.Keys) { Stop-Tree $processId $roots[$processId] }
    foreach ($entry in $ports) {
        if (-not (Wait-PortFree $entry.Port)) {
            throw "Port $($entry.Port) is still in use after stopping the old $($entry.Label). Check: Get-NetTCPConnection -LocalPort $($entry.Port)"
        }
    }
    if ($roots.Count -eq 0) { Write-Host 'No previous processes found.' }
}

function Find-Python {
    $candidates = @(
        (Join-Path $projectPath '.venv\Scripts\python.exe'),
        (Join-Path $PSScriptRoot '.venv\Scripts\python.exe')
    )
    foreach ($candidate in $candidates) {
        if (-not (Test-Path -LiteralPath $candidate)) { continue }
        try {
            & $candidate --version 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) { return $candidate }
        } catch {
            continue
        }
    }
    throw "No working Python environment found. Create projects\$Project\.venv and install projects\$Project\requirements.txt, then retry."
}

function Start-Logged([string]$Label, [string]$FilePath, [string[]]$ArgumentList, [string]$WorkingDirectory) {
    $stdout = Join-Path $logDir "$Label.out.log"
    $stderr = Join-Path $logDir "$Label.err.log"
    $process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -WorkingDirectory $WorkingDirectory `
        -RedirectStandardOutput $stdout -RedirectStandardError $stderr -WindowStyle Hidden -PassThru
    $script:startedPids += "$Label $($process.Id)"
    return $process
}

# Other tools (file watchers, indexers) may hold logs\ files briefly; retry.
function Save-Pids {
    for ($attempt = 1; $attempt -le 10; $attempt++) {
        try {
            Set-Content -LiteralPath $pidFile -Value $script:startedPids -Encoding ascii
            return
        } catch {
            if ($attempt -eq 10) { Write-Warning "Could not write $pidFile; -Stop will fall back to port lookup." }
            Start-Sleep -Milliseconds 200
        }
    }
}

function Wait-Listening($Process, [int]$LocalPort, [string]$Label, [int]$TimeoutSeconds = 60) {
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if (Get-ListeningPids $LocalPort) { return }
        if ($Process.HasExited) { break }
        Start-Sleep -Milliseconds 500
    }
    Write-Host "---- $Label logs ($logDir\$Label.*.log) ----"
    foreach ($suffix in @('out', 'err')) {
        $log = Join-Path $logDir "$Label.$suffix.log"
        if (Test-Path -LiteralPath $log) { Get-Content -LiteralPath $log -Tail 20 }
    }
    throw "$Label did not start listening on port $LocalPort."
}

New-Item -ItemType Directory -Force -Path $logDir | Out-Null
Stop-Previous
if ($Stop) { return }

$startFrontend = $config.FrontendPort -and -not $BackendOnly
$pythonPath = Find-Python
if ($startFrontend) {
    $nodePath = (Get-Command node -ErrorAction Stop).Source
    if (-not (Test-Path -LiteralPath (Join-Path $uiPath 'node_modules'))) {
        Write-Host "Installing frontend dependencies in $uiPath ..."
        Push-Location $uiPath
        try { & npm install; if ($LASTEXITCODE -ne 0) { throw 'npm install failed.' } } finally { Pop-Location }
    }
}

$script:startedPids = @()
$previousPort = $env:BACKEND_PORT
try {
    # Inherited by both children: the backend binds it, the Vite proxy targets it.
    if ($Project -eq 'ai_video_management') { $env:BACKEND_PORT = "$($config.BackendPort)" }

    $backend = Start-Logged 'backend' $pythonPath (@('-m', 'apps.api.main') + $config.BackendArgs) $projectPath
    if ($startFrontend) {
        $viteArgs = @('node_modules\vite\bin\vite.js', '--port', "$($config.FrontendPort)", '--strictPort')
        $frontend = Start-Logged 'frontend' $nodePath $viteArgs $uiPath
    }
} finally {
    $env:BACKEND_PORT = $previousPort
    if ($script:startedPids) { Save-Pids }
}

Wait-Listening $backend $config.BackendPort 'backend'
Write-Host "Backend   http://127.0.0.1:$($config.BackendPort)/  (PID $($backend.Id))"
if ($startFrontend) {
    Wait-Listening $frontend $config.FrontendPort 'frontend'
    Write-Host "Frontend  http://127.0.0.1:$($config.FrontendPort)/  (PID $($frontend.Id))"
}
Write-Host "Logs in $logDir. Stop with: .\start.ps1 -Project $Project -Stop"
