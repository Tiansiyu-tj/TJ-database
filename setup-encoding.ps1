# PowerShell UTF-8 Encoding Setup Script
# Fix Chinese path and output encoding issues

# Set console output encoding to UTF-8 FIRST
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# Set PowerShell output encoding
$OutputEncoding = [System.Text.Encoding]::UTF8

# Set code page to UTF-8 (65001)
$null = chcp 65001

# Set environment variables
$env:PYTHONIOENCODING = "utf-8"
$env:LC_ALL = "zh_CN.UTF-8"

# Clear screen to apply encoding changes
Clear-Host

# Output status using English to avoid encoding issues
Write-Host "[SUCCESS] PowerShell encoding has been set to UTF-8" -ForegroundColor Green
Write-Host "Current output encoding: $([Console]::OutputEncoding.EncodingName)" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now use Chinese characters in paths and commands without encoding issues." -ForegroundColor Yellow

