# 数据库配置
# 请根据你的 MySQL 配置修改以下参数

DATABASE_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",           # 修改为你的 MySQL 用户名
    "password": "20050712ABC",     # 修改为你的 MySQL 密码
    "database": "jiading_commute"  # 数据库名
}

# SQLAlchemy 数据库连接 URL
DATABASE_URL = f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?charset=utf8mb4"
