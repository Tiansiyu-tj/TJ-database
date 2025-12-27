from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import hashlib

from database import get_db
from models import User

router = APIRouter()


# ============ 请求模型 ============

class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    nickname: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None


# ============ 工具函数 ============

def hash_password(password: str) -> str:
    """简单的密码哈希（课设演示用，生产环境建议用 bcrypt）"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    # 支持明文密码（兼容初始数据）和哈希密码
    return plain_password == hashed_password or hash_password(plain_password) == hashed_password


# ============ API 接口 ============

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    用户注册
    """
    # 检查用户名是否存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return {"code": 1, "message": "用户名已存在", "data": None}
    
    # 检查邮箱是否存在
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        return {"code": 2, "message": "邮箱已被注册", "data": None}
    
    # 创建用户
    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        email=user.email,
        nickname=user.nickname or user.username,
        role='user'
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "code": 0,
        "message": "注册成功",
        "data": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
    }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录
    """
    # 查找用户
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        return {"code": 1, "message": "用户不存在", "data": None}
    
    # 验证密码
    if not verify_password(user.password, db_user.password):
        return {"code": 2, "message": "密码错误", "data": None}
    
    # 返回用户信息（简化版，实际项目应返回 JWT token）
    return {
        "code": 0,
        "message": "登录成功",
        "data": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "nickname": db_user.nickname,
            "avatar": db_user.avatar,
            "role": db_user.role
        }
    }


@router.get("/me")
def get_current_user(
    userId: int,
    db: Session = Depends(get_db)
):
    """
    获取用户信息
    """
    user = db.query(User).filter(User.id == userId).first()
    if not user:
        return {"code": 404, "message": "用户不存在", "data": None}
    
    return {
        "code": 0,
        "message": "",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "role": user.role
        }
    }


@router.put("/me")
def update_user(
    userId: int,
    update: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    更新用户信息
    """
    user = db.query(User).filter(User.id == userId).first()
    if not user:
        return {"code": 404, "message": "用户不存在", "data": None}
    
    if update.nickname:
        user.nickname = update.nickname
    if update.email:
        user.email = update.email
    if update.avatar:
        user.avatar = update.avatar
    
    db.commit()
    
    return {
        "code": 0,
        "message": "更新成功",
        "data": {
            "id": user.id,
            "nickname": user.nickname,
            "email": user.email
        }
    }
