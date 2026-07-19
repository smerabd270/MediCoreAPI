from fastapi import FastAPI
from app.core.config import settings

from app.database.session import SessionLocal
app = FastAPI(
    title=settings.APP_NAME,
    description="Hospital Management System Backend",
    version=settings.APP_VERSION,
)


@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION
    }