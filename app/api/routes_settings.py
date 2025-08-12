from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import config
from app.core import openvino_env

router = APIRouter()

class Settings(BaseModel):
    whisper_path: str
    model_path: str
    openvino_script_path: str
    openvino_enabled: bool
    openvino_shell: str

@router.get("/", response_model=Settings)
async def get_settings():
    s = config.settings
    return Settings(
        whisper_path=s.get("whisper_path", ""),
        model_path=s.get("model_path", ""),
        openvino_script_path=s.get("openvino_script_path", ""),
        openvino_enabled=bool(s.get("openvino_enabled", False)),
        openvino_shell=s.get("openvino_shell", "auto"),
    )

@router.post("/")
async def save_settings(settings: Settings):
    config.set("whisper_path", settings.whisper_path)
    config.set("model_path", settings.model_path)
    config.set("openvino_script_path", settings.openvino_script_path)
    config.set("openvino_enabled", settings.openvino_enabled)
    config.set("openvino_shell", settings.openvino_shell)
    return {"message": "Settings updated"}

@router.post("/openvino/test")
async def test_openvino_script():
    success, output = openvino_env.run_openvino_script()
    if success:
        return {"message": "OpenVINO script executed successfully", "output": output}
    raise HTTPException(status_code=500, detail={"message": "Failed to execute OpenVINO script", "output": output})
