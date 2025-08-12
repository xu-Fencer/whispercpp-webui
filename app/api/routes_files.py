import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.task_manager import task_manager

router = APIRouter()

def is_valid_file_path(file_path: str, task_dir: str) -> bool:
    return os.path.commonpath([os.path.abspath(file_path), os.path.abspath(task_dir)]) == os.path.abspath(task_dir)

@router.get("/{job_id}")
async def list_files(job_id: str):
    task = task_manager.get_task_status(job_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_dir = task["task_dir"]
    if not os.path.isdir(task_dir):
        raise HTTPException(status_code=404, detail="Task dir not found")

    files = [f for f in os.listdir(task_dir) if os.path.isfile(os.path.join(task_dir, f))]
    return {"files": files}

@router.get("/{job_id}/{file_name}")
async def download_file(job_id: str, file_name: str):
    task = task_manager.get_task_status(job_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_dir = task["task_dir"]
    file_path = os.path.join(task_dir, file_name)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    if not is_valid_file_path(file_path, task_dir):
        raise HTTPException(status_code=403, detail="Forbidden file access")

    return FileResponse(file_path)
