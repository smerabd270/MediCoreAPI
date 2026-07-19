from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """
    Abstract OOP Base class for all database models.
    
    Provides global, standardized auditing fields automatically to every table 
    that inherits from it, ensuring clean code reuse.
    """
    
    # Standardized auto-incrementing Primary Key for all models
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    
    # Automatically tracks when a row is inserted
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    
    # Automatically updates its timestamp whenever a row is modified
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
