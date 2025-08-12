from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.whisper.cli_args import WHISPER_CLI_ARGS, json_path
import json

router = APIRouter()

@router.get("/whisper-args")
async def get_whisper_args():
    """
    提供所有 whisper.cpp 的命令行参数定义，供前端动态生成 UI。
    """
    return WHISPER_CLI_ARGS

@router.put("/whisper-args")
async def update_whisper_args(new_args: dict):
    """
    更新 whisper-args.json 文件。
    """
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(new_args, f, indent=4, ensure_ascii=False)
        return JSONResponse(content={"message": "Whisper args updated successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))