"""
Domain Rules Engine (v3).
Produces evidence-backed answers from structured domain models.
"""

from dataclasses import dataclass
from typing import Dict, Any, List

from app.v3.data.data_access import DataAccess


@dataclass
class RawAnswer:
    answer: str
    evidence: List[Dict[str, Any]]
    confidence_score: float


def _match_strength(text: str, question: str) -> float:
    if not text:
        return 0.0
    q = question.lower()
    t = text.lower()
    return 1.0 if any(word in t for word in q.split()) else 0.3


def _intent_evidence(data: Dict[str, Any], intent: str) -> List[Dict[str, Any]]:
    evidence: List[Dict[str, Any]] = []

    if intent == "project_query":
        for p in data["projects"]:
            evidence.append(
                {
                    "source": "projects",
                    "id": p.id,
                    "title": p.title,
                    "domain": p.domain,
                    "tech_stack": p.tech_stack,
                }
            )
    elif intent == "experience_query":
        for e in data["experience"]:
            evidence.append(
                {
                    "source": "experience",
                    "role": e.role,
                    "company": e.company,
                    "duration": e.duration,
                }
            )
    elif intent == "skills_query":
        skills = data["skills"]
        evidence.append(
            {
                "source": "skills",
                "backend": skills.backend,
                "frontend": skills.frontend,
                "languages": skills.programming_languages,
            }
        )
    elif intent == "education_query":
        for e in data["education"]:
            evidence.append(
                {
                    "source": "education",
                    "degree": e.get("degree"),
                    "institution": e.get("institution"),
                    "duration": e.get("duration"),
                }
            )
    elif intent == "certificate_query":
        for c in data["certificates"]:
            evidence.append(
                {
                    "source": "certificates",
                    "name": c.get("name"),
                    "issuer": c.get("issuer"),
                    "year": c.get("year"),
                }
            )
    elif intent == "contact_query":
        contact = data.get("contact") or {}
        evidence.append(
            {
                "source": "contact",
                "email": contact.get("email"),
                "phone": contact.get("phone"),
                "linkedin": contact.get("linkedin"),
                "github": contact.get("github"),
            }
        )
    return evidence


def _confidence_score(question: str, evidence: List[Dict[str, Any]], intent: str) -> float:
    if not evidence:
        return 0.2
    # Simple scoring: match strength + intent relevance + recency hint
    match = 0.0
    for ev in evidence:
        match = max(match, _match_strength(str(ev), question))

    intent_bonus = 0.2 if intent in {"project_query", "experience_query", "skills_query"} else 0.1

    # Recency heuristic: if question mentions "latest/recent/current"
    q = question.lower()
    recency = 0.2 if any(k in q for k in ["recent", "latest", "current"]) else 0.0

    score = min(1.0, 0.4 + match * 0.3 + intent_bonus + recency)
    return round(score, 2)


def _find_tech_mentions(question: str, data: Dict[str, Any]) -> List[str]:
    q = (question or "").lower()
    skills = data["skills"]
    candidates = (
        skills.backend
        + skills.frontend
        + skills.tools_platforms
        + skills.programming_languages.get("primary", [])
        + skills.programming_languages.get("core", [])
    )
    hits = []
    for tech in candidates:
        if tech.lower() in q:
            hits.append(tech)
    return hits


