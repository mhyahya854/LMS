$ErrorActionPreference = "Stop"
$studiesRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$codeRoot = Join-Path $studiesRoot "Codebase\LMS"
$runtimeRoot = Join-Path $codeRoot "runtime"
$logDir = Join-Path $runtimeRoot "logs"
New-Item -ItemType Directory -Path $logDir -Force | Out-Null
$log = Join-Path $logDir "launch.log"
$compose = Join-Path $runtimeRoot "compose.yaml"
$envFile = Join-Path $runtimeRoot ".env"

function Write-Log([string]$Text) {
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Text
    Add-Content -LiteralPath $log -Value $line
    Write-Output $line
}

Write-Log "Studies root: $studiesRoot"
$docker = Get-Command docker -ErrorAction SilentlyContinue
if (-not $docker) { Write-Log "Docker CLI is not installed. Complete WSL/Docker setup first."; exit 10 }
if (-not (Test-Path -LiteralPath $compose)) { Write-Log "Project Compose configuration is not provisioned yet; no services were started."; exit 11 }
if (-not (Test-Path -LiteralPath $envFile)) { Write-Log "Runtime secrets are not initialized. Run scripts\Initialize-StudiesRuntime.ps1 first."; exit 11 }

$desktopCandidates = @(
    (Join-Path $env:LOCALAPPDATA "Programs\DockerDesktop\Docker Desktop.exe"),
    (Join-Path $env:ProgramFiles "Docker\Docker\Docker Desktop.exe")
)
$desktopExe = $desktopCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if ($desktopExe) {
    if (-not (Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue)) {
        Write-Log "Starting Docker Desktop."
        Start-Process -FilePath $desktopExe
    }
}

$composeArgs = @("compose", "--project-directory", $runtimeRoot, "--env-file", $envFile, "-f", $compose)

$dockerReady = $false
for ($attempt = 0; $attempt -lt 60; $attempt++) {
    # Docker emits connection errors on stderr while Docker Desktop is still
    # starting. Redirect only stderr so this remains a retryable probe under
    # ErrorActionPreference = Stop.
    & docker info 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $dockerReady = $true; break }
    Start-Sleep -Seconds 2
}
if (-not $dockerReady) { Write-Log "Docker engine did not become ready within 120 seconds."; exit 12 }

Write-Log "Starting the Studies Compose project."
& docker @composeArgs up -d
if ($LASTEXITCODE -ne 0) { Write-Log "docker compose up failed with exit code $LASTEXITCODE."; exit 13 }

$benchProcesses = & docker @composeArgs exec -T frappe bash -lc 'pgrep -af "[b]ench start" || true' 2>$null
if (-not $benchProcesses) {
    Write-Log "Starting Bench inside the Frappe development container."
    & docker @composeArgs exec -d frappe bash -lc 'cd /workspace/development/frappe-bench && nohup bench start >> /workspace/development/bench.log 2>&1 < /dev/null & echo $! > /workspace/development/bench-start.pid'
    if ($LASTEXITCODE -ne 0) { Write-Log "Could not start Bench; inspect runtime\bench\bench.log."; exit 14 }
}

$healthUrl = "http://127.0.0.1:8000/lms"
$healthy = $false
for ($attempt = 0; $attempt -lt 60; $attempt++) {
    try {
        $response = Invoke-WebRequest -Uri $healthUrl -TimeoutSec 4 -UseBasicParsing
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) { $healthy = $true; break }
    } catch {}
    Start-Sleep -Seconds 2
}
if (-not $healthy) { Write-Log "Compose started, but LMS did not respond at $healthUrl; inspect Docker service logs and runtime\bench\bench.log."; exit 15 }
Write-Log "LMS health check passed: $healthUrl"
Start-Process $healthUrl
