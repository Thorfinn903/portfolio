"""
Recruiter Psychology Engine (v3).
Reorders evidence and reframes answer without changing facts.
"""

from __future__ import annotations

from typing import List, Dict, Any, Tuple

from app.v3.psychology.evidence_weighting import rank_evidence
from app.v3.psychology.recruiter_psychology_profiles import PROFILES


def _summarize_evidence(evidence: List[Dict[str, Any]]) -> str:
    if not evidence:
        return "Evidence: None available."

    lines = ["Evidence:"]
    for ev in evidence[:4]:
        src = ev.get("source", "unknown")
        if src == "projects":
            title = ev.get("title") or ev.get("id") or "project"
            domain = ev.get("domain")
            detail = f"{title}" + (f" ({domain})" if domain else "")
            lines.append(f"- Project: {detail}")
        elif src == "experience":
            role = ev.get("role") or "role"
            company = ev.get("company")
            detail = f"{role}" + (f" at {company}" if company else "")
            lines.append(f"- Experience: {detail}")
        elif src == "skills":
            backend = ev.get("backend") or []
            frontend = ev.get("frontend") or []
            snippet = ", ".join((backend + frontend)[:4]) if isinstance(backend, list) else "skills listed"
            lines.append(f"- Skills: {snippet}")
        elif src == "education":
            degree = ev.get("degree") or "degree"
            institution = ev.get("institution")
            detail = f"{degree}" + (f" at {institution}" if institution else "")
            lines.append(f"- Education: {detail}")
        elif src == "certificates":
            name = ev.get("name") or ev.get("title") or "certificate"
            issuer = ev.get("issuer")
            detail = f"{name}" + (f" ({issuer})" if issuer else "")
            lines.append(f"- Certificate: {detail}")
        else:
            lines.append(f"- {src}: listed")
    return "\n".join(lines)


def apply_psychology_layer(
    answer: str,
    evidence: List[Dict[str, Any]],
    recruiter_type: str,
    intent: str,
) -> Tuple[str, List[Dict[str, Any]], str, bool]:
    if intent == "unknown_intent":
        return answer, evidence, "unknown", False

    ranked = rank_evidence(evidence, recruiter_type)
    profile_name = recruiter_type if recruiter_type in PROFILES else "unknown"

    evidence_block = _summarize_evidence(ranked)

    if recruiter_type == "hr_recruiter":
        reframed = (
            "Stability & Reliability\n"
            f"{answer}\n\n"
            f"{evidence_block}\n\n"
            "Technical Support Summary\n"
            "Focus on production support and consistent delivery.\n\n"
            "Growth Mindset\n"
            "Open to feedback and continuous learning."
        )
    elif recruiter_type == "technical_reviewer":
        reframed = (
            "Core Technical Strength\n"
            f"{answer}\n\n"
            "Architecture Exposure\n"
            "Experience includes backend services and production debugging.\n\n"
            "Real Debugging Proof\n"
            f"{evidence_block}\n\n"
            "Stack Summary\n"
            "Backend-first stack with production support exposure."
        )
    elif recruiter_type == "engineering_manager":
        reframed = (
            "Delivery Reliability\n"
            f"{answer}\n\n"
            "Production Experience\n"
            f"{evidence_block}\n\n"
            "Ownership Signals\n"
            "Focus on maintainable systems and reliable execution.\n\n"
            "Tech Summary\n"
            "Backend-first, practical delivery orientation."
        )
    elif recruiter_type == "founder_cto":
        reframed = (
            "Business Impact\n"
            f"{answer}\n\n"
            "System Thinking\n"
            "Focus on systems that support product workflows and reliability.\n\n"
            "Scaling Readiness\n"
            f"{evidence_block}\n\n"
            "Tech Foundation\n"
            "Backend-first stack with production exposure."
        )
    else:
        reframed = f"{answer}\n\n{evidence_block}"

    return reframed, ranked, profile_name, True
