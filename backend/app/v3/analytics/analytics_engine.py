"""
Analytics Engine (v3.7).
In-memory analytics for intent and recruiter behavior with cross-category mapping.
"""

from __future__ import annotations

from threading import Lock
from typing import Dict, List, Tuple


class AnalyticsEngine:
    _lock = Lock()
    _intent_counts: Dict[str, int] = {}
    _recruiter_types: Dict[str, int] = {}
    _recruiter_intent_map: Dict[str, Dict[str, int]] = {}
    _total_interactions: int = 0

    @classmethod
    def track_interaction(cls, intent: str, recruiter_type: str) -> None:
        with cls._lock:
            cls._total_interactions += 1
            cls._intent_counts[intent] = cls._intent_counts.get(intent, 0) + 1
            cls._recruiter_types[recruiter_type] = cls._recruiter_types.get(recruiter_type, 0) + 1
            if recruiter_type not in cls._recruiter_intent_map:
                cls._recruiter_intent_map[recruiter_type] = {}
            cls._recruiter_intent_map[recruiter_type][intent] = (
                cls._recruiter_intent_map[recruiter_type].get(intent, 0) + 1
            )

    @classmethod
    def _sorted_map(cls, data: Dict[str, int]) -> List[Tuple[str, int]]:
        return sorted(data.items(), key=lambda x: x[1], reverse=True)

    @classmethod
    def get_top_trends(cls) -> List[str]:
        trends: List[str] = []
        for recruiter_type, intents in cls._recruiter_intent_map.items():
            if not intents:
                continue
            top_intent, count = max(intents.items(), key=lambda x: x[1])
            trends.append(
                f"Top Interest for {recruiter_type}: {top_intent} ({count} requests)"
            )
        return trends

    @classmethod
    def get_analytics(cls) -> Dict[str, object]:
        with cls._lock:
            return {
                "total_interactions": cls._total_interactions,
                "intent_counts": cls._sorted_map(cls._intent_counts),
                "recruiter_types": cls._sorted_map(cls._recruiter_types),
                "recruiter_intent_map": cls._recruiter_intent_map,
                "top_trends": cls.get_top_trends(),
            }
