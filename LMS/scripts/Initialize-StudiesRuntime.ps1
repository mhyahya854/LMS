$ErrorActionPreference = "Stop"
$studiesRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$codeRoot = Join-Path $studiesRoot "Codebase\LMS"
$runtimeRoot = Join-Path $codeRoot "runtime"
$logDir = Join-Path $runtimeRoot "logs"
$envFile = Join-Path $runtimeRoot ".env"
$compose = Join-Path $runtimeRoot "compose.yaml"
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

function New-HexSecret {
    $bytes = [byte[]]::new(32)
    $generator = [Security.Cryptography.RandomNumberGenerator]::Create()
    try { $generator.GetBytes($bytes) } finally { $generator.Dispose() }
    return [BitConverter]::ToString($bytes).Replace("-", "")
}

if (-not (Test-Path -LiteralPath $envFile)) {
    $lines = @(
        "MARIADB_ROOT_PASSWORD=$(New-HexSecret)"
        "SITE_ADMIN_PASSWORD=$(New-HexSecret)"
        "SITE_NAME=studies.localhost"
    )
    [IO.File]::WriteAllLines($envFile, $lines, [Text.UTF8Encoding]::new($false))
    Write-Output "Created ignored local runtime credentials at runtime\.env. Keep this file private."
} else {
    Write-Output "Keeping existing runtime credentials; runtime\.env will not be overwritten."
}

$requiredKeys = @("MARIADB_ROOT_PASSWORD", "SITE_ADMIN_PASSWORD", "SITE_NAME")
$envText = Get-Content -LiteralPath $envFile -Raw
foreach ($key in $requiredKeys) {
    if ($envText -notmatch "(?m)^$key=.+$") { throw "runtime\.env is missing $key; preserve it and repair that entry before retrying." }
}

$docker = Get-Command docker -ErrorAction SilentlyContinue
if (-not $docker) { throw "Docker CLI is not installed. Install Docker Desktop, restart Windows, then retry." }

$composeArgs = @("compose", "--project-directory", $runtimeRoot, "--env-file", $envFile, "-f", $compose)
& docker @composeArgs config --quiet
if ($LASTEXITCODE -ne 0) { throw "Docker Compose configuration validation failed with exit code $LASTEXITCODE." }

Write-Output "Starting MariaDB, Redis, and the Frappe development container."
& docker @composeArgs up -d
if ($LASTEXITCODE -ne 0) { throw "Docker Compose startup failed with exit code $LASTEXITCODE." }

$ready = $false
for ($attempt = 0; $attempt -lt 90; $attempt++) {
    & docker @composeArgs exec -T mariadb healthcheck.sh --connect --innodb_initialized *> $null
    if ($LASTEXITCODE -eq 0) { $ready = $true; break }
    Start-Sleep -Seconds 2
}
if (-not $ready) { throw "MariaDB did not become healthy. Inspect `docker compose logs mariadb` before retrying." }

Write-Output "Bootstrapping Frappe Framework v16, Frappe Learning v2.63.0, and Studies Hub. This can take several minutes."
& docker @composeArgs exec -T frappe bash /workspace/project/scripts/bootstrap-runtime.sh
if ($LASTEXITCODE -ne 0) { throw "Runtime bootstrap stopped with exit code $LASTEXITCODE. Existing runtime files and volumes were preserved." }

Write-Output "Starting the local Bench process."
& docker @composeArgs exec -d frappe bash -lc 'cd /workspace/development/frappe-bench && if ! pgrep -af "[b]ench start" >/dev/null; then nohup bench start >> /workspace/development/bench.log 2>&1 < /dev/null & echo $! > /workspace/development/bench-start.pid; fi'
if ($LASTEXITCODE -ne 0) { throw "Could not start Bench. Inspect runtime\bench\bench.log." }

$healthUrl = "http://127.0.0.1:8000/lms"
$healthy = $false
for ($attempt = 0; $attempt -lt 90; $attempt++) {
    try {
        $response = Invoke-WebRequest -Uri $healthUrl -TimeoutSec 4 -UseBasicParsing
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) { $healthy = $true; break }
    } catch {}
    Start-Sleep -Seconds 2
}
if (-not $healthy) { throw "Bench did not respond at $healthUrl. Inspect runtime\bench\bench.log and Docker service logs." }
Write-Output "Local LMS is responding at $healthUrl. Use Launch Studies.cmd for future starts."
