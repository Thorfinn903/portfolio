"""
Evidence Weighting (v3).
Ranks evidence items based on recruiter priorities.
"""

from __future__ import annotations

from typing import List, Dict, Any


def _rank_order_for_recruiter(recruiter_type: str) -> List[str]:
    if recruiter_type == "hr_recruiter":
        return ["experience", "skills", "projects", "education", "contact", "certificates"]
    if recruiter_type == "technical_reviewer":
        return ["skills", "projects", "experience", "certificates", "education", "contact"]
    if recruiter_type == "engineering_manager":
        return ["experience", "projects", "skills", "certificates", "education", "contact"]
    if recruiter_type == "founder_cto":
        return ["projects", "experience", "skills", "certificates", "education", "contact"]
    return ["experience", "projects", "skills", "certificates", "education", "contact"]


def rank_evidence(evidence_list: List[Dict[str, Any]], recruiter_type: str) -> List[Dict[str, Any]]:
    order = _rank_order_for_recruiter(recruiter_type)
    order_index = {name: idx for idx, name in enumerate(order)}

    def key_fn(item: Dict[str, Any]) -> int:
        src = item.get("source", "unknown")
        return order_index.get(src, len(order_index) + 1)

    return sorted(evidence_list or [], key=key_fn)
