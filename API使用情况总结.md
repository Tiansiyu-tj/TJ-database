# 嘉定出行 API 使用情况总结

## 已接入后端 API 的数据

| 数据类型 | API 接口 | 前端位置 | 说明 |
|---------|---------|---------|------|
| 时刻表 | `GET /api/commute/schedules` | `Commute.vue` → `busSchedules` | DZ1/北安跨线/822路/教职班车 |
| 拥挤度曲线 | `GET /api/metro/congestion/profiles` | `Commute.vue` → `congestionProfiles` | 11/14号线每小时拥挤度 |
| 路径元数据 | `GET /api/commute/routeMeta` | `Commute.vue` → `lineMeta` | 路径名称/颜色/步行距离等 |
| 终点站时间 | `GET /api/commute/destinationTimes` | `Commute.vue` → `destinationTravelMinutes` | 各站点到达时间 |
| 线路站点 | `GET /api/metro/lines-with-stations` | `Commute.vue` → `lineOptions` / `lineToStations` | 线路和站点下拉选项 |

---

## 使用方式

### API 服务文件
`src/api/commuteApi.js` - 封装了5个 API 调用函数

### 数据加载时机
- **页面加载时**：`onMounted()` 调用 `loadAllData()` 从后端获取全部数据
- **切换日期类型时**：`watch(dayType)` 重新加载时刻表

---

## 仍使用本地数据的内容

| 内容 | 来源 |
|------|------|
| 时刻表键名列表 `timetableKeys` | 前端硬编码 `['bus822', 'dz1', 'beian', 'teacher']` |
| 倒计时卡片配置 | 前端硬编码 tag 类型和方向标签 |

---

## 文件变更清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `src/api/commuteApi.js` | 新增 | API 服务模块 |
| `src/views/Commute.vue` | 修改 | 改用 API 获取数据 |
| `src/data/commuteData.js` | 保留 | 作为备用/fallback 数据 |

---

## 后端文件清单

| 文件 | 说明 |
|------|------|
| `backend/main.py` | FastAPI 入口 |
| `backend/config.py` | 数据库配置 |
| `backend/database.py` | 数据库连接 |
| `backend/models.py` | ORM 模型 |
| `backend/schemas.py` | 响应模型 |
| `backend/routers/commute.py` | 出行 API (3个) |
| `backend/routers/metro.py` | 地铁 API (2个) |
| `backend/sql/create_tables.sql` | 建表语句 |
| `backend/sql/init_data.sql` | 初始数据 |
