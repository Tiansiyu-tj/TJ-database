from sqlalchemy import Column, Integer, String, Time, DECIMAL, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base


class CommuteSchedule(Base):
    """校区出行时刻表（短驳/公交/教职班车）"""
    __tablename__ = "commute_schedule"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    campus = Column(String(50), nullable=False, comment="校区，如 jiading")
    route_key = Column(String(50), nullable=False, comment="路线标识，如 dz1/beian/bus822/teacher")
    day_type = Column(Enum('weekday', 'weekend'), nullable=False, comment="工作日/周末")
    direction = Column(String(50), nullable=False, comment="方向，如 campusToStation/stationToCampus")
    departure_time = Column(Time, nullable=False, comment="发车时间")


class MetroCongestionProfile(Base):
    """地铁拥挤度曲线"""
    __tablename__ = "metro_congestion_profile"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    line_id = Column(String(10), nullable=False, comment="线路号，如 11/14")
    hour = Column(Integer, nullable=False, comment="小时(0-23)")
    congestion = Column(DECIMAL(3, 2), nullable=False, comment="拥挤度(0-1)")


class CommuteRouteMeta(Base):
    """路径元数据"""
    __tablename__ = "commute_route_meta"
    
    line_key = Column(String(20), primary_key=True, comment="如 line11/line14")
    display_name = Column(String(100), nullable=False)
    color = Column(String(10), nullable=False, comment="颜色代码")
    default_metro_minutes = Column(Integer, nullable=False)
    walk_steps = Column(Integer, nullable=False)
    shuttle_key = Column(String(50), comment="接驳方式")
    description_template = Column(Text)


class DestinationTravelTime(Base):
    """终点站-线路时间对照"""
    __tablename__ = "destination_travel_time"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_name = Column(String(50), nullable=False, comment="终点站名")
    line_key = Column(String(20), nullable=False, comment="线路如 line11/line14")
    travel_minutes = Column(Integer, nullable=False)


class MetroLine(Base):
    """地铁线路"""
    __tablename__ = "metro_line"
    
    line_id = Column(String(10), primary_key=True)
    line_name = Column(String(50), nullable=False)
    
    # 关联站点
    stations = relationship("MetroStation", secondary="metro_line_station", back_populates="lines")


class MetroStation(Base):
    """地铁站点"""
    __tablename__ = "metro_station"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    
    # 关联线路
    lines = relationship("MetroLine", secondary="metro_line_station", back_populates="stations")


class MetroLineStation(Base):
    """线路-站点关联表"""
    __tablename__ = "metro_line_station"
    
    line_id = Column(String(10), ForeignKey("metro_line.line_id"), primary_key=True)
    station_id = Column(Integer, ForeignKey("metro_station.id"), primary_key=True)
    seq = Column(Integer, comment="站点顺序")


class UserFavorite(Base):
    """用户收藏"""
    __tablename__ = "user_favorite"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), default="default", comment="用户ID")
    station_name = Column(String(50), nullable=False, comment="收藏的站点名")
    line_key = Column(String(20), comment="线路标识")
    created_at = Column(String(50), comment="创建时间")


class CongestionFeedback(Base):
    """拥挤度反馈"""
    __tablename__ = "congestion_feedback"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    line_id = Column(String(10), nullable=False, comment="线路号")
    hour = Column(Integer, nullable=False, comment="小时(0-23)")
    reported_level = Column(Enum('empty', 'normal', 'crowded', 'packed'), nullable=False, comment="拥挤等级")
    user_id = Column(String(50), default="anonymous", comment="用户ID")
    created_at = Column(String(50), comment="创建时间")


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    email = Column(String(100), unique=True, nullable=False, comment="邮箱")
    nickname = Column(String(50), comment="昵称")
    avatar = Column(String(255), comment="头像URL")
    role = Column(Enum('user', 'admin'), default='user', comment="角色")
    created_at = Column(String(50), comment="创建时间")
    updated_at = Column(String(50), comment="更新时间")
