from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.schemas.chat import ChatRequest
from app.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["AI Engine"])

def get_chat_service(db: AsyncSession = Depends(get_db_session)) -> ChatService:
    return ChatService(db_session=db)

@router.post("/stream", status_code=status.HTTP_200_OK)
async def handle_chat_stream(
    payload: ChatRequest, 
    chat_service: ChatService = Depends(get_chat_service)
):
    return StreamingResponse(
        chat_service.stream_chat(payload.session_id, payload.prompt),
        media_type="text/event-stream"
    )
