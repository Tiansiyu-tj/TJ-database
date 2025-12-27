import os

# 数据库配置
# 优先使用环境变量 DATABASE_URL / DATABASE_URL_METRO，回退到仓库内的默认配置

DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "database": os.getenv("DB_NAME", "jiading_commute")
}

# SQLAlchemy 数据库连接 URL（主库）
DATABASE_URL = os.getenv("DATABASE_URL") or f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?charset=utf8mb4"

# 第二个数据库（上海地铁分析数据库），可通过环境变量 DATABASE_URL_METRO 覆盖
DATABASE_URL_METRO = os.getenv("DATABASE_URL_METRO") or f"mysql+pymysql://{os.getenv('DB_METRO_USER','root')}:{os.getenv('DB_METRO_PASSWORD','123456')}@{os.getenv('DB_METRO_HOST','localhost')}:{os.getenv('DB_METRO_PORT',3306)}/shanghai_metro?charset=utf8mb4"
