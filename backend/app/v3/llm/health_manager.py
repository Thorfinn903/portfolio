"""
LLM Health Manager (v3).
Tracks recent failures and cooldowns to auto-disable LLM usage safely.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
import time


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default


@dataclass
class LLMHealthState:
    last_success_ts: float | None = None
    last_failure_ts: float | None = None
    failure_count: int = 0
    disabled_until_ts: float | None = None


class LLMHealthManager:
    def __init__(self) -> None:
        self.state = LLMHealthState()
        self.failure_threshold = _env_int("LLM_FAILURE_THRESHOLD", 3)
        self.cooldown_seconds = _env_int("LLM_COOLDOWN_SECONDS", 300)

    def _now(self) -> float:
        return time.time()

    def status(self) -> str:
        now = self._now()
        if self.state.disabled_until_ts and now < self.state.disabled_until_ts:
            return "disabled"
        if self.state.failure_count > 0:
            return "degraded"
        return "healthy"

    def should_use_llm(self) -> bool:
        now = self._now()
        if self.state.disabled_until_ts and now < self.state.disabled_until_ts:
            return False
        # Cooldown elapsed; reset failures and re-enable
        if self.state.disabled_until_ts and now >= self.state.disabled_until_ts:
            self.state.disabled_until_ts = None
            self.state.failure_count = 0
        return True

    def record_success(self) -> None:
        self.state.last_success_ts = self._now()
        self.state.failure_count = 0
        self.state.disabled_until_ts = None

    def record_failure(self) -> None:
        self.state.last_failure_ts = self._now()
        self.state.failure_count += 1
        if self.state.failure_count >= self.failure_threshold:
            self.state.disabled_until_ts = self._now() + self.cooldown_seconds
