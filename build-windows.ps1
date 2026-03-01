# Build Windows executable for ATEM Media File Generator
# Uses PyInstaller with selective hidden imports

param(
    [switch]$Help = $false
)

if ($Help) {
    Write-Host "Usage: .\build-windows.ps1"
    Write-Host ""
    Write-Host "Builds the ATEM Media File Generator application for Windows."
    Write-Host "Requires Python 3.9+, pip, and a virtual environment (venv)."
    exit 0
}

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "ATEM Media File Generator - Windows Build" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Error: Virtual environment not found." -ForegroundColor Red
    Write-Host "Run: python -m venv venv"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Check PyInstaller
Write-Host "Checking PyInstaller installation..." -ForegroundColor Yellow
$pyinstaller = python -m pip show pyinstaller 2>$null
if (-not $pyinstaller) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
Get-ChildItem "*.spec" | Remove-Item -Force 2>$null

# Build executable
Write-Host "Building executable..." -ForegroundColor Yellow
python -m PyInstaller `
    --onedir `
    --name "ATEM-Media-Generator" `
    --hidden-import=PyQt5.QtWidgets `
    --hidden-import=PyQt5.QtCore `
    --hidden-import=PyQt5.QtGui `
    --hidden-import=PyQt5.QtPrintSupport `
    --hidden-import=PyQt5.QtSvg `
    --hidden-import=PIL `
    --hidden-import=PIL.ImageTk `
    --collect-data=PIL `
    --windowed `
    main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "✅ Windows Build Successful!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location:" -ForegroundColor Cyan
    Write-Host "  dist\ATEM-Media-Generator\ATEM-Media-Generator.exe"
    Write-Host ""
    Write-Host "To run the application:" -ForegroundColor Yellow
    Write-Host "  .\dist\ATEM-Media-Generator\ATEM-Media-Generator.exe"
    Write-Host ""
    Write-Host "To create a portable zip archive:" -ForegroundColor Yellow
    Write-Host "  powershell Compress-Archive -Path 'dist\ATEM-Media-Generator' -DestinationPath 'ATEM-Media-Generator-windows.zip'"
    Write-Host ""
    Write-Host "Application details:"
    $exePath = "dist\ATEM-Media-Generator\ATEM-Media-Generator.exe"
    if (Test-Path $exePath) {
        $fileSize = (Get-Item $exePath).Length / 1MB
        Write-Host "  Size: $([Math]::Round($fileSize, 2)) MB"
    }
    Write-Host "=========================================" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Build failed! Check error messages above." -ForegroundColor Red
    exit 1
}
