#requires -RunAsAdministrator
$ErrorActionPreference = "Stop"
$studiesRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$logDir = Join-Path $studiesRoot "Codebase\LMS\runtime\logs"
New-Item -ItemType Directory -Path $logDir -Force | Out-Null
$report = Join-Path $logDir ("wsl-prerequisites-{0}.txt" -f [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ"))
$utf8 = [Text.UTF8Encoding]::new($false)
function Write-Report([string]$Text) {
    [IO.File]::AppendAllText($report, $Text + [Environment]::NewLine, $utf8)
    Write-Output $Text
}

$computer = Get-CimInstance Win32_ComputerSystem
$os = Get-CimInstance Win32_OperatingSystem
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
Write-Report "WSL prerequisite setup UTC: $([DateTime]::UtcNow.ToString('o'))"
Write-Report "OS: $($os.Caption), build $($os.BuildNumber)"
Write-Report "Manufacturer/model: $($computer.Manufacturer) / $($computer.Model); HypervisorPresent=$($computer.HypervisorPresent); RAM_GB=$([math]::Round($computer.TotalPhysicalMemory/1GB,1))"
Write-Report "CPU: $($cpu.Name); firmware virtualization=$($cpu.VirtualizationFirmwareEnabled); SLAT=$($cpu.SecondLevelAddressTranslationExtensions); VMX=$($cpu.VMMonitorModeExtensions)"
$restartNeeded = $false

foreach ($feature in @("Microsoft-Windows-Subsystem-Linux", "VirtualMachinePlatform")) {
    $state = (Get-WindowsOptionalFeature -Online -FeatureName $feature).State
    Write-Report "$feature before: $state"
    if ($state -ne "Enabled") {
        $result = Enable-WindowsOptionalFeature -Online -FeatureName $feature -All -NoRestart
        Write-Report "$feature enable result: restart=$($result.RestartNeeded); state=$($result.State)"
        if ($result.RestartNeeded) { $restartNeeded = $true }
    }
}

try {
    $installOutput = & wsl.exe --install --no-distribution 2>&1
    $installCode = $LASTEXITCODE
    Write-Report "wsl --install --no-distribution exit code: $installCode"
    foreach ($line in $installOutput) { Write-Report ([string]$line) }
    if (($installOutput | Out-String) -match "restart|reboot|pending") { $restartNeeded = $true }
} catch {
    Write-Report "WSL bootstrap error: $($_.Exception.Message)"
}

foreach ($feature in @("Microsoft-Windows-Subsystem-Linux", "VirtualMachinePlatform")) {
    try {
        $state = (Get-WindowsOptionalFeature -Online -FeatureName $feature).State
        Write-Report "$feature after: $state"
        if ($state -eq "EnablePending") { $restartNeeded = $true }
    } catch {
        Write-Report "Could not recheck $feature`: $($_.Exception.Message)"
    }
}

if ($computer.HypervisorPresent -eq $true) {
    Write-Report "Windows reports an active hypervisor; firmware virtualization was available to this boot. WMI virtualization flags may be masked while the hypervisor is active. No BIOS/UEFI change is indicated by this inspection."
} elseif ($cpu.VirtualizationFirmwareEnabled -ne $true -or $cpu.SecondLevelAddressTranslationExtensions -ne $true) {
    Write-Report "Human-only firmware check may be required: no active hypervisor was detected and Windows reports firmware virtualization or SLAT unavailable. No BIOS/UEFI settings were changed."
}
if ($restartNeeded) {
    Write-Report "RESTART REQUIRED. This script will not restart Windows."
} else {
    Write-Report "No restart was requested by the feature installer. Verify WSL after setup."
}
Write-Output "Report: $report"
