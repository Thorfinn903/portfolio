"""
Context Manager (v3).
Stores and retrieves session context (page, intents, summary, etc.).
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class ContextState:
    session_id: str | None = None
    current_page: str | None = None
    last_project_viewed: str | None = None
    recent_intents: List[str] = field(default_factory=list)
    conversation_summary: str | None = None
    last_entities: Dict[str, Any] | None = None


_STORE: Dict[str, ContextState] = {}


class ContextManager:
    @staticmethod
    def load(session_id: str | None) -> Dict[str, Any]:
        if not session_id:
            return ContextState().__dict__
        if session_id not in _STORE:
            _STORE[session_id] = ContextState(session_id=session_id)
        return _STORE[session_id].__dict__

    @staticmethod
    def update(
        session_id: str | None,
        *,
        current_page: str | None = None,
        last_project_viewed: str | None = None,
        last_entities: Dict[str, Any] | None = None,
        intent: str | None = None,
        question: str | None = None,
    ) -> Dict[str, Any]:
        if not session_id:
            return ContextState().__dict__
        state = _STORE.get(session_id) or ContextState(session_id=session_id)

        if current_page:
            state.current_page = current_page
        if last_project_viewed:
            state.last_project_viewed = last_project_viewed
        if last_entities:
            state.last_entities = last_entities
        if intent:
            state.recent_intents.append(intent)
            state.recent_intents = state.recent_intents[-5:]
        if question:
            # Simple rolling summary (placeholder for real summarizer)
            state.conversation_summary = question

        _STORE[session_id] = state
        return state.__dict__
