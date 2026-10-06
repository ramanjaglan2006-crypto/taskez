import os
import json
import asyncio
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from taskez.core.agent import TaskEZAgent
from taskez.core.state import TraceEvent

app = FastAPI(title="TaskEZ Web UI Dashboard", version="1.0.0")

# Mount Web Directory
web_dir = os.path.join(os.path.dirname(__file__), "web")
app.mount("/static", StaticFiles(directory=web_dir), name="static")

class RunRequest(BaseModel):
    goal: str
    inject_failure: str = ""

active_websockets = set()

@app.get("/")
def get_dashboard():
    return FileResponse(os.path.join(web_dir, "index.html"))

@app.websocket("/ws/trace")
async def websocket_trace(websocket: WebSocket):
    await websocket.accept()
    active_websockets.add(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_websockets.remove(websocket)

async def broadcast_event(event: TraceEvent):
    event_json = event.json()
    disconnected = set()
    for ws in active_websockets:
        try:
            await ws.send_text(event_json)
        except Exception:
            disconnected.add(ws)
    for ws in disconnected:
        active_websockets.remove(ws)

@app.post("/api/run")
async def run_agent_task(req: RunRequest, background_tasks: BackgroundTasks):
    failure_tool = req.inject_failure if req.inject_failure and req.inject_failure != "none" else None
    agent = TaskEZAgent(failure_injection_tool=failure_tool)
    
    loop = asyncio.get_event_loop()

    def sync_listener(event: TraceEvent):
        asyncio.run_coroutine_threadsafe(broadcast_event(event), loop)

    agent.register_event_listener(sync_listener)

    def execute_in_background():
        agent.run(req.goal)

    background_tasks.add_task(execute_in_background)
    
    return {"status": "started", "goal": req.goal, "inject_failure": failure_tool}
