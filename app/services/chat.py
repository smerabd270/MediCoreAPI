import json
from typing import AsyncGenerator
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.chat import ChatLog

class ChatService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        if getattr(settings, "AI_PROVIDER", "openai").lower() == "ollama":
            self.client = AsyncOpenAI(
                base_url=f"{settings.OLLAMA_BASE_URL}/v1",
                api_key="ollama"
            )
            self.model = settings.OLLAMA_MODEL_NAME
        else:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = getattr(settings, "MODEL_NAME", "gpt-4o")

    async def _get_history(self, session_id: str) -> list[dict]:
        result = await self.db.execute(
            select(ChatLog)
            .filter(ChatLog.session_id == session_id)
            .order_by(ChatLog.created_at.asc())
        )
        logs = result.scalars().all()
        return [{"role": log.role, "content": log.content} for log in logs]

    async def _save_message(self, session_id: str, role: str, content: str) -> None:
        log_entry = ChatLog(session_id=session_id, role=role, content=content)
        self.db.add(log_entry)
        await self.db.commit()

    async def stream_chat(self, session_id: str, prompt: str) -> AsyncGenerator[str, None]:
        history = await self._get_history(session_id)
        await self._save_message(session_id, "user", prompt)
        
        messages = [
            {"role": "system", "content": "You are a stateful assistant integrated into a Hospital Management System backend."}
        ] + history + [{"role": "user", "content": prompt}]

        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            
            accumulated_response = []
            async for chunk in stream:
                if chunk.choices:
                    token = chunk.choices[0].delta.content
                    if token:
                        accumulated_response.append(token)
                        yield json.dumps({"token": token}) + "\n"

            await self._save_message(session_id, "assistant", "".join(accumulated_response))

        except Exception as e:
            yield json.dumps({"error": f"Streaming iteration failed: {str(e)}"})
