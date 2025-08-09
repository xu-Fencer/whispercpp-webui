from fastapi import APIRouter
import json
from pydantic import BaseModel
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
    with open("app/settings.json", "r") as f:
        settings = json.load(f)
    return settings

@router.post("/")
async def save_settings(settings: Settings):
    # 更新配置文件
    with open("app/settings.json", "w") as f:
        json.dump(settings.dict(), f, indent=4)
    return {"message": "Settings updated"}

@router.post("/openvino/test")
async def test_openvino_script():
    # 执行 OpenVINO 脚本，并测试环境变量
    success, output = openvino_env.run_openvino_script()
    if success:
        return {"message": "OpenVINO script executed successfully", "output": output}
    return {"message": "Failed to execute OpenVINO script", "output": output}
