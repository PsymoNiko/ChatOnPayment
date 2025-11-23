"""
Chat Microservice - FastAPI Application with WebSocket Support

Provides real-time chat functionality via WebSocket connections.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

app = FastAPI(title="Chat Service", version="0.1.0")


class ConnectionManager:
    """Manages WebSocket connections for chat rooms."""
    
    def __init__(self):
        # room_name -> list of websocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room_name: str):
        """Connect a client to a chat room."""
        await websocket.accept()
        if room_name not in self.active_connections:
            self.active_connections[room_name] = []
        self.active_connections[room_name].append(websocket)
    
    def disconnect(self, websocket: WebSocket, room_name: str):
        """Disconnect a client from a chat room."""
        if room_name in self.active_connections:
            self.active_connections[room_name].remove(websocket)
            if not self.active_connections[room_name]:
                del self.active_connections[room_name]
    
    async def broadcast(self, message: dict, room_name: str):
        """Broadcast a message to all clients in a room."""
        if room_name in self.active_connections:
            disconnected = []
            for connection in self.active_connections[room_name]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)
            
            # Clean up disconnected clients
            for conn in disconnected:
                self.disconnect(conn, room_name)


manager = ConnectionManager()


@app.get("/healthz")
async def health_check():
    """Health check endpoint for liveness probe."""
    return {"status": "ok"}


@app.get("/readyz")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready"}


@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    """
    WebSocket endpoint for chat rooms.
    
    Clients connect to a specific room and can send/receive messages.
    Message format: {"message": "text", "phone_number": "user", "avatar": "url"}
    """
    await manager.connect(websocket, room_name)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Broadcast message to all clients in the room
            await manager.broadcast(
                {
                    "message": message_data.get("message", ""),
                    "phone_number": message_data.get("phone_number", ""),
                    "avatar": message_data.get("avatar", "")
                },
                room_name
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_name)
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")
        manager.disconnect(websocket, room_name)


@app.get("/rooms/{room_name}/info")
async def get_room_info(room_name: str):
    """Get information about a chat room."""
    connection_count = len(manager.active_connections.get(room_name, []))
    return {
        "room_name": room_name,
        "active_connections": connection_count
    }
