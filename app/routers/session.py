import uuid
from fastapi import APIRouter, status
# Change the import path to load from app.schemas.chat
from app.schemas.chat import SessionResponse

router = APIRouter(prefix="/sessions", tags=["Session Manager"])

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_new_chat_session():
    unique_session_id = str(uuid.uuid4())
    return SessionResponse(session_id=unique_session_id)
