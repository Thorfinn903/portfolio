"""
Recruiter Classifier (v3.5).
Classifies recruiter type based on keyword density.
"""

from __future__ import annotations

import logging


TECH_KEYWORDS = [
    "sharding",
    "scale",
    "latency",
    "throughput",
    "cap theorem",
    "microservices",
    "distributed",
    "concurrency",
    "async",
    "database",
    "sql",
    "nosql",
    "redis",
    "caching",
    "optimization",
    "fastapi",
    "system design",
    "deployment",
    "ci/cd",
    "docker",
    "kubernetes",
    "aws",
    "cloud",
]

HR_KEYWORDS = [
    "culture",
    "team",
    "fit",
    "values",
    "hobby",
    "hobbies",
    "fun",
    "weekend",
    "passion",
    "outside work",
    "conflict",
    "weakness",
    "strength",
    "salary",
    "notice period",
    "relocation",
    "remote",
    "soft skills",
]

PRODUCT_KEYWORDS = [
    "roadmap",
    "timeline",
    "deadline",
    "user",
    "customer",
    "impact",
    "metrics",
    "kpi",
    "growth",
    "feature",
    "prioritization",
    "agile",
    "scrum",
]

logger = logging.getLogger("portfolio.v3.recruiter")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)


def _count_keywords(q: str, keywords: list[str]) -> int:
    return sum(1 for k in keywords if k in q)


class RecruiterClassifier:
    @classmethod
    def classify(cls, question: str) -> str:
        q = (question or "").lower()
        tech_hits = _count_keywords(q, TECH_KEYWORDS)
        hr_hits = _count_keywords(q, HR_KEYWORDS)
        product_hits = _count_keywords(q, PRODUCT_KEYWORDS)

        if tech_hits >= 1:
            detected = "TECH_LEAD"
        elif hr_hits >= 1:
            detected = "HR_MANAGER"
        elif product_hits >= 1:
            detected = "PRODUCT_MANAGER"
        else:
            detected = "GENERALIST"

        logger.info(
            "recruiter_type_detected",
            extra={
                "type": detected,
                "tech_hits": tech_hits,
                "hr_hits": hr_hits,
                "product_hits": product_hits,
            },
        )
        return detected


def detect_recruiter_type(question: str, metadata: dict | None = None) -> str:
    """
    Backwards-compatible wrapper for existing callers.
    """
    return RecruiterClassifier.classify(question)
