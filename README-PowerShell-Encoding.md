# PowerShell 编码问题解决方案

## 问题描述
在 Windows PowerShell 中执行命令时，如果路径或输出包含中文字符，可能会出现乱码问题。

## 解决方案

### 方法 1: 临时设置（推荐用于单次会话）

在 PowerShell 中执行以下命令：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null
```

### 方法 2: 使用提供的脚本

运行项目根目录下的 `setup-encoding.ps1` 脚本：

```powershell
.\setup-encoding.ps1
```

### 方法 3: 永久设置（推荐）

将以下内容添加到 PowerShell 配置文件中：

1. 检查配置文件是否存在：
```powershell
Test-Path $PROFILE
```

2. 如果不存在，创建配置文件：
```powershell
New-Item -Path $PROFILE -Type File -Force
```

3. 编辑配置文件，添加以下内容：
```powershell
notepad $PROFILE
```

在文件中添加：
```powershell
# 设置 UTF-8 编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null
```

4. 保存并重新加载配置：
```powershell
. $PROFILE
```

### 方法 4: 在 Cursor 中设置

如果是在 Cursor 中执行命令，可以在命令前添加编码设置：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; [Console]::InputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8; chcp 65001 | Out-Null; Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing | Select-Object -ExpandProperty Content
```

## 验证设置

执行以下命令验证编码设置是否生效：

```powershell
[Console]::OutputEncoding.EncodingName
$OutputEncoding.EncodingName
```

应该显示 "Unicode (UTF-8)"。

## 注意事项

- 方法 1 和方法 2 只在当前 PowerShell 会话中有效
- 方法 3 是永久设置，对所有新的 PowerShell 会话都有效
- 如果路径中包含中文字符，确保文件系统也支持 UTF-8 编码

