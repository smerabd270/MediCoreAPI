import os
import sys
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

# CRITICAL FIX: This path injection MUST run before importing any local 'app' modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.database.session import engine
from app.database.base import Base
from app.routers.chat import router as chat_router
from app.routers.session import router as session_router
from app.models.chat import ChatLog

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Checking and initializing database schemas...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database file initialized and 'chat_logs' table verified!")
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description="Hospital Management System Backend",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(session_router)
app.include_router(chat_router)

@app.get("/health", tags=["Monitoring"])
def health_check():
    return {
        "status": "ok",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
