from abc import ABC, abstractmethod
from typing import AsyncGenerator

class BaseAIProvider(ABC):
    """Abstract Interface forcing all AI clients to use the identical stream signature."""
    
    @abstractmethod
    async def generate_stream(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        pass
