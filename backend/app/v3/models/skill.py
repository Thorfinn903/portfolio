from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SkillModel:
    programming_languages: Dict[str, List[str]]
    databases: Dict[str, List[str]]
    backend: List[str]
    frontend: List[str]
    concepts: List[str]
    tools_platforms: List[str]
    languages_spoken: List[str]

    @staticmethod
    def from_json(payload: Dict[str, Any]) -> "SkillModel":
        return SkillModel(
            programming_languages=payload.get("programming_languages", {}),
            databases=payload.get("databases", {}),
            backend=payload.get("backend", []),
            frontend=payload.get("frontend", []),
            concepts=payload.get("concepts", []),
            tools_platforms=payload.get("tools_platforms", []),
            languages_spoken=payload.get("languages_spoken", []),
        )
