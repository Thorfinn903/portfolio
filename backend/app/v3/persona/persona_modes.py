"""
Persona Modes (v3).
Defines recruiter-aware tone variants.
"""

from __future__ import annotations

HR_MODE = (
    "I’m strongest in backend development using Python and FastAPI.\n"
    "I’ve worked on ERPNext production support where I handled real client issues."
)

TECHNICAL_MODE = (
    "My backend focus is mainly Python-based services using FastAPI.\n"
    "I’m comfortable working with REST APIs, database integration,\n"
    "and production debugging in ERPNext/Frappe environments."
)

MANAGER_MODE = (
    "I’ve worked in production ERP environments where uptime and client response time mattered.\n"
    "I focus on writing maintainable backend systems that teams can extend safely."
)

FOUNDER_MODE = (
    "I like building backend systems that directly support product workflows.\n"
    "In ERPNext work, I saw how backend reliability directly affects business operations."
)

DEFAULT_MODE = (
    "I focus on practical backend delivery with evidence from real work.\n"
    "I’m strongest in Python-based systems and production support where reliability matters."
)
