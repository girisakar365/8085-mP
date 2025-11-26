import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routes.api import docs, assemble, reset, execute, timing

app = FastAPI(
    title="8085 Asm Studio",
    description="Simulator for the 8085 microprocessor.",
    version="1.0.0",
)

cors_origins = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:5173,http://localhost:4173,http://127.0.0.1:5173,http://127.0.0.1:4173,http://localhost"

).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docs.router, prefix="/api", tags=["Documentation"])
app.include_router(timing.router, prefix="/api", tags=["Timing"])
app.include_router(assemble.router, prefix="/api", tags=["Assemble"])
app.include_router(reset.router, prefix="/api", tags=["Reset"])
app.include_router(execute.router, prefix="/api", tags=["Execute"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "8085 Asm Studio Backend is running."}

@app.get("/")
async def root():
    return {"message": "Welcome to the 8085 Asm Studio Backend!"}

if __name__ == "__main__":
    uvicorn.run("Backend.main:app", host="127.0.0.1", port=8000)
