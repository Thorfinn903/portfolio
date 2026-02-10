"""
Recruiter Psychology Profiles (v3).
Defines recruiter priorities and focus words.
"""

from __future__ import annotations

PROFILES = {
    "hr_recruiter": {
        "priorities": {
            "risk_reduction": "high",
            "team_behavior": "high",
            "technical_depth": "medium",
            "innovation": "low",
        },
        "focus_words": ["reliable", "consistent", "adaptable", "collaborative"],
    },
    "technical_reviewer": {
        "priorities": {
            "technical_depth": "very_high",
            "debugging_skill": "high",
            "architecture": "high",
            "risk_reduction": "medium",
        },
        "focus_words": ["scalable", "optimized", "architecture", "performance"],
    },
    "engineering_manager": {
        "priorities": {
            "delivery": "very_high",
            "ownership": "high",
            "stability": "high",
            "teamwork": "high",
        },
        "focus_words": ["production_ready", "maintainable", "reliable", "delivery"],
    },
    "founder_cto": {
        "priorities": {
            "business_impact": "very_high",
            "scalability": "high",
            "learning_speed": "high",
            "ownership": "very_high",
        },
        "focus_words": ["impact", "scale", "product_value", "automation", "efficiency"],
    },
    "unknown": {
        "priorities": {},
        "focus_words": [],
    },
}
