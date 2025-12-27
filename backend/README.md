# 嘉定出行后端 API

基于 FastAPI 的嘉定智能出行决策后端服务。

## 项目结构

```
backend/
├── main.py                 # FastAPI 入口
├── config.py              # 数据库配置（需修改）
├── database.py            # 数据库连接
├── models.py              # SQLAlchemy ORM 模型
├── schemas.py             # Pydantic 响应模型
├── requirements.txt       # Python 依赖
├── README.md              # 本文件
├── sql/
│   ├── create_tables.sql  # 建表语句
│   └── init_data.sql      # 初始数据
└── routers/
    ├── __init__.py
    ├── commute.py         # 出行相关 API
    └── metro.py           # 地铁相关 API
```

## 快速开始

### 1. 配置数据库

编辑 `config.py`，修改 MySQL 连接信息：

```python
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",           # 你的用户名
    "password": "123456",     # 你的密码
    "database": "jiading_commute"
}
```

### 2. 初始化数据库

在 MySQL 中执行：

```sql
source f:/大三上/数据库课设/代码/backend/sql/create_tables.sql;
source f:/大三上/数据库课设/代码/backend/sql/init_data.sql;
```

或使用命令行：

```bash
mysql -u root -p < sql/create_tables.sql
mysql -u root -p jiading_commute < sql/init_data.sql
```

### 3. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 4. 启动服务

```bash
python -m uvicorn main:app --reload --port 8000
```

或直接运行：

```bash
python main.py
```

### 5. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/commute/schedules` | 校区出行时刻表 |
| GET | `/api/commute/routeMeta` | 路径元数据 |
| GET | `/api/commute/destinationTimes` | 终点站地铁时间 |
| GET | `/api/metro/congestion/profiles` | 地铁拥挤度曲线 |
| GET | `/api/metro/lines-with-stations` | 线路与站点信息 |

## 示例请求

### 查询时刻表

```
GET /api/commute/schedules?campus=jiading&routeKey=dz1&dayType=weekday&direction=campusToStation
```

### 查询拥挤度

```
GET /api/metro/congestion/profiles?lines=11,14
```
