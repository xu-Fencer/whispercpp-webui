from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.core.task_manager import task_manager

router = APIRouter()

class TaskRequest(BaseModel):
    input_file: str
    output_format: str
    whisper_params: Dict[str, Any] = {}

@router.post("/")
async def create_task(task: TaskRequest):
    try:
        job_id = task_manager.create_task(task.input_file, task.output_format, task.whisper_params)
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
