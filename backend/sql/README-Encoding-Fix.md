# MySQL 中文编码问题解决方案

## 问题描述

执行 SQL 文件时出现以下错误：
```
ERROR 1366 (HY000): Incorrect string value: '\xA6\x82' for column 'station_name' at row 1
```

这是因为 MySQL 客户端连接的字符集不是 UTF-8，导致无法正确插入中文字符。

## 解决方案

### 方法 1: 在 MySQL 客户端中手动设置（推荐）

在 MySQL 命令行中执行以下命令：

```sql
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;
```

然后再执行 SQL 文件：

```sql
source F:/大三上/数据库课设/代码/backend/sql/add_crud_tables.sql;
```

### 方法 2: 使用修复后的 SQL 文件（已自动修复）

所有 SQL 文件已经在开头添加了字符集设置，直接执行即可：

```sql
source F:/大三上/数据库课设/代码/backend/sql/add_crud_tables.sql;
```

### 方法 3: 永久设置 MySQL 客户端编码

编辑 MySQL 配置文件 `my.ini`（Windows）或 `my.cnf`（Linux），在 `[client]` 和 `[mysql]` 部分添加：

```ini
[client]
default-character-set=utf8mb4

[mysql]
default-character-set=utf8mb4
```

然后重启 MySQL 服务。

### 方法 4: 在连接时指定字符集

使用 MySQL 客户端连接时指定字符集：

```bash
mysql -u root -p --default-character-set=utf8mb4
```

或者在连接后立即执行：

```sql
SET NAMES utf8mb4;
```

## 验证字符集设置

执行以下 SQL 查看当前字符集设置：

```sql
SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'collation%';
```

应该看到：
- `character_set_client` = `utf8mb4`
- `character_set_connection` = `utf8mb4`
- `character_set_results` = `utf8mb4`
- `character_set_database` = `utf8mb4`

## 检查数据库和表的字符集

```sql
-- 检查数据库字符集
SHOW CREATE DATABASE jiading_commute;

-- 检查表字符集
SHOW CREATE TABLE user_favorite;
SHOW CREATE TABLE congestion_feedback;
```

确保都是 `utf8mb4` 或 `utf8mb4_unicode_ci`。

## 如果仍然有问题

1. **检查 SQL 文件编码**：确保 SQL 文件本身以 UTF-8 编码保存
2. **检查终端编码**：确保终端支持 UTF-8（参考 `setup-encoding.ps1`）
3. **重新创建表**：如果表已经创建但字符集不对，需要重新创建：

```sql
ALTER TABLE user_favorite CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE congestion_feedback CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```


