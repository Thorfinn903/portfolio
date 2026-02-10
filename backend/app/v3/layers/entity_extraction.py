"""
Entity Extraction (v3).
Detects project names, tech stack mentions, role types, and domain keywords.
"""

from typing import Dict, Any, List

from app.v3.data.data_access import DataAccess


def _normalize(text: str) -> str:
    return text.lower().strip()


def extract_entities(question: str) -> Dict[str, Any]:
    q = _normalize(question or "")
    data = DataAccess.load_all()

    projects = []
    tech_stack = []
    roles = []
    domains = []

    # Project names + domains
    for p in data.get("projects", []):
        if _normalize(p.title) in q or _normalize(p.id) in q:
            projects.append(p.title)
        if p.domain and _normalize(p.domain) in q:
            domains.append(p.domain)

        for tech in p.tech_stack:
            if _normalize(tech) in q:
                tech_stack.append(tech)

    # Skills tech stack mentions
    skills = data.get("skills")
    if skills:
        for tech in skills.backend + skills.frontend + skills.tools_platforms:
            if _normalize(tech) in q:
                tech_stack.append(tech)

    # Role types from experience
    for e in data.get("experience", []):
        if e.role and _normalize(e.role) in q:
            roles.append(e.role)

    # Heuristic role keywords
    role_keywords = ["backend", "frontend", "full stack", "fullstack", "devops", "data", "ai"]
    for rk in role_keywords:
        if rk in q:
            roles.append(rk)

    # Deduplicate while preserving order
    def dedupe(items: List[str]) -> List[str]:
        seen = set()
        out = []
        for item in items:
            key = _normalize(item)
            if key not in seen:
                seen.add(key)
                out.append(item)
        return out

    return {
        "projects": dedupe(projects),
        "tech_stack": dedupe(tech_stack),
        "roles": dedupe(roles),
        "domains": dedupe(domains),
    }
