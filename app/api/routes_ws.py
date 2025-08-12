import asyncio
import os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from app.core.task_manager import task_manager

router = APIRouter()

@router.websocket("/logs/{job_id}")
async def logs_ws(websocket: WebSocket, job_id: str):
    await websocket.accept()
    try:
        status = task_manager.get_task_status(job_id)
        if not status:
            await websocket.send_text("Task not found")
            await websocket.close()
            return

        task_dir = status["task_dir"]
        log_path = os.path.join(task_dir, "log.txt")
        # 确保日志文件存在
        os.makedirs(task_dir, exist_ok=True)
        open(log_path, "a", encoding="utf-8").close()

        # 简易 tail -f
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line:
                    await websocket.send_text(line.rstrip("\n"))
                else:
                    await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_text(f"WS error: {e}")
        except Exception:
            pass
        try:
            await websocket.close()
        except Exception:
            pass
