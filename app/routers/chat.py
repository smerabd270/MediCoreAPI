from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.schemas.chat import ChatHistoryResponse
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
@router.get("/history/{session_id}", response_model=ChatHistoryResponse, status_code=status.HTTP_200_OK)
async def handle_get_history(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    raw_history = await chat_service.get_session_history(session_id)
    return ChatHistoryResponse(session_id=session_id, history=raw_history)
