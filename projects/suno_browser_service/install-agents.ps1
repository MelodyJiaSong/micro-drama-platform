param([ValidateSet('Both','Claude','Codex')][string]$Client = 'Both')
$ErrorActionPreference = 'Stop'
$SunoRepo = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$SunoPython = Join-Path $SunoRepo '.venv/Scripts/python.exe'
$SunoMcp = Join-Path $PSScriptRoot 'apps/mcp/main.py'
if (-not (Test-Path -LiteralPath $SunoPython)) { throw 'Run setup.ps1 first.' }
Push-Location $SunoRepo
try {
    if ($Client -in @('Both','Claude')) {
        if (-not (Get-Command claude -ErrorAction SilentlyContinue)) { throw 'Claude Code CLI not found.' }
        $SunoClaudeConfig = Join-Path $SunoRepo '.mcp.json'
        $SunoClaudeEntry = $null
        if (Test-Path -LiteralPath $SunoClaudeConfig) {
            $SunoClaudeEntry = (Get-Content -LiteralPath $SunoClaudeConfig -Raw | ConvertFrom-Json).mcpServers.'suno-browser'
        }
        if ($SunoClaudeEntry) {
            if ($SunoClaudeEntry.command -ne $SunoPython -or ($SunoClaudeEntry.args -join '|') -ne $SunoMcp) { throw 'Existing Claude suno-browser entry differs; preserved. Inspect it before replacing.' }
            Write-Output 'Claude suno-browser already registered.'
        } else {
            & claude mcp add --scope project --transport stdio suno-browser -- $SunoPython $SunoMcp
            if ($LASTEXITCODE -ne 0) { throw 'Claude MCP registration failed; existing entries are preserved.' }
        }
    }
    if ($Client -in @('Both','Codex')) {
        if (-not (Get-Command codex -ErrorAction SilentlyContinue)) { throw 'Codex CLI not found.' }
        $SunoSavedPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        $SunoCodexRaw = & codex mcp get suno-browser --json 2>$null
        $SunoCodexFound = $LASTEXITCODE -eq 0
        $ErrorActionPreference = $SunoSavedPreference
        if ($SunoCodexFound) {
            $SunoCodexEntry = ($SunoCodexRaw | ConvertFrom-Json).transport
            if ($SunoCodexEntry.command -ne $SunoPython -or ($SunoCodexEntry.args -join '|') -ne $SunoMcp) { throw 'Existing Codex suno-browser entry differs; preserved. Inspect it before replacing.' }
            Write-Output 'Codex suno-browser already registered.'
        } else {
            & codex mcp add suno-browser -- $SunoPython $SunoMcp
            if ($LASTEXITCODE -ne 0) { throw 'Codex MCP registration failed.' }
        }
    }
    Write-Output 'MCP entry registered. Restart the agent session to discover suno_* tools. No credentials were copied.'
} finally { Pop-Location }
