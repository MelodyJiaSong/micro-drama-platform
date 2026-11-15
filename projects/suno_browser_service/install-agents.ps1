$ErrorActionPreference = 'Stop'
$SunoRepo = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$SunoPython = Join-Path $SunoRepo '.venv/Scripts/python.exe'
$SunoMcp = Join-Path $PSScriptRoot 'apps/mcp/main.py'
if (-not (Test-Path -LiteralPath $SunoPython)) { throw 'Run setup.ps1 first.' }
$SharedConfig = Join-Path $SunoRepo '.agents/mcp.json'
$Config = Get-Content -LiteralPath $SharedConfig -Raw -Encoding utf8 | ConvertFrom-Json
$Entry = $Config.mcpServers.'suno-browser'
if (-not $Entry -or $Entry.command -ne $SunoPython -or ($Entry.args -join '|') -ne $SunoMcp) {
    throw 'Shared suno-browser definition differs from this checkout. Update .agents/mcp.json, then rerun; existing settings preserved.'
}
& $SunoPython (Join-Path $SunoRepo 'tools/sync_agent_config.py') --fix
if ($LASTEXITCODE -ne 0) { throw 'Shared MCP configuration sync failed.' }
Write-Output 'Kimi and Codex project MCP configurations synchronized. Restart the desired client and inspect its MCP connection. No user settings or credentials were changed.'
