import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.path_guard import is_valid_file_path
from app.core.task_manager import TaskManager

router = APIRouter()

# 用于管理任务
task_manager = TaskManager()

@router.get("/{job_id}")
async def list_files(job_id: str):
    """
    获取指定任务 ID 下的所有生成文件列表
    """
    task = task_manager.get_task_status(job_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_dir = task["task_dir"]
    
    # 获取该目录下的所有文件
    try:
        files = [f for f in os.listdir(task_dir) if os.path.isfile(os.path.join(task_dir, f))]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Task files not found")
    
    return {"files": files}


@router.get("/{job_id}/{file_name}")
async def download_file(job_id: str, file_name: str):
    """
    下载指定任务 ID 下的文件
    """
    task = task_manager.get_task_status(job_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_dir = task["task_dir"]
    file_path = os.path.join(task_dir, file_name)
    
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # 验证文件路径安全
    if not is_valid_file_path(file_path, task_dir):
        raise HTTPException(status_code=403, detail="Forbidden file access")

    # 返回文件响应
    return FileResponse(file_path)


# 安全检查函数：确保文件路径在任务目录范围内
def is_valid_file_path(file_path: str, task_dir: str) -> bool:
    """
    验证文件路径是否在指定的任务目录内
    """
    # 确保文件路径在任务目录内，避免路径穿越攻击
    return os.path.commonpath([file_path, task_dir]) == task_dir
