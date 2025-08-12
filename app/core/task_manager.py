import uuid
import os
from typing import Dict, Any, Optional
from app.whisper.command_builder import build_whisper_command
from app.core.process_runner import run_whisper_process

RUNS_DIR = "app/runs"
os.makedirs(RUNS_DIR, exist_ok=True)


class TaskManager:
    def __init__(self):
        # job_id -> { status, process, task_dir }
        self.tasks: Dict[str, Dict[str, Any]] = {}

    def create_task(self, input_file: str, output_format: str, whisper_params: dict) -> str:
        job_id = str(uuid.uuid4())
        task_dir = os.path.join(RUNS_DIR, job_id)
        os.makedirs(task_dir, exist_ok=True)

        command = build_whisper_command(input_file, output_format, whisper_params or {})
        process = run_whisper_process(command, job_id, task_dir)

        self.tasks[job_id] = {
            "status": "in-progress",
            "pid": process.pid,
            "process": process,
            "task_dir": task_dir,
        }
        return job_id

    def get_task_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        task = self.tasks.get(job_id)
        if not task:
            return None

        proc = task.get("process")
        if proc and proc.poll() is not None:
            task["status"] = "finished" if proc.returncode == 0 else "failed"
            task["returncode"] = proc.returncode
        return {
            "job_id": job_id,
            "status": task.get("status"),
            "pid": task.get("pid"),
            "returncode": task.get("returncode", None),
            "task_dir": task.get("task_dir"),
        }

    def cancel_task(self, job_id: str) -> bool:
        task = self.tasks.get(job_id)
        if not task:
            return False
        proc = task.get("process")
        if proc and proc.poll() is None:
            try:
                proc.terminate()
            except Exception:
                pass
        self.tasks.pop(job_id, None)
        return True


# 单例：供所有路由共享
task_manager = TaskManager()
