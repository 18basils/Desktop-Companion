# Desktop Companion - Background Launcher for PowerShell
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $scriptDir) { $scriptDir = $PWD.Path }

$pythonw = "$env:LOCALAPPDATA\Programs\Python\Python313\pythonw.exe"
if (-not (Test-Path $pythonw)) {
    $pythonw = Join-Path $scriptDir ".venv\Scripts\pythonw.exe"
}
if (-not (Test-Path $pythonw)) {
    $pythonw = "pythonw.exe"
}

$script = Join-Path $scriptDir "companion.py"

Start-Process -FilePath $pythonw -ArgumentList "`"$script`"" -WorkingDirectory $scriptDir

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Desktop Companion service is now running in background! " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  * The avatar will walk onto the left side of your screen." -ForegroundColor Yellow
Write-Host "  * Tray Icon: Look for the blue 💧 icon next to your clock." -ForegroundColor Yellow
Write-Host "    (If hidden, click the '^' Show Hidden Icons arrow)" -ForegroundColor DarkYellow
Write-Host "  * Right-click 💧 icon to open 'Settings' or 'Exit'." -ForegroundColor Yellow
Write-Host ""
Write-Host "You can now safely CLOSE this PowerShell window." -ForegroundColor Green
Write-Host ""
