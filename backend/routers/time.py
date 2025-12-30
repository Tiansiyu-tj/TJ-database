from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

router = APIRouter()

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic 模型
class TimeSegment(BaseModel):
    Slot: int
    recordDate: str
    StartTime: str
    EndTime: str

class TimeSegmentCreate(BaseModel):
    recordDate: str
    StartTime: str
    EndTime: str

class DateInfo(BaseModel):
    recordDate: str
    weekday: int
    isHoliday: bool

class WeatherRecord(BaseModel):
    recordDate: str
    recordTime: str
    temperature_2m: float
    rain: float
    wind_speed_10m: float

# 模拟数据存储（实际项目中应使用数据库）
time_segments = []
date_infos = []
weather_records = []

# 示例数据已移除 — 使用真实数据库或通过其它接口插入数据
# time_segments, date_infos, weather_records 保持为空列表，由数据库或调用方填充

@router.get("/segments", tags=["时间"], response_model=List[TimeSegment])
async def get_time_segments(
    recordDate: Optional[str] = None,
    limit: Optional[int] = 1000
):
    """
    获取时间段数据
    """
    logger.info(f"Fetching time segments, recordDate: {recordDate}, limit: {limit}")
    
    filtered_segments = time_segments
    
    if recordDate:
        filtered_segments = [seg for seg in filtered_segments if seg["recordDate"] == recordDate]
    
    if limit:
        filtered_segments = filtered_segments[:limit]
    
    return filtered_segments

@router.get("/segments/{slot}", tags=["时间"], response_model=TimeSegment)
async def get_time_segment_by_slot(slot: int):
    """
    根据Slot获取时间段数据
    """
    logger.info(f"Fetching time segment for slot: {slot}")
    
    for segment in time_segments:
        if segment["Slot"] == slot:
            return segment
    
    raise HTTPException(status_code=404, detail="Time segment not found")

@router.post("/segments", tags=["时间"], response_model=TimeSegment)
async def create_time_segment(segment: TimeSegmentCreate):
    """
    创建时间段数据
    """
    logger.info(f"Creating time segment: {segment}")
    
    # 生成新的Slot ID
    new_slot = len(time_segments) + 1
    new_segment = {
        "Slot": new_slot,
        "recordDate": segment.recordDate,
        "StartTime": segment.StartTime,
        "EndTime": segment.EndTime
    }
    
    time_segments.append(new_segment)
    return new_segment

@router.put("/segments/{slot}", tags=["时间"], response_model=TimeSegment)
async def update_time_segment(slot: int, segment: TimeSegmentCreate):
    """
    更新时间段数据
    """
    logger.info(f"Updating time segment {slot}: {segment}")
    
    for i, seg in enumerate(time_segments):
        if seg["Slot"] == slot:
            updated_segment = {
                "Slot": slot,
                "recordDate": segment.recordDate,
                "StartTime": segment.StartTime,
                "EndTime": segment.EndTime
            }
            time_segments[i] = updated_segment
            return updated_segment
    
    raise HTTPException(status_code=404, detail="Time segment not found")

@router.delete("/segments/{slot}", tags=["时间"])
async def delete_time_segment(slot: int):
    """
    删除时间段数据
    """
    logger.info(f"Deleting time segment: {slot}")
    
    for i, segment in enumerate(time_segments):
        if segment["Slot"] == slot:
            del time_segments[i]
            return {"message": "Time segment deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Time segment not found")

@router.get("/dateinfo", tags=["时间"])
async def get_date_info(
    recordDate: Optional[str] = None,
    limit: Optional[int] = 100
):
    """
    获取日期信息，返回统一格式：{code, message, data}
    """
    logger.info(f"Fetching date info, recordDate: {recordDate}, limit: {limit}")
    
    filtered_dates = date_infos
    
    if recordDate:
        filtered_dates = [date for date in filtered_dates if date["recordDate"] == recordDate]
    
    if limit:
        filtered_dates = filtered_dates[:limit]
    
    return {"code": 0, "message": "", "data": filtered_dates}

@router.get("/weather", tags=["时间"], response_model=List[WeatherRecord])
async def get_weather(
    recordDate: Optional[str] = None,
    recordTime: Optional[str] = None,
    limit: Optional[int] = 100
):
    """
    获取天气数据
    """
    logger.info(f"Fetching weather, recordDate: {recordDate}, recordTime: {recordTime}, limit: {limit}")
    
    filtered_weather = weather_records
    
    if recordDate:
        filtered_weather = [w for w in filtered_weather if w["recordDate"] == recordDate]
    
    if recordTime:
        filtered_weather = [w for w in filtered_weather if w["recordTime"] == recordTime]
    
    if limit:
        filtered_weather = filtered_weather[:limit]
    
    return filtered_weather

@router.post("/weather", tags=["时间"], response_model=WeatherRecord)
async def create_weather_record(weather: WeatherRecord):
    """
    创建天气记录
    """
    logger.info(f"Creating weather record: {weather}")
    
    weather_records.append(weather.dict())
    return weather