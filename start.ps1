param(
    [ValidateSet('ai_video_management', 'spec_driven', 'drama_reverse_engine', 'jimeng_web_bridge')]
    [string]$Project = 'ai_video_management',
    [switch]$NoReload,
    [ValidateRange(1, 65535)]
    [int]$Port = 8766
)

$ErrorActionPreference = 'Stop'
$projectPath = Join-Path $PSScriptRoot "projects\$Project"
$pythonCandidates = @(
    (Join-Path $projectPath '.venv\Scripts\python.exe'),
    (Join-Path $PSScriptRoot '.venv\Scripts\python.exe')
)
$pythonPath = $null
foreach ($candidate in $pythonCandidates) {
    if (Test-Path -LiteralPath $candidate) {
        try {
            & $candidate --version 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) {
                $pythonPath = $candidate
                break
            }
        } catch {
            continue
        }
    }
}
if (-not $pythonPath) {
    throw "No working Python environment found. Create projects\$Project\.venv and install projects\$Project\requirements.txt, then retry."
}

Push-Location $projectPath
$previousPort = $env:BACKEND_PORT
try {
    if ($Project -eq 'ai_video_management') { $env:BACKEND_PORT = "$Port" }
    $backendArgs = @('-m', 'apps.api.main')
    if ($NoReload -and $Project -eq 'ai_video_management') { $backendArgs += '--no-reload' }
    & $pythonPath @backendArgs
    $backendExitCode = $LASTEXITCODE
} finally {
    $env:BACKEND_PORT = $previousPort
    Pop-Location
}
exit $backendExitCode
