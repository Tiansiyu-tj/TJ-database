from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL, DATABASE_URL_METRO

# 主库（jiading_commute）引擎
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False  # 设为 True 可打印 SQL 语句用于调试
)

# 次库（shanghai_metro）引擎
engine_metro = create_engine(
    DATABASE_URL_METRO,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocalMetro = sessionmaker(autocommit=False, autoflush=False, bind=engine_metro)

# 模型基类
Base = declarative_base()
BaseMetro = declarative_base()


def get_db():
    """
    获取主库数据库会话的依赖函数
    使用方式: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_metro():
    """
    获取次库（shanghai_metro）数据库会话的依赖函数
    使用方式: db: Session = Depends(get_db_metro)
    """
    db = SessionLocalMetro()
    try:
        yield db
    finally:
        db.close()
