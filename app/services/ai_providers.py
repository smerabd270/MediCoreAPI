import json
from typing import AsyncGenerator
from openai import AsyncOpenAI
from app.services.ai_base import BaseAIProvider
from app.core.config import settings

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME

    async def generate_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        async range for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield token


class OllamaProvider(BaseAIProvider):
    def __init__(self):
        # Ollama runs standard OpenAI-compatible API configurations locally!
        self.client = AsyncOpenAI(
            base_url=f"{settings.OLLAMA_BASE_URL}/v1",
            api_key="ollama" # Static placeholder value required by client validation
        )
        self.model = settings.OLLAMA_MODEL_NAME

    async def generate_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        async for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield token
