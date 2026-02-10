"""
Session Manager (v4).
In-memory session state for recruiter type persistence.
"""

from __future__ import annotations

from threading import Lock
from typing import Dict, Optional


class SessionManager:
    _lock = Lock()
    _sessions: Dict[str, Dict[str, Optional[str]]] = {
        "default_user": {"type": None}
    }

    _specific_types = {"TECH_LEAD", "HR_MANAGER", "PRODUCT_MANAGER"}

    @classmethod
    def _ensure_session(cls, user_id: str) -> Dict[str, Optional[str]]:
        if user_id not in cls._sessions:
            cls._sessions[user_id] = {"type": None}
        return cls._sessions[user_id]

    @classmethod
    def update_session(cls, user_id: str, new_type: str | None) -> None:
        with cls._lock:
            session = cls._ensure_session(user_id)
            current = session.get("type")
            if new_type in cls._specific_types:
                session["type"] = new_type
            elif current in cls._specific_types and new_type == "GENERALIST":
                return
            else:
                session["type"] = new_type

    @classmethod
    def get_session(cls, user_id: str) -> Optional[str]:
        with cls._lock:
            session = cls._ensure_session(user_id)
            return session.get("type")
