from sqlalchemy.orm import sessionmaker

from app.database.engine import engine

# Factory for creating database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)