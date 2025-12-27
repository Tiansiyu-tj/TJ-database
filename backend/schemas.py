from pydantic import BaseModel
from typing import List, Dict, Optional, Any


# ============ 通用响应模型 ============

class BaseResponse(BaseModel):
    """通用响应基类"""
    code: int = 0
    message: str = ""


# ============ 时刻表相关 ============

class ScheduleData(BaseModel):
    campus: str
    routeKey: str
    dayType: str
    direction: str
    times: List[str]


class ScheduleResponse(BaseResponse):
    data: ScheduleData


# ============ 拥挤度曲线相关 ============

class CongestionProfile(BaseModel):
    line: str
    hours: List[str]
    congestion: List[float]


class CongestionResponse(BaseResponse):
    data: List[CongestionProfile]


# ============ 路径元数据相关 ============

class RouteMeta(BaseModel):
    lineKey: str
    displayName: str
    color: str
    defaultMetroMinutes: int
    walkSteps: int
    shuttleKey: Optional[str]
    descriptionTemplate: Optional[str]


class RouteMetaResponse(BaseResponse):
    data: List[RouteMeta]


# ============ 终点站时间相关 ============

class LineTimes(BaseModel):
    line11: Optional[int] = None
    line14: Optional[int] = None


class DestinationTime(BaseModel):
    station: str
    lineTimes: Dict[str, int]


class DestinationTimesResponse(BaseResponse):
    data: List[DestinationTime]


# ============ 线路站点相关 ============

class Station(BaseModel):
    id: int
    name: str


class LineWithStations(BaseModel):
    lineId: str
    lineName: str
    stations: List[Station]


class LinesWithStationsResponse(BaseResponse):
    data: List[LineWithStations]
