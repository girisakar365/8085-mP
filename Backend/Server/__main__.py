"""FastAPI server for the 8085 simulator backend."""

import os
import sys
import traceback
import signal

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from M8085.api import main as api

# Configuration from environment
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8085"))
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
IS_TAURI = os.getenv("TAURI_ENV", "0") == "1"

app = FastAPI(
    title="8085 Microprocessor Simulator",
    description="Simulator for the 8085 microprocessor.",
    version="1.0.0",
)

# CORS configuration - allow connections from various sources
ALLOWED_ORIGINS = [
    # Development
    os.getenv("VITE_DEV_ORIGIN", "http://127.185.243.17:4916"),
    "http://localhost:4916",
    "http://127.0.0.1:4916",
    # Tauri
    os.getenv("TAURI_ORIGIN", "tauri://localhost"),
    "tauri://localhost",
    # Allow any localhost port (for dynamic port support)
    "http://localhost:*",
    "http://127.0.0.1:*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for packaged app compatibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler: returns a JSON 500 for any unhandled error.
    Includes traceback when DEBUG=1.
    """
    tb_list = traceback.extract_tb(exc.__traceback__)
    last = tb_list[-1] if tb_list else None
    payload = {
        "success": False,
        "error": {
            "type": "server_error",
            "message": str(exc),
            "endpoint": f"{request.method} {request.url.path}",
            "location": {
                "file": last.filename if last else None,
                "line": last.lineno if last else None,
                "function": last.name if last else None,
            }
        },
    }

    return JSONResponse(status_code=500, content=payload)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "ok",
        "message": "8085 Microprocessor Simulator Backend is running.",
        "port": BACKEND_PORT,
        "host": BACKEND_HOST,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the 8085 Microprocessor Simulator Backend!"}


@app.get("/config")
async def get_config():
    """Get backend configuration for frontend discovery."""
    return {
        "port": BACKEND_PORT,
        "host": BACKEND_HOST,
        "base_url": f"http://{BACKEND_HOST}:{BACKEND_PORT}",
    }


def graceful_shutdown(signum, frame):
    """Handle graceful shutdown on SIGTERM/SIGINT."""
    print(f"\nReceived signal {signum}. Shutting down gracefully...")
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)
    
    print(f"Starting 8085 Microprocessor Simulator Backend...")
    print(f"  Host: {BACKEND_HOST}")
    print(f"  Port: {BACKEND_PORT}")
    print(f"  Tauri Environment: {IS_TAURI}")
    
    uvicorn.run(
        "Server.__main__:app",
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        log_level="info",
    )
