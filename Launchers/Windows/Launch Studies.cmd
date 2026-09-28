@echo off
setlocal
for %%I in ("%~dp0..\..\..") do set "STUDIES_ROOT=%%~fI"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%STUDIES_ROOT%\Codebase\LMS\scripts\Start-Studies.ps1"
if errorlevel 1 (
  echo.
  echo Studies could not start. See Codebase\LMS\runtime\logs\launch.log.
)
exit /b %ERRORLEVEL%
