from sqlalchemy import create_engine

from app.core.config import settings

# SQL Server connection URL
DATABASE_URL = (
    f"mssql+pyodbc://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}"
    f"@{settings.DATABASE_SERVER}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    f"&TrustServerCertificate={'yes' if settings.DATABASE_TRUST_SERVER_CERTIFICATE else 'no'}"
)

# SQLAlchemy Engine (created once for the entire application)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)