from fastapi import APIRouter
import subprocess

router = APIRouter()

@router.get("/ffmpeg")
async def probe_ffmpeg():
    try:
        output = subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT)
        return {"ffmpeg_version": output.decode("utf-8")}
    except subprocess.CalledProcessError:
        return {"error": "ffmpeg not found"}

@router.get("/whisper")
async def probe_whisper():
    try:
        output = subprocess.check_output(["whisper-cli", "-h"], stderr=subprocess.STDOUT)
        return {"whisper_available": True}
    except subprocess.CalledProcessError:
        return {"error": "whisper-cli not found"}
