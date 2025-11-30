import os, traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from M8085.api import main as api

app = FastAPI(
    title="8085 Asm Studio",
    description="Simulator for the 8085 microprocessor.",
    version="1.0.0",
)

cors_origins = os.getenv(
    "CORS_ORIGINS", 
    "http://127.185.243.17:4916"

).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

app = FastAPI(title="8085 Microprocessor Simulator API")
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
    return {"status": "ok", "message": "8085 Asm Studio Backend is running."}

@app.get("/")
async def root():
    return {"message": "Welcome to the 8085 Asm Studio Backend!"}

if __name__ == "__main__":
    uvicorn.run("Server.__main__:app", host="127.185.243.18", port=8085)