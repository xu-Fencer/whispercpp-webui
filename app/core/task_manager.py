import asyncio
import uuid
import os
import subprocess
from typing import Dict, Any, Optional, List
from fastapi import WebSocket

from app.whisper.command_builder import build_whisper_command
from app.core.process_runner import run_whisper_process

RUNS_DIR = "app/runs"
os.makedirs(RUNS_DIR, exist_ok=True)


class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.listeners: Dict[str, List[WebSocket]] = {}

    async def _log_broadcaster(self, job_id: str, process: subprocess.Popen):
        task_dir = self.tasks[job_id]["task_dir"]
        log_path = os.path.join(task_dir, "log.txt")
        log_buffer = self.tasks[job_id]["log_buffer"]

        with open(log_path, "w", encoding="utf-8") as log_file:
            while True:
                chunk = await asyncio.to_thread(process.stdout.read, 1)
                if not chunk:
                    break
                log_file.write(chunk)
                log_file.flush()
                log_buffer.append(chunk)

                # Broadcast to listeners
                if job_id in self.listeners:
                    for listener in self.listeners[job_id]:
                        await listener.send_text(chunk)

    def create_task(self, input_file: str, output_format: str, whisper_params: dict) -> str:
        job_id = str(uuid.uuid4())
        task_dir = os.path.join(RUNS_DIR, job_id)
        os.makedirs(task_dir, exist_ok=True)

        command = build_whisper_command(input_file, output_format, whisper_params or {})
        process = run_whisper_process(command, task_dir)

        self.tasks[job_id] = {
            "status": "in-progress",
            "pid": process.pid,
            "process": process,
            "task_dir": task_dir,
            "log_buffer": [],
        }

        asyncio.create_task(self._log_broadcaster(job_id, process))
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

    async def add_listener(self, job_id: str, websocket: WebSocket):
        if job_id not in self.listeners:
            self.listeners[job_id] = []
        self.listeners[job_id].append(websocket)

        # Send buffered logs
        task = self.tasks.get(job_id)
        if task and task.get("log_buffer"):
            for chunk in task["log_buffer"]:
                await websocket.send_text(chunk)

    def remove_listener(self, job_id: str, websocket: WebSocket):
        if job_id in self.listeners:
            self.listeners[job_id].remove(websocket)
            if not self.listeners[job_id]:
                del self.listeners[job_id]


# 单例：供所有路由共享
task_manager = TaskManager()