"""
Data Access Layer (v3).
Loads content sources and returns structured domain models.
"""

from typing import Dict, Any

from app.data_loader import load_json, load_markdown
from app.v3.models.project import ProjectModel
from app.v3.models.skill import SkillModel
from app.v3.models.experience import ExperienceModel


class DataAccess:
    @staticmethod
    def load_all() -> Dict[str, Any]:
        return {
            "about": load_markdown("about.md"),
            "skills": SkillModel.from_json(load_json("skills.json")),
            "projects": [ProjectModel.from_json(p) for p in load_json("projects.json")],
            "experience": [ExperienceModel.from_json(e) for e in load_json("experience.json")],
            "education": load_json("education.json"),
            "certificates": load_json("certificates.json"),
            "contact": load_json("contact.json"),
        }
