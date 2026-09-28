$ErrorActionPreference = "Continue"
$studiesRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$logDir = Join-Path $studiesRoot "Codebase\LMS\runtime\logs"
New-Item -ItemType Directory -Path $logDir -Force | Out-Null
$report = Join-Path $logDir ("windows-runtime-inspection-{0}.txt" -f [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ"))
$utf8 = [Text.UTF8Encoding]::new($false)
function Add-ReportText([string]$Text) { [IO.File]::AppendAllText($report, $Text, $utf8) }
Add-ReportText "Inspection UTC: $([DateTime]::UtcNow.ToString('o'))`r`n"
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber,OSArchitecture | Format-List | Out-String | ForEach-Object { Add-ReportText $_ }
$computer = Get-CimInstance Win32_ComputerSystem
$computer | Select-Object Manufacturer,Model,HypervisorPresent,@{n="RAM_GB";e={[math]::Round($_.TotalPhysicalMemory/1GB,1)}} | Format-List | Out-String | ForEach-Object { Add-ReportText $_ }
Get-CimInstance Win32_Processor | Select-Object -First 1 Name,NumberOfCores,VirtualizationFirmwareEnabled,SecondLevelAddressTranslationExtensions,VMMonitorModeExtensions | Format-List | Out-String | ForEach-Object { Add-ReportText $_ }
Get-PSDrive C | Select-Object Name,@{n="Free_GB";e={[math]::Round($_.Free/1GB,1)}} | Format-List | Out-String | ForEach-Object { Add-ReportText $_ }
foreach ($feature in @("Microsoft-Windows-Subsystem-Linux","VirtualMachinePlatform")) {
    try {
        Get-WindowsOptionalFeature -Online -FeatureName $feature | Select-Object FeatureName,State | Format-List | Out-String | ForEach-Object { Add-ReportText $_ }
    } catch {
        Add-ReportText "Feature query failed for ${feature}: $($_.Exception.Message)`r`n"
    }
}
try { bcdedit /enum 2>&1 | Out-String | ForEach-Object { Add-ReportText $_ } } catch { Add-ReportText "$($_.Exception.Message)`r`n" }
Write-Output "Wrote $report"
Get-Content -LiteralPath $report
