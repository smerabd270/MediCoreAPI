from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class ChatLog(Base):
    """
    OOP Database Model for tracking user interactions and AI completions.
    Inherits automatic ID and Auditing timestamps from app.database.base.Base.
    """
    __tablename__ = "chat_logs"

    # Group identifier to keep different user chat sessions isolated
    session_id: Mapped[str] = mapped_column(
        String(100), 
        index=True, 
        nullable=False
    )
    
    # Dictates who sent the message: 'user' or 'assistant'
    role: Mapped[str] = mapped_column(
        String(20), 
        nullable=False
    )
    
    # The actual text contents of the message exchange
    content: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
