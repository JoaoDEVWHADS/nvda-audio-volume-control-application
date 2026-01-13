# Install dependencies script for NVDA Audio Volume Control Add-on
# This script bundles Python dependencies with the add-on

Write-Host "Installing Python dependencies for NVDA Audio Volume Control Add-on..." -ForegroundColor Cyan
Write-Host ""

# Create lib directory if it doesn't exist
$libDir = "addon\lib"
if (-not (Test-Path $libDir)) {
    New-Item -ItemType Directory -Path $libDir | Out-Null
}

# Install dependencies to addon/lib
Write-Host "Installing pycaw, comtypes, and psutil to addon\lib..." -ForegroundColor Yellow
pip install -r requirements.txt --target addon\lib --upgrade

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Dependencies are now bundled in: addon\lib\" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now build the add-on with: scons" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "✗ Error installing dependencies!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure pip is installed and try again." -ForegroundColor Red
    exit 1
}