def _fallback_evidence(question: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
    q = (question or "").lower()
    fallback: List[Dict[str, Any]] = []

    # Skills mentions
    skills = data.get("skills")
    if skills:
        skill_candidates = skills.backend + skills.frontend + skills.tools_platforms
        matched_skills = [s for s in skill_candidates if s.lower() in q]
        if matched_skills:
            fallback.append(
                {
                    "source": "skills",
                    "matched": matched_skills[:5],
                }
            )

    # Projects mentions
    for p in data.get("projects", []):
        if p.title and p.title.lower() in q:
            fallback.append(
                {
                    "source": "projects",
                    "id": p.id,
                    "title": p.title,
                    "domain": p.domain,
                    "tech_stack": p.tech_stack,
                }
            )

    # Experience mentions
    for e in data.get("experience", []):
        role = (e.role or "").lower()
        company = (e.company or "").lower()
        if role in q or company in q:
            fallback.append(
                {
                    "source": "experience",
                    "role": e.role,
                    "company": e.company,
                    "duration": e.duration,
                }
            )

    # Education mentions
    for e in data.get("education", []):
        degree = (e.get("degree") or "").lower()
        institution = (e.get("institution") or "").lower()
        if degree in q or institution in q:
            fallback.append(
                {
                    "source": "education",
                    "degree": e.get("degree"),
                    "institution": e.get("institution"),
                    "duration": e.get("duration"),
                }
            )

    return fallback


def _ensure_min_evidence(
    evidence: List[Dict[str, Any]], intent: str, data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    out = list(evidence or [])
    sources = {e.get("source") for e in out if isinstance(e, dict)}

    def add_project():
        if data.get("projects"):
            p = data["projects"][0]
            out.append(
                {
                    "source": "projects",
                    "id": p.id,
                    "title": p.title,
                    "domain": p.domain,
                    "tech_stack": p.tech_stack,
                }
            )

    def add_skills():
        skills = data.get("skills")
        if skills:
            out.append(
                {
                    "source": "skills",
                    "backend": skills.backend,
                    "frontend": skills.frontend,
                    "languages": skills.programming_languages,
                }
            )

    def add_experience():
        if data.get("experience"):
            e = data["experience"][0]
            out.append(
                {
                    "source": "experience",
                    "role": e.role,
                    "company": e.company,
                    "duration": e.duration,
                }
            )

    def add_education():
        if data.get("education"):
            e = data["education"][0]
            out.append(
                {
                    "source": "education",
                    "degree": e.get("degree"),
                    "institution": e.get("institution"),
                    "duration": e.get("duration"),
                }
            )

    if intent == "project_query" and "projects" not in sources:
        add_project()
    if intent == "skills_query" and "skills" not in sources:
        add_skills()
    if intent == "experience_query" and "experience" not in sources:
        add_experience()

    if intent == "role_fit_evaluation":
        while len(out) < 2:
            if "skills" not in sources:
                add_skills()
                sources.add("skills")
                continue
            if "experience" not in sources:
                add_experience()
                sources.add("experience")
                continue
            if "projects" not in sources:
                add_project()
                sources.add("projects")
                continue
            if "education" not in sources:
                add_education()
                sources.add("education")
                continue
            break

    if not out:
        add_skills()

    return out


def handle_unknown_intent(context: Dict[str, Any] | None = None) -> RawAnswer:
    return RawAnswer(
        answer=(
            "I can only answer questions about Narayan’s professional profile, "
            "skills, projects, and experience. "
            "If you are evaluating him for a role, you can ask about backend skills, "
            "projects, or experience."
        ),
        evidence=[],
        confidence_score=0.0,
    )


def run_rules(question: str, intent: str, strategy: Dict[str, Any], context: Dict[str, Any]) -> RawAnswer:
    data = DataAccess.load_all()
    if intent == "unknown_intent":
        return handle_unknown_intent(context)
    evidence = _intent_evidence(data, intent)
    strategy_type = strategy.get("strategy_type", "summary_strategy")
    entities = (context or {}).get("last_entities") or {}

    # Strategy-driven responses
    if strategy_type == "comparison_strategy":
        answer = (
            "Fit summary: Strong backend focus (Python, FastAPI, Flask) with ERPNext/Frappe production support and "
            "delivery of B2B systems.\n"
            "Evidence highlights: ERPNext support role handling live client issues; projects include Digital Dukan and ClickMart.\n"
            "Considerations: Limited explicit large-team leadership signals; experience is early-career.\n"
            "Confidence: Medium (based on portfolio data only)."
        )
    elif strategy_type == "evidence_strategy":
        if intent == "project_query" and entities.get("projects"):
            project_title = entities["projects"][0]
            project = next((p for p in data["projects"] if p.title == project_title), None)
            if project:
                answer = (
                    f"Project: {project.title}\n"
                    f"Domain: {project.domain}\n"
                    f"Summary: {project.description}\n"
                    f"Key features: " + "; ".join(project.key_features)
                )
                evidence = [
                    {
                        "source": "projects",
                        "id": project.id,
                        "title": project.title,
                        "domain": project.domain,
                        "tech_stack": project.tech_stack,
                        "key_features": project.key_features,
                    }
                ]
            else:
                answer = "Project details are available in the portfolio data."
        elif intent == "skills_query":
            tech_hits = _find_tech_mentions(question, data)
            if tech_hits:
                tech = tech_hits[0]
                projects_using = [
                    p.title for p in data["projects"] if tech in p.tech_stack
                ]
                answer = (
                    f"Evidence for {tech}:\n"
                    f"- Skill listing: {tech if tech in data['skills'].backend else 'Listed outside backend skills'}\n"
                    f"- Projects: {', '.join(projects_using) if projects_using else 'No project lists it explicitly'}\n"
                    f"- Production exposure: ERPNext/Frappe support role with live client issue resolution."
                )
            else:
                answer = "Skills evidence is available across backend, frontend, databases, and tools."
        else:
            answer = "Evidence-backed details are available for this request."
    elif strategy_type == "summary_strategy":
        if intent == "skills_query":
            answer = "Skills span backend, frontend, databases, and tools with a backend-first focus."
        elif intent == "project_query":
            answer = "Projects emphasize real-world delivery with clear outcomes."
        elif intent == "experience_query":
            answer = "Experience includes ERPNext support and React development roles."
        elif intent == "education_query":
            answer = "Education includes a BE in Computer Science and a Diploma in CS."
        elif intent == "certificate_query":
            answer = "Certifications are listed with issuer and year in the portfolio data."
        elif intent == "contact_query":
            answer = "Contact details are available in the portfolio data."
        elif intent == "about_query":
            answer = "This portfolio highlights a backend-focused engineer with production support and project delivery experience."
        else:
            answer = "Here is a concise portfolio summary based on your request."
    else:
        answer = "Here is a structured portfolio summary based on your request."

    if not evidence:
        evidence = _fallback_evidence(question, data)
    evidence = _ensure_min_evidence(evidence, intent, data)
    confidence_score = _confidence_score(question, evidence, intent)

    return RawAnswer(
        answer=answer,
        evidence=evidence,
        confidence_score=confidence_score,
    )
