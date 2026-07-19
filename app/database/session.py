from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# 1. Configuration URI (Using aiosqlite for asynchronous SQLite operations)
DATABASE_URL = "sqlite+aiosqlite:///./project_ai_backend.db"

# 2. Asynchronous Engine Core Setup
# We disable 'check_same_thread' exclusively for SQLite worker allocation
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    connect_args={"check_same_thread": False}
)

# 3. Upgraded Modern Session Factory (Replaces your standard sync SessionLocal)
# This binds to our async engine and enforces the AsyncSession wrapper interface
SessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# 4. Clean Dependency Injection Lifecycle Helper
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields an active database transactional session scoped to a single request lifecycle.
    Guarantees automated rollbacks on errors and clean disconnection states.
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
