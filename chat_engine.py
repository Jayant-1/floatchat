from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import AsyncGenerator, Dict, Iterable, List, Optional

from utils import get_logger, load_env, sanitize_user_input

logger = get_logger(__name__)
load_env()


@dataclass
class ChatMessage:
    role: str  # "user" | "assistant" | "system"
    content: str


class BaseChatEngine:
    async def stream_reply(self, messages: List[ChatMessage]) -> AsyncGenerator[str, None]:
        raise NotImplementedError


class OpenAIEngine(BaseChatEngine):
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        from openai import OpenAI  # lazy import
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def stream_reply(self, messages: List[ChatMessage]) -> AsyncGenerator[str, None]:
        # Convert to OpenAI format
        payload = [
            {"role": m.role, "content": sanitize_user_input(m.content) if m.role == "user" else m.content}
            for m in messages
        ]
        # Run in thread to avoid blocking
        def _do_stream() -> Iterable[str]:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=payload,
                stream=True,
            )
            for chunk in resp:
                delta = getattr(getattr(chunk, "choices", [{}])[0], "delta", None)
                if delta and delta.get("content"):
                    yield delta["content"]
        loop = asyncio.get_running_loop()
        for token in await loop.run_in_executor(None, lambda: list(_do_stream())):
            yield token


class EchoEngine(BaseChatEngine):
    async def stream_reply(self, messages: List[ChatMessage]) -> AsyncGenerator[str, None]:
        # Simple echo for offline dev
        user_text = next((m.content for m in reversed(messages) if m.role == "user"), "")
        reply = f"Echo: {user_text}"
        for token in reply.split(" "):
            await asyncio.sleep(0.02)
            yield (" " if token != reply.split(" ")[0] else "") + token


def build_engine(provider: str = "openai", **kwargs) -> BaseChatEngine:
    provider = (provider or "openai").lower()
    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            logger.warning("OPENAI_API_KEY not set. Falling back to EchoEngine.")
            return EchoEngine()
        return OpenAIEngine(model=kwargs.get("model", "gpt-4o-mini"))
    # Future: add providers like "ollama", "gemini", etc.
    logger.warning("Unknown provider '%s'. Using EchoEngine.", provider)
    return EchoEngine() 