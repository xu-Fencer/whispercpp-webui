import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.task_manager import task_manager

router = APIRouter()

@router.websocket("/logs/{job_id}")
async def logs_ws(websocket: WebSocket, job_id: str):
    await websocket.accept()
    await task_manager.add_listener(job_id, websocket)
    try:
        # 检查任务是否存在
        if not task_manager.get_task_status(job_id):
            await websocket.send_text(f"Error: Task {job_id} not found.")
            await websocket.close()
            return

        while True:
            # 保持连接打开，等待来自 TaskManager 的消息
            # 也可以在这里接收来自客户端的消息，例如心跳
            await websocket.receive_text() # 等待客户端消息以保持连接
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for job_id: {job_id}")
        task_manager.remove_listener(job_id, websocket)

    except Exception as e:
        print(f"An error occurred in WebSocket for job_id {job_id}: {e}")
        task_manager.remove_listener(job_id, websocket)
        try:
            await websocket.close()
        except Exception:
            pass