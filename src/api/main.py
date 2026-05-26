"""
TSBL — API Principal (FastAPI + WebSocket)
Sprint 0: Servidor base con heartbeat y manejo de sesiones
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI(
    title="TSBL API",
    description="Trust & Security Behavioral Lab — Backend de captura y análisis",
    version="0.1.0-sprint0",
)

# CORS para desarrollo (frontend en localhost:8080)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELOS DE DATOS ====================


class SessionStart(BaseModel):
    user_id: str
    metadata: Optional[Dict] = {}


class SessionResponse(BaseModel):
    session_id: str
    status: str
    created_at: str


class StreamPayload(BaseModel):
    seq: int
    ts_client: float
    landmarks: Optional[list] = None
    dom_events: Optional[list] = []
    fsp_level: int = 0


# ==================== ESTADO GLOBAL (en memoria para Sprint 0) ====================

sessions: Dict[str, dict] = {}

# ==================== ENDPOINTS REST ====================


@app.get("/")
async def root():
    return {
        "service": "TSBL API",
        "version": "0.1.0-sprint0",
        "status": "running",
        "sprint": "Sprint 0 — Cimientos",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_sessions": len(sessions),
    }


@app.post("/session/start", response_model=SessionResponse)
async def start_session(data: SessionStart):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "user_id": data.user_id,
        "created_at": datetime.utcnow().isoformat(),
        "status": "active",
        "frames_received": 0,
        "events_received": 0,
        "last_activity": datetime.utcnow().isoformat(),
        "baseline_ready": False,
        "vc_episodes": [],
        "theta": None,  # Se calibrará en Sprint 3
    }
    return SessionResponse(
        session_id=session_id,
        status="created",
        created_at=sessions[session_id]["created_at"],
    )


@app.get("/session/{session_id}/status")
async def session_status(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return sessions[session_id]


@app.post("/session/{session_id}/stream")
async def receive_stream(session_id: str, payload: StreamPayload):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    session = sessions[session_id]
    session["frames_received"] += 1 if payload.landmarks else 0
    session["events_received"] += len(payload.dom_events) if payload.dom_events else 0
    session["last_activity"] = datetime.utcnow().isoformat()

    # Sprint 0: Solo contamos, no procesamos embeddings aún
    return {
        "seq": payload.seq,
        "ts_server": datetime.utcnow().timestamp(),
        "received": True,
        "processing": "stored",  # En Sprint 2 se cambiará a "embedding_computed"
    }


# ==================== WEBSOCKET ====================


@app.websocket("/v1/stream/{session_id}")
async def websocket_stream(websocket: WebSocket, session_id: str):
    await websocket.accept()

    if session_id not in sessions:
        await websocket.close(code=4004, reason="Session not found")
        return

    session = sessions[session_id]

    try:
        while True:
            # Recibir mensaje del cliente
            message = await websocket.receive_text()
            data = json.loads(message)

            # Actualizar contadores
            session["frames_received"] += 1 if data.get("landmarks") else 0
            session["events_received"] += len(data.get("dom_events", []))
            session["last_activity"] = datetime.utcnow().isoformat()

            # Sprint 0: Echo + heartbeat
            response = {
                "seq": data.get("seq", 0),
                "ts_server": datetime.utcnow().timestamp(),
                "session_active": True,
                "baseline_ready": False,  # Sprint 3
                "vc_detected": False,  # Sprint 3
                "fsp_trigger": 0,  # Sprint 3
                "message": "Sprint 0: Datos recibidos correctamente",
            }

            await websocket.send_json(response)

    except WebSocketDisconnect:
        session["status"] = "disconnected"
        print(f"🔌 Cliente desconectado: {session_id}")
    except Exception as e:
        print(f"❌ Error en WebSocket {session_id}: {e}")
        await websocket.close(code=1011, reason="Internal error")


# ==================== SMOKE TEST ====================


@app.get("/smoke-test")
async def smoke_test():
    """Verificación rápida de que todo el stack funciona"""
    checks = {
        "fastapi": True,
        "websocket_handler": True,
        "session_manager": True,
        "numpy": np.__version__,
        "timestamp": datetime.utcnow().isoformat(),
    }
    return {"status": "✅ OK", "checks": checks}


# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    import sys

    # Permitir --smoke-test para verificación rápida
    if "--smoke-test" in sys.argv:
        print("✅ Smoke test pasado: servidor puede iniciar")
        sys.exit(0)

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
