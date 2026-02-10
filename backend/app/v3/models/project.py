from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ProjectModel:
    id: str
    title: str
    domain: str
    description: str
    key_features: List[str]
    tech_stack: List[str]
    status: str

    @staticmethod
    def from_json(payload: Dict[str, Any]) -> "ProjectModel":
        return ProjectModel(
            id=payload.get("id", ""),
            title=payload.get("title", ""),
            domain=payload.get("domain", ""),
            description=payload.get("description", ""),
            key_features=payload.get("key_features", []),
            tech_stack=payload.get("tech_stack", []),
            status=payload.get("status", ""),
        )
