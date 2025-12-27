from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models import UserFavorite

router = APIRouter()


class FavoriteCreate(BaseModel):
    stationName: str
    lineKey: Optional[str] = None
    userId: str = "default"


@router.get("")
def get_favorites(
    userId: str = Query("default", description="用户ID"),
    db: Session = Depends(get_db)
):
    """
    获取用户收藏列表
    """
    favorites = db.query(UserFavorite).filter(
        UserFavorite.user_id == userId
    ).order_by(UserFavorite.id.desc()).all()
    
    data = []
    for f in favorites:
        data.append({
            "id": f.id,
            "stationName": f.station_name,
            "lineKey": f.line_key,
            "createdAt": f.created_at
        })
    
    return {
        "code": 0,
        "message": "",
        "data": data
    }


@router.post("")
def add_favorite(fav: FavoriteCreate, db: Session = Depends(get_db)):
    """
    添加收藏
    """
    # 检查是否已收藏
    existing = db.query(UserFavorite).filter(
        UserFavorite.user_id == fav.userId,
        UserFavorite.station_name == fav.stationName
    ).first()
    
    if existing:
        return {
            "code": 1,
            "message": "已收藏该站点",
            "data": {"id": existing.id}
        }
    
    # 创建收藏
    new_fav = UserFavorite(
        user_id=fav.userId,
        station_name=fav.stationName,
        line_key=fav.lineKey
    )
    
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    
    return {
        "code": 0,
        "message": "收藏成功",
        "data": {
            "id": new_fav.id,
            "stationName": fav.stationName
        }
    }


@router.delete("/{favorite_id}")
def remove_favorite(favorite_id: int, db: Session = Depends(get_db)):
    """
    取消收藏
    """
    record = db.query(UserFavorite).filter(UserFavorite.id == favorite_id).first()
    if not record:
        return {"code": 404, "message": "收藏不存在", "data": None}
    
    db.delete(record)
    db.commit()
    
    return {
        "code": 0,
        "message": "已取消收藏",
        "data": {"id": favorite_id}
    }


@router.delete("/station/{station_name}")
def remove_favorite_by_station(
    station_name: str,
    userId: str = Query("default"),
    db: Session = Depends(get_db)
):
    """
    按站点名取消收藏
    """
    record = db.query(UserFavorite).filter(
        UserFavorite.user_id == userId,
        UserFavorite.station_name == station_name
    ).first()
    
    if not record:
        return {"code": 404, "message": "未收藏该站点", "data": None}
    
    db.delete(record)
    db.commit()
    
    return {
        "code": 0,
        "message": "已取消收藏",
        "data": {"stationName": station_name}
    }
