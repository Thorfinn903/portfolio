import os
import asyncio
from google import genai


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            self.enabled = False
            return

        self.client = genai.Client(api_key=api_key)
        self.enabled = True

    async def rewrite(self, text: str, *, intent: str | None = None, strategy: str | None = None):
        if not self.enabled:
            return {
                "text": text,
                "used": False,
                "error": False,
                "error_reason": None,
            }

        try:
            def blocking_call():
                intent_hint = intent or "unknown"
                strategy_hint = strategy or "summary"
                return self.client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"""
Rewrite safely.
Do not add new facts.
Keep meaning identical.
Preserve any evidence and claims.
Tone: professional, recruiter-friendly.
Intent: {intent_hint}
Strategy: {strategy_hint}

TEXT:
{text}
""",
                )

            response = await asyncio.wait_for(
                asyncio.to_thread(blocking_call),
                timeout=5,
            )

            return {
                "text": response.text,
                "used": True,
                "error": False,
                "error_reason": None,
            }

        except Exception as e:
            return {
                "text": text,
                "used": False,
                "error": True,
                "error_reason": str(e),
            }
