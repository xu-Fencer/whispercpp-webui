import uuid
import os
from app.whisper.command_builder import build_whisper_command
from app.core.process_runner import run_whisper_process

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def create_task(self, input_file: str, output_format: str, whisper_params: dict):
        job_id = str(uuid.uuid4())
        task_dir = os.path.join("app/runs", job_id)
        os.makedirs(task_dir, exist_ok=True)
        
        command = build_whisper_command(input_file, output_format, whisper_params)
        process = run_whisper_process(command, job_id, task_dir)
        
        self.tasks[job_id] = {
            "status": "in-progress",
            "process": process,
            "task_dir": task_dir
        }
        return job_id

    def get_task_status(self, job_id: str):
        task = self.tasks.get(job_id)
        if not task:
            return None
        return task

    def cancel_task(self, job_id: str):
        task = self.tasks.get(job_id)
        if not task:
            return False
        task["process"].terminate()
        self.tasks.pop(job_id, None)
        return True
