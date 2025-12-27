# Shanghai Metro 数据库说明 🧭

## 概述

本文档基于 `DataBaseStatement.txt` 中的 DDL 语句，目标数据库为 **shanghai_metro**。内容包括：模式概览、表结构、索引与性能建议、常用查询、部署与运维命令、以及改进建议。

> 注意：原始 DDL 中存在少量语法错误（如 `CREATE USER` 行），文中已给出修正后的示例语句以供直接使用。

---

## 一、数据库信息

- 数据库名：`shanghai_metro`
- 推荐字符集：`utf8mb4`，排序规则：`utf8mb4_unicode_ci`
- 推荐管理员用户（示例）：

```sql
CREATE DATABASE shanghai_metro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'metro_admin'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON shanghai_metro.* TO 'metro_admin'@'%';
FLUSH PRIVILEGES;
```

---

## 二、表结构概览

按依赖顺序列出主要表及字段说明：

### 1) `Station`（站点） 🔸

- 字段：`stationID INT PRIMARY KEY`, `name VARCHAR(100) NOT NULL`, `lon DECIMAL(11,8)`, `lat DECIMAL(11,8)`
- 说明：站点基础信息；建议为 `name` 建索引以便按名称查询。

### 2) `Neighbour`（邻站关系） 🔗

- 字段：`stationID INT`, `neighbourID INT`；主键 (`stationID`, `neighbourID`)
- 外键：均引用 `Station(stationID)`；表示站点拓扑结构（建议明确 `ON DELETE` 策略）。

### 3) `DateInfo`（日期信息） 📅

- 字段：`recordDate DATE PRIMARY KEY`, `isWorkDay TINYINT(1) NOT NULL`
- 说明：标识每天是否为工作日，用于按日聚合。

### 4) `TimeSegment`（时间段） ⏱️

- 字段：`Slot INT PRIMARY KEY`, `recordDate DATE NOT NULL`, `StartTime TIME NOT NULL`, `EndTime TIME NOT NULL`
- 外键：`recordDate` -> `DateInfo(recordDate)`；用于按 Slot 聚合流量。

### 5) `Weather`（逐小时天气） ☁️

- 字段：`recordDate DATE`, `recordTime TIME`, `temperature_2m`, `apparent_temperature`, `rain`, `wind_speed_10m`
- 主键：(`recordDate`, `recordTime`)；外键：`recordDate` -> `DateInfo(recordDate)`

### 6) `Inflow` / `Outflow`（进/出站流量） 🚉

- 字段示例：`Slot`, `stationID`, `Tot_IF/Tot_OF`, `C_IF/C_OF`, `HB_IF/HB_OF`, `NHB_IF/NHB_OF`。
- 主键：(`Slot`, `stationID`)；外键：`Slot` -> `TimeSegment(Slot)`，`stationID` -> `Station(stationID)`。
- 说明：`C_`/`HB_`/`NHB_` 表示分票类或人群分组（应在项目文档中补充定义）。

### 7) `ODFlow`（OD 流量） 🔁

- 字段：`Slot`, `O_Station`, `D_Station`, `Tot_F`, `C_F`, `HB_F`, `NHB_F`
- 主键：(`Slot`, `O_Station`, `D_Station`)；外键：`O_Station`/`D_Station` -> `Station(stationID)`。

---

## 三、索引与优化建议 ⚙️

- 已建议索引：`idx_station_name`（Station.name）、`idx_timesegment_date`（TimeSegment.recordDate）、`idx_inflow_station`/`idx_outflow_station`、`idx_odflow_o/d/od`。
- 建议：
  - 为 `TimeSegment(recordDate, StartTime)` 添加复合索引以加速按时间范围查询。
  - 在 `Inflow/Outflow` 上按需添加 `Slot` 单列索引以优化基于 Slot 的聚合查询。
  - 若数据量大，考虑按 `recordDate` 或 `Slot` 做分区（PARTITION）以便归档和删除历史数据。
  - 如需地理查询，考虑将经纬度改为 MySQL 空间类型并添加空间索引（`POINT` + `SPATIAL INDEX`）。

---

## 四、常用查询示例 🔍

- 某站某 Slot 总进站：

```sql
SELECT stationID, SUM(Tot_IF) AS tot_in
FROM Inflow
WHERE Slot = 20251225_01
GROUP BY stationID;
```

- Top 10 OD 对（某 Slot）：

```sql
SELECT O_Station, D_Station, SUM(Tot_F) AS flow
FROM ODFlow
WHERE Slot = 1234
GROUP BY O_Station, D_Station
ORDER BY flow DESC
LIMIT 10;
```

- 将天气与进站量按小时合并（示例）：

```sql
SELECT w.recordDate, w.recordTime, SUM(i.Tot_IF) AS tot_in
FROM Weather w
JOIN TimeSegment t ON t.recordDate = w.recordDate
JOIN Inflow i ON i.Slot = t.Slot
WHERE w.recordTime = '08:00'
GROUP BY w.recordDate, w.recordTime;
```

---

## 五、部署与运维命令 🛠️

- 检查 InnoDB 状态与当前运行进程：

```sql
SHOW ENGINE INNODB STATUS\G;
SHOW PROCESSLIST;
```

- 数据库备份示例：

```bash
mysqldump -u root -p shanghai_metro > shanghai_metro_backup_$(date +%F).sql
```

- 使用专用账号连接：

```bash
mysql -u metro_admin -p shanghai_metro
```

---

## 六、设计改进建议 💡

- 明确外键 `ON DELETE/ON UPDATE` 策略（建议使用 `RESTRICT` 或 `CASCADE` 视业务而定）。
- 为 `Neighbour` 明确单向或双向关系约定，避免重复插入（可在应用层保证或在表中统一约束）。
- 补充字段语义：在仓库文档中说明 `C_`、`HB_`、`NHB_` 等票类/人群字段具体含义。
- 若预计有大规模写入，建议针对批量导入采用分区与批量插入事务来减少锁竞争。

---

## 七、修正后的关键 DDL（节选）

```sql
CREATE DATABASE shanghai_metro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'metro_admin'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON shanghai_metro.* TO 'metro_admin'@'%';
FLUSH PRIVILEGES;

CREATE TABLE Station (
    stationID INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lon DECIMAL(11,8),
    lat DECIMAL(11,8)
) ENGINE=InnoDB;

CREATE TABLE Neighbour (
    stationID INT,
    neighbourID INT,
    PRIMARY KEY (stationID, neighbourID),
    FOREIGN KEY (stationID) REFERENCES Station(stationID),
    FOREIGN KEY (neighbourID) REFERENCES Station(stationID)
) ENGINE=InnoDB;
```

---

如需我将该 DDL 另存为 `shanghai_metro_schema.sql`，或基于此生成 ER 图（Mermaid / draw.io），或添加具体索引/分区脚本，请告诉我下一步操作。🔧
