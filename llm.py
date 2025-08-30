"""Lightweight OpenAI client wrapper for chat completions."""

import os
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv

try:
    
    from openai import OpenAI
except Exception:  # pragma: no cover - if openai not installed yet
    OpenAI = None  # type: ignore


load_dotenv()


def _get_client() -> "OpenAI":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY not set. Create a free key and set it in your environment."
        )
    if OpenAI is None:
        raise RuntimeError(
            "openai package not installed. Run: pip install -r requirements.txt"
        )
    return OpenAI(api_key=api_key)


def chat(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 500,
) -> str:
    """
    Send a chat conversation to OpenAI and return assistant text.

    messages: list of {"role": "system|user|assistant", "content": "..."}
    """
    client = _get_client()
    used_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    response = client.chat.completions.create(
        model=used_model,
        temperature=temperature,
        max_tokens=max_output_tokens,
        messages=messages,
    )

    content = response.choices[0].message.content if response.choices else None
    return content or ""


