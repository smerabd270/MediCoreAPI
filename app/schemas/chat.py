from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    prompt: str = Field(..., min_length=1)
    # Added dynamic translation instruction string parameter
    language: str = Field(default="en", description="The target output language for the AI response (e.g., en, ar, fr, es)")

class ChatResponse(BaseModel):
    session_id: str
    response: str

class MessageHistoryItem(BaseModel):
    role: str
    content: str

class ChatHistoryResponse(BaseModel):
    session_id: str
    history: list[MessageHistoryItem]

class SessionResponse(BaseModel):
    session_id: str
