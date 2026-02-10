"""
Response Strategy Engine (v3).
Selects how to answer (summary, evidence, comparison, timeline, etc.).
"""

from typing import Dict, Any


def _strategy(
    strategy_type: str,
    tone_style: str,
    evidence_required: bool,
    confidence_required: bool,
) -> Dict[str, Any]:
    return {
        "strategy_type": strategy_type,
        "tone_style": tone_style,
        "evidence_required": evidence_required,
        "confidence_required": confidence_required,
    }


def select_strategy(intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
    if intent == "unknown_intent":
        return _strategy(
            "fallback_strategy",
            "professional_safe",
            False,
            False,
        )

    # Intent -> Strategy mapping (v3 contract)
    if intent == "role_fit_evaluation":
        return _strategy(
            "comparison_strategy",
            "professional_evaluative",
            True,
            True,
        )

    if intent == "project_query":
        return _strategy(
            "evidence_strategy",
            "technical_concise",
            True,
            True,
        )

    if intent == "skills_query":
        return _strategy(
            "summary_strategy",
            "professional_brief",
            False,
            False,
        )

    if intent == "experience_query":
        return _strategy(
            "timeline_strategy",
            "professional_structured",
            True,
            True,
        )

    if intent in {"education_query", "certificate_query", "contact_query"}:
        return _strategy(
            "summary_strategy",
            "professional_brief",
            False,
            False,
        )

    if intent == "about_query":
        return _strategy(
            "highlight_strategy",
            "professional_summary",
            False,
            False,
        )

    # Context-aware fallback
    last_intents = (context or {}).get("recent_intents", [])
    if last_intents:
        recent = last_intents[-1]
        if recent == "project_query":
            return _strategy(
                "evidence_strategy",
                "technical_concise",
                True,
                True,
            )

    return _strategy(
        "summary_strategy",
        "professional_brief",
        False,
        False,
    )
