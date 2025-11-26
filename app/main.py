from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from fastapi import WebSocket, WebSocketDisconnect
from app.websockets.manager import manager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development: Boleh dari semua domain. Production: Ganti jadi ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Moshi Moshi! Backend is Alive."}

# Endpoint WebSocket (ws://localhost:8000/ws/kitchen)
@app.websocket("/ws/kitchen")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)




