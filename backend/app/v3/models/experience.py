from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ExperienceModel:
    role: str
    company: str
    location: str
    duration: str
    responsibilities: List[str]

    @staticmethod
    def from_json(payload: Dict[str, Any]) -> "ExperienceModel":
        return ExperienceModel(
            role=payload.get("role", ""),
            company=payload.get("company", ""),
            location=payload.get("location", ""),
            duration=payload.get("duration", ""),
            responsibilities=payload.get("responsibilities", []),
        )
