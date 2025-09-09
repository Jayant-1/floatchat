import json
import logging
import os
import re
from datetime import datetime
from typing import Any, List

from dotenv import load_dotenv


def load_env() -> None:
    # Load .env if present
    load_dotenv()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


_SANITIZE_PATTERN = re.compile(r"[\x00-\x1f\x7f]")


def sanitize_user_input(text: str) -> str:
    # Remove control characters; basic guard against injections in prompts
    safe = _SANITIZE_PATTERN.sub(" ", text or "")
    return safe.strip()


def export_chat_as_txt(messages: List[dict[str, Any]]) -> str:
    lines = []
    for m in messages:
        role = m.get("role", "")
        content = m.get("content", "")
        lines.append(f"[{role}] {content}")
    return "\n".join(lines)


def export_chat_as_json(messages: List[dict[str, Any]]) -> str:
    return json.dumps(messages, ensure_ascii=False, indent=2) 