from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, List

from ..database import get_db
from ..models import CommuteSchedule, CommuteRouteMeta, DestinationTravelTime

router = APIRouter()


@router.get("/schedules")
def get_schedules(
    campus: str = Query(..., description="校区，如 jiading"),
    routeKey: str = Query(..., description="路线标识，如 dz1/beian/bus822/teacher"),
    dayType: str = Query(..., description="工作日/周末: weekday/weekend"),
    direction: str = Query(..., description="方向: campusToStation/stationToCampus"),
    db: Session = Depends(get_db)
):
    """
    获取校区出行时刻表
    
    - **campus**: 校区名称（jiading）
    - **routeKey**: 路线标识（dz1/beian/bus822/teacher）
    - **dayType**: 日期类型（weekday/weekend）
    - **direction**: 方向（campusToStation/stationToCampus）
    """
    # 查询时刻表
    schedules = db.query(CommuteSchedule).filter(
        CommuteSchedule.campus == campus,
        CommuteSchedule.route_key == routeKey,
        CommuteSchedule.day_type == dayType,
        CommuteSchedule.direction == direction
    ).order_by(CommuteSchedule.departure_time).all()
    
    # 格式化时间为 HH:MM
    times = [s.departure_time.strftime("%H:%M") for s in schedules]
    
    return {
        "code": 0,
        "message": "",
        "data": {
            "campus": campus,
            "routeKey": routeKey,
            "dayType": dayType,
            "direction": direction,
            "times": times
        }
    }


@router.get("/routeMeta")
def get_route_meta(db: Session = Depends(get_db)):
    """
    获取路径元数据（步行距离/地铁时间/接驳方式）
    """
    routes = db.query(CommuteRouteMeta).all()
    
    data = []
    for r in routes:
        data.append({
            "lineKey": r.line_key,
            "displayName": r.display_name,
            "color": r.color,
            "defaultMetroMinutes": r.default_metro_minutes,
            "walkSteps": r.walk_steps,
            "shuttleKey": r.shuttle_key,
            "descriptionTemplate": r.description_template
        })
    
    return {
        "code": 0,
        "message": "",
        "data": data
    }


@router.get("/destinationTimes")
def get_destination_times(db: Session = Depends(get_db)):
    """
    获取不同终点站对应的地铁时间
    """
    records = db.query(DestinationTravelTime).all()
    
    # 按站点聚合
    station_times: Dict[str, Dict[str, int]] = {}
    for r in records:
        if r.station_name not in station_times:
            station_times[r.station_name] = {}
        station_times[r.station_name][r.line_key] = r.travel_minutes
    
    # 转换为响应格式
    data = [
        {"station": station, "lineTimes": times}
        for station, times in station_times.items()
    ]
    
    return {
        "code": 0,
        "message": "",
        "data": data
    }


# ============ 时刻表 CRUD 操作 ============

from pydantic import BaseModel
from datetime import time as dt_time

class ScheduleCreate(BaseModel):
    campus: str = "jiading"
    routeKey: str
    dayType: str
    direction: str
    departureTime: str  # 格式 "HH:MM"

class ScheduleUpdate(BaseModel):
    departureTime: str  # 格式 "HH:MM"


@router.post("/schedules")
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    """
    添加一条班次时刻
    """
    # 解析时间
    hour, minute = map(int, schedule.departureTime.split(":"))
    departure = dt_time(hour, minute)
    
    # 创建记录
    new_schedule = CommuteSchedule(
        campus=schedule.campus,
        route_key=schedule.routeKey,
        day_type=schedule.dayType,
        direction=schedule.direction,
        departure_time=departure
    )
    
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    
    return {
        "code": 0,
        "message": "添加成功",
        "data": {
            "id": new_schedule.id,
            "departureTime": schedule.departureTime
        }
    }


@router.put("/schedules/{schedule_id}")
def update_schedule(schedule_id: int, schedule: ScheduleUpdate, db: Session = Depends(get_db)):
    """
    修改一条班次时刻
    """
    record = db.query(CommuteSchedule).filter(CommuteSchedule.id == schedule_id).first()
    if not record:
        return {"code": 404, "message": "班次不存在", "data": None}
    
    # 更新时间
    hour, minute = map(int, schedule.departureTime.split(":"))
    record.departure_time = dt_time(hour, minute)
    
    db.commit()
    
    return {
        "code": 0,
        "message": "修改成功",
        "data": {"id": schedule_id, "departureTime": schedule.departureTime}
    }


@router.delete("/schedules/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """
    删除一条班次时刻
    """
    record = db.query(CommuteSchedule).filter(CommuteSchedule.id == schedule_id).first()
    if not record:
        return {"code": 404, "message": "班次不存在", "data": None}
    
    db.delete(record)
    db.commit()
    
    return {
        "code": 0,
        "message": "删除成功",
        "data": {"id": schedule_id}
    }


@router.get("/schedules/list")
def list_schedules(
    routeKey: str = Query(None, description="路线标识"),
    dayType: str = Query(None, description="日期类型"),
    db: Session = Depends(get_db)
):
    """
    获取时刻表列表（带ID，用于管理）
    """
    query = db.query(CommuteSchedule)
    
    if routeKey:
        query = query.filter(CommuteSchedule.route_key == routeKey)
    if dayType:
        query = query.filter(CommuteSchedule.day_type == dayType)
    
    schedules = query.order_by(CommuteSchedule.route_key, CommuteSchedule.departure_time).all()
    
    data = []
    for s in schedules:
        data.append({
            "id": s.id,
            "campus": s.campus,
            "routeKey": s.route_key,
            "dayType": s.day_type,
            "direction": s.direction,
            "departureTime": s.departure_time.strftime("%H:%M")
        })
    
    return {
        "code": 0,
        "message": "",
        "data": data
    }

