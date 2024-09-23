from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: bytes):
        for connection in self.active_connections:
            await connection.send_bytes(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_bytes()
            response = {
                "status": "ok",
                "client_id": client_id,
                "message": data
            }
            await websocket.send_bytes(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        response = {
            "status": "disconnected",
            "client_id": client_id
        }
        await manager.broadcast(response)
    except Exception as e:
        response = {
            "status": "error",
            "client_id": client_id,
            "message": str(e)
        }
        await websocket.send_json(response)
