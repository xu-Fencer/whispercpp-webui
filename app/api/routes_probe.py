from fastapi import APIRouter, HTTPException
import subprocess
import os
from app.config import config

# 主路由（挂载到 /api/probe）
router = APIRouter()
# 兼容路由（直接挂载到根 /whisper）
router_compat = APIRouter()


def _probe_whisper_impl() -> dict:
    whisper_exe = config.get("whisper_path")
    if not whisper_exe:
        raise HTTPException(status_code=400, detail="whisper executable path is not configured in settings.json (whisper_path)")
    if not os.path.exists(whisper_exe):
        raise HTTPException(status_code=400, detail=f"whisper executable not found: {whisper_exe}")

    try:
        output = subprocess.check_output([whisper_exe, "-h"], stderr=subprocess.STDOUT)
        text = output.decode("utf-8", errors="ignore")
        return {"whisper_available": True, "exe": whisper_exe, "help": text[:4000]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to execute whisper: {e}")


@router.get("/ffmpeg")
async def probe_ffmpeg():
    try:
        output = subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT)
        return {"ffmpeg_version": output.decode("utf-8", errors="ignore")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ffmpeg not found or failed: {e}")


@router.get("/whisper")
async def probe_whisper():
    return _probe_whisper_impl()


# 兼容旧路径：/whisper（便于前端回退）
@router_compat.get("/whisper")
async def probe_whisper_compat():
    return _probe_whisper_impl()
