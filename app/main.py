from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes_tasks import router as tasks_router
from app.api.routes_settings import router as settings_router
from app.api.routes_files import router as files_router
from app.api.routes_probe import router as probe_router, router_compat as probe_router_compat

# 可选：WebSocket 日志（若使用前端 LogConsole）
try:
    from app.api.routes_ws import router as ws_router
    HAS_WS = True
except Exception:
    HAS_WS = False

import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态（若有构建产物）
if os.path.isdir("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 路由注册
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
app.include_router(settings_router, prefix="/api/settings", tags=["settings"])
app.include_router(files_router, prefix="/api/files", tags=["files"])
app.include_router(probe_router, prefix="/api/probe", tags=["probe"])

# 兼容旧路径 /whisper
app.include_router(probe_router_compat, prefix="", tags=["probe-compat"])

# 可选 WS：/ws/logs/{job_id}
if HAS_WS:
    app.include_router(ws_router, prefix="/ws", tags=["ws"])
