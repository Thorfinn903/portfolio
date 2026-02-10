"""
Persona Engine (v3) - Dynamic Recruiter-Aware Persona Switching.
Applies Narayan voice without changing facts or evidence.
"""

from __future__ import annotations

from app.v3.persona.persona_modes import (
    HR_MODE,
    TECHNICAL_MODE,
    MANAGER_MODE,
    FOUNDER_MODE,
    DEFAULT_MODE,
)

PERSONA_CONFIG = {
    "name": "Narayan",
    "tone": "confident_technical_honest",
    "traits": [
        "evidence_driven",
        "practical_engineer",
        "startup_minded",
        "continuous_learner",
    ],
    "speech_rules": [
        "avoid_corporate_fluff",
        "admit_limits_when_needed",
        "prioritize_real_work_examples",
    ],
}


def _variant_for_recruiter(recruiter_type: str) -> str:
    if recruiter_type == "hr_recruiter":
        return "hr"
    if recruiter_type == "technical_reviewer":
        return "technical"
    if recruiter_type == "engineering_manager":
        return "manager"
    if recruiter_type == "founder_cto":
        return "founder"
    return "default"


def apply_dynamic_persona(
    answer: str,
    intent: str,
    strategy: str,
    recruiter_type: str,
) -> tuple[str, str]:
    variant = _variant_for_recruiter(recruiter_type)

    if variant == "hr":
        return HR_MODE, variant
    if variant == "technical":
        return TECHNICAL_MODE, variant
    if variant == "manager":
        return MANAGER_MODE, variant
    if variant == "founder":
        return FOUNDER_MODE, variant

    return DEFAULT_MODE, variant
