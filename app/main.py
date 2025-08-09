from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.routes_tasks import router as tasks_router
from app.api.routes_settings import router as settings_router
from app.api.routes_files import router as files_router
from app.api.routes_probe import router as probe_router

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以更严格地限制来源
    allow_credentials=True,
    allow_methods=["*"],  # 或者限制允许的 HTTP 方法
    allow_headers=["*"],
)

# 静态文件托管（前端构建好的文件）
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 路由注册
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(settings_router, prefix="/api/settings", tags=["settings"])
app.include_router(files_router, prefix="/api/files", tags=["files"])
app.include_router(probe_router, prefix="/api/probe", tags=["probe"])

# FastAPI 的其他相关设置可以在这里配置
