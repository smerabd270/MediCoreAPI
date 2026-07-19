import uvicorn
from fastapi import FastAPI

# Explicitly import everything needed for engine tracking and schema synchronization
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base

# Mandatory import so Base.metadata becomes aware of the chat table layout
from app.models.chat import ChatLog

app = FastAPI(
    title=settings.APP_NAME,
    description="Hospital Management System Backend",
    version=settings.APP_VERSION,
)

@app.on_event("startup")
async def init_db():
    """
    Automated application startup trigger.
    Inspects storage medium, spawns the local SQLite file, and maps structural schemas.
    """
    print("⏳ Checking and initializing database schemas...")
    async with engine.begin() as conn:
        # Executes table generation sequentially across background worker processes
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database file initialized and 'chat_logs' table verified!")

@app.get("/health", tags=["Monitoring"])
def health_check():
    return {
        "status": "ok",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
