import json
from typing import AsyncGenerator
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.chat import ChatLog
from app.services.vector_store import VectorStoreManager

class OpenAIProvider:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME

    async def generate_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        async for chunk in stream:
            # FIX: Access the first element of the choices list array safely
            if hasattr(chunk, 'choices') and chunk.choices:
                token = chunk.choices[0].delta.content
                if token:
                    yield token

class OllamaProvider:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=f"{settings.OLLAMA_BASE_URL}/v1",
            api_key="ollama"
        )
        self.model = settings.OLLAMA_MODEL_NAME

    async def generate_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        async for chunk in stream:
            # FIX: Access the first element of the choices list array safely
            if hasattr(chunk, 'choices') and chunk.choices:
                token = chunk.choices[0].delta.content
                if token:
                    yield token

class ChatService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.vector_store = VectorStoreManager()
        if getattr(settings, "AI_PROVIDER", "openai").lower() == "ollama":
            self.ai_client = OllamaProvider()
        else:
            self.ai_client = OpenAIProvider()

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

    async def get_session_history(self, session_id: str) -> list[dict]:
        return await self._get_history(session_id)

    async def stream_chat(self, session_id: str, prompt: str, language: str = "en") -> AsyncGenerator[str, None]:
        history = await self._get_history(session_id)
        await self._save_message(session_id, "user", prompt)
        
        retrieved_context = self.vector_store.query_similarity(prompt, n_results=3)
        
        system_instruction = (
            "You are a stateful clinical assistant integrated into a Hospital Management System backend. "
            "Analyze the user request using the provided retrieved context facts below. "
            "Do not output the raw context text. Instead, synthesize the answer cleanly and professionally based on these facts.\n"
            f"CRITICAL CONSTRAINT: You MUST write your entire response strictly in this language format: '{language}'. "
            "Translate all concepts cleanly to match that specified language output requirement seamlessly.\n\n"
            f"--- RETRIEVED HOSPITAL FACTS ---\n{retrieved_context}"
        )

        messages = [
            {"role": "system", "content": system_instruction}
        ] + history + [{"role": "user", "content": prompt}]

        try:
            accumulated_response = []
            async for token in self.ai_client.generate_stream(messages):
                accumulated_response.append(token)
                yield token

            await self._save_message(session_id, "assistant", "".join(accumulated_response))

        except Exception as e:
            yield f"\n[Streaming iteration failed: {str(e)}]"
