from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional

from ..database import get_db
from ..models import MetroCongestionProfile, MetroLine, MetroStation, MetroLineStation

router = APIRouter()


@router.get("/congestion/profiles")
def get_congestion_profiles(
    lines: str = Query(..., description="线路号，逗号分隔，如 11,14"),
    date: Optional[str] = Query(None, description="日期 YYYY-MM-DD（可选）"),
    db: Session = Depends(get_db)
):
    """
    获取地铁拥挤度曲线
    
    - **lines**: 线路号，逗号分隔（如 11,14）
    - **date**: 日期（可选，暂未使用）
    """
    line_list = [l.strip() for l in lines.split(",")]
    
    data = []
    for line_id in line_list:
        # 查询该线路的拥挤度数据
        profiles = db.query(MetroCongestionProfile).filter(
            MetroCongestionProfile.line_id == line_id
        ).order_by(MetroCongestionProfile.hour).all()
        
        if profiles:
            hours = [f"{p.hour:02d}:00" for p in profiles]
            congestion = [float(p.congestion) for p in profiles]
            
            data.append({
                "line": line_id,
                "hours": hours,
                "congestion": congestion
            })
    
    return {
        "code": 0,
        "message": "",
        "data": data
    }


@router.get("/lines-with-stations")
def get_lines_with_stations(db: Session = Depends(get_db)):
    """
    获取地铁线路及其站点信息
    """
    # 查询所有线路
    lines = db.query(MetroLine).all()
    
    data = []
    for line in lines:
        # 查询该线路的站点（按顺序）
        station_records = db.query(
            MetroStation.id,
            MetroStation.name,
            MetroLineStation.seq
        ).join(
            MetroLineStation,
            MetroStation.id == MetroLineStation.station_id
        ).filter(
            MetroLineStation.line_id == line.line_id
        ).order_by(MetroLineStation.seq).all()
        
        stations = [
            {"id": s.id, "name": s.name}
            for s in station_records
        ]
        
        data.append({
            "lineId": line.line_id,
            "lineName": line.line_name,
            "stations": stations
        })
    
    return {
        "code": 0,
        "message": "",
        "data": data
    }
