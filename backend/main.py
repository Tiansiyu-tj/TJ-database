from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import commute, metro, favorite, feedback, auth
from .routers import metro_metro

# 创建 FastAPI 应用
app = FastAPI(
    title="嘉定出行后端 API",
    description="为嘉定智能出行决策页面提供数据接口",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI 文档地址
    redoc_url="/redoc"     # ReDoc 文档地址
)

# 配置 CORS 跨域（允许前端调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # 生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(commute.router, prefix="/api/commute", tags=["出行"])
app.include_router(metro.router, prefix="/api/metro", tags=["地铁"])
app.include_router(metro_metro.router, prefix="/api/metro", tags=["上海地铁（shanghai_metro）"])
app.include_router(favorite.router, prefix="/api/favorites", tags=["收藏"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["反馈"])
app.include_router(auth.router, prefix="/api/auth", tags=["用户认证"])


@app.get("/", tags=["根"])
def root():
    """API 服务状态检查"""
    return {
        "message": "嘉定出行 API 服务正在运行",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["根"])
def health_check():
    """健康检查接口"""
    return {"status": "healthy"}


# 开发环境直接运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
