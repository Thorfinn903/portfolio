"""
LLM Provider Factory (v3).
Allows swapping providers without changing controller code.
"""

import os

from app.v3.llm.gemini_client import GeminiClient


def get_llm_client():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower().strip()
    if provider == "gemini":
        return GeminiClient()
    # Future providers: openrouter, local, azure, anthropic, etc.
    return GeminiClient()
