from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import os
from app.core.process_runner import run_whisper_process
from app.core.task_manager import TaskManager

router = APIRouter()

class TaskRequest(BaseModel):
    input_file: str
    output_format: str
    whisper_params: dict

# 用于管理任务
task_manager = TaskManager()

@router.post("/")
async def create_task(task: TaskRequest):
    job_id = task_manager.create_task(task.input_file, task.output_format, task.whisper_params)
    return {"job_id": job_id}

@router.get("/{job_id}")
async def get_task_status(job_id: str):
    status = task_manager.get_task_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return status

@router.delete("/{job_id}")
async def cancel_task(job_id: str):
    success = task_manager.cancel_task(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task cancelled"}
