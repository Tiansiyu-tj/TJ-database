from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models import CongestionFeedback

router = APIRouter()


class FeedbackCreate(BaseModel):
    lineId: str
    hour: int
    reportedLevel: str  # 'empty' | 'normal' | 'crowded' | 'packed'
    userId: str = "anonymous"


@router.post("/congestion")
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    提交拥挤度反馈
    """
    new_feedback = CongestionFeedback(
        line_id=feedback.lineId,
        hour=feedback.hour,
        reported_level=feedback.reportedLevel,
        user_id=feedback.userId
    )
    
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    
    return {
        "code": 0,
        "message": "反馈已提交，感谢您的贡献！",
        "data": {
            "id": new_feedback.id,
            "lineId": feedback.lineId,
            "hour": feedback.hour,
            "reportedLevel": feedback.reportedLevel
        }
    }


@router.get("/congestion/stats")
def get_feedback_stats(
    lineId: str = Query(..., description="线路号"),
    db: Session = Depends(get_db)
):
    """
    获取某条线路的拥挤度反馈统计
    """
    # 按小时和等级统计
    stats = db.query(
        CongestionFeedback.hour,
        CongestionFeedback.reported_level,
        func.count(CongestionFeedback.id).label('count')
    ).filter(
        CongestionFeedback.line_id == lineId
    ).group_by(
        CongestionFeedback.hour,
        CongestionFeedback.reported_level
    ).all()
    
    # 整理为按小时分组的数据
    hourly_stats = {}
    for hour, level, count in stats:
        if hour not in hourly_stats:
            hourly_stats[hour] = {'empty': 0, 'normal': 0, 'crowded': 0, 'packed': 0, 'total': 0}
        hourly_stats[hour][level] = count
        hourly_stats[hour]['total'] += count
    
    # 计算每小时的众数（最多人反馈的等级）
    result = []
    for hour in range(24):
        if hour in hourly_stats:
            data = hourly_stats[hour]
            # 找出最多的等级
            levels = ['empty', 'normal', 'crowded', 'packed']
            most_reported = max(levels, key=lambda x: data[x])
            result.append({
                'hour': hour,
                'mostReported': most_reported,
                'total': data['total'],
                'breakdown': {k: data[k] for k in levels}
            })
        else:
            result.append({
                'hour': hour,
                'mostReported': None,
                'total': 0,
                'breakdown': {'empty': 0, 'normal': 0, 'crowded': 0, 'packed': 0}
            })
    
    return {
        "code": 0,
        "message": "",
        "data": {
            "lineId": lineId,
            "hourlyStats": result
        }
    }


@router.get("/congestion/recent")
def get_recent_feedbacks(
    lineId: str = Query(None, description="线路号（可选）"),
    limit: int = Query(20, description="返回数量"),
    db: Session = Depends(get_db)
):
    """
    获取最近的反馈记录
    """
    query = db.query(CongestionFeedback)
    
    if lineId:
        query = query.filter(CongestionFeedback.line_id == lineId)
    
    feedbacks = query.order_by(CongestionFeedback.id.desc()).limit(limit).all()
    
    data = []
    for f in feedbacks:
        data.append({
            "id": f.id,
            "lineId": f.line_id,
            "hour": f.hour,
            "reportedLevel": f.reported_level,
            "createdAt": f.created_at
        })
    
    return {
        "code": 0,
        "message": "",
        "data": data
    }
