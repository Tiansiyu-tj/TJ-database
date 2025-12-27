# PowerShell UTF-8 编码设置脚本
# 解决中文路径和输出乱码问题

# 首先设置控制台输出编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# 设置 PowerShell 输出编码
$OutputEncoding = [System.Text.Encoding]::UTF8

# 设置代码页为 UTF-8 (65001)
$null = chcp 65001

# 设置环境变量
$env:PYTHONIOENCODING = "utf-8"
$env:LC_ALL = "zh_CN.UTF-8"

# 清除屏幕以应用编码更改
Clear-Host

# 使用 UTF-8 字节数组输出中文（避免文件编码问题）
$successMsg = [System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("PowerShell 编码已设置为 UTF-8"))
$encodingMsg = [System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("当前输出编码: "))

Write-Host "[SUCCESS] $successMsg" -ForegroundColor Green
Write-Host "$encodingMsg$([Console]::OutputEncoding.EncodingName)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now you can use Chinese characters in paths and commands." -ForegroundColor Yellow

