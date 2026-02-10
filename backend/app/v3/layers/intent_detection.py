"""
Intent Detection Layer (v3).
Classifies recruiter intent from the question + context.
"""

from typing import Dict, Any, List, Tuple


def _score_match(q: str, phrases: List[str], score: float) -> float:
    return score if any(p in q for p in phrases) else 0.0


def rank_intents(question: str, context: Dict[str, Any]) -> List[Tuple[str, float]]:
    q = (question or "").lower().strip()

    scores: Dict[str, float] = {}

    # Role fit / evaluation
    role_fit_phrases = [
        "role fit",
        "good for",
        "fit for",
        "suitable for",
        "hire",
        "hiring",
        "candidate",
        "can he",
        "can she",
        "should we",
        "would you hire",
    ]
    scores["role_fit_evaluation"] = _score_match(q, role_fit_phrases, 0.95)

    # Skills / technologies
    skill_phrases = [
        "skill",
        "skills",
        "technology",
        "tech stack",
        "stack",
        "know",
        "experience with",
        "familiar with",
    ]
    scores["skills_query"] = _score_match(q, skill_phrases, 0.85)

    # Projects
    if "project" in q or "projects" in q or "built" in q:
        scores["project_query"] = max(scores.get("project_query", 0.0), 0.8)

    # Experience / work
    if "experience" in q or "work" in q or "role" in q or "job" in q:
        scores["experience_query"] = max(scores.get("experience_query", 0.0), 0.75)

    # Education
    if "education" in q or "study" in q or "college" in q or "degree" in q:
        scores["education_query"] = max(scores.get("education_query", 0.0), 0.7)

    # Certificates
    if "certificate" in q or "certification" in q:
        scores["certificate_query"] = max(scores.get("certificate_query", 0.0), 0.7)

    # Contact
    if "contact" in q or "email" in q or "phone" in q or "linkedin" in q or "github" in q:
        scores["contact_query"] = max(scores.get("contact_query", 0.0), 0.8)

    # About / summary
    if "about" in q or "who are you" in q or "summary" in q or "profile" in q:
        scores["about_query"] = max(scores.get("about_query", 0.0), 0.8)

    # Personal / hobbies
    personal_phrases = [
        "hobby",
        "hobbies",
        "fun",
        "weekend",
        "passion",
        "interest",
        "life",
        "free time",
    ]
    scores["personal_query"] = max(scores.get("personal_query", 0.0), _score_match(q, personal_phrases, 0.7))

    # Use context if available (fallback to current page)
    current_page = (context or {}).get("current_page")
    if current_page:
        if "projects" in current_page:
            scores["project_query"] = max(scores.get("project_query", 0.0), 0.6)
        if "experience" in current_page:
            scores["experience_query"] = max(scores.get("experience_query", 0.0), 0.6)
        if "education" in current_page:
            scores["education_query"] = max(scores.get("education_query", 0.0), 0.6)
        if "skills" in current_page:
            scores["skills_query"] = max(scores.get("skills_query", 0.0), 0.6)

    # Recent intent trend (soft bias)
    recent_intents = (context or {}).get("recent_intents", [])
    if recent_intents:
        recent = recent_intents[-1]
        scores[recent] = max(scores.get(recent, 0.0), 0.5)

    if not scores:
        return [("unknown_intent", 0.1)]

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked


def detect_intent(question: str, context: Dict[str, Any]) -> str:
    ranked = rank_intents(question, context)
    return ranked[0][0] if ranked else "unknown_intent"
