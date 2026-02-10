import json
import os
from pathlib import Path

# Resolve the data directory at runtime to survive different deploy roots.
def _resolve_data_dir():
    env_dir = os.getenv("DATA_DIR", "").strip()
    if env_dir:
        candidate = Path(env_dir).expanduser()
        if candidate.is_dir():
            return candidate.resolve()

    current = Path(__file__).resolve()
    for parent in [current, *current.parents]:
        for folder in ("Data", "data"):
            candidate = parent / folder
            if candidate.is_dir():
                return candidate
    return None


DATA_DIR = _resolve_data_dir()


def _require_data_dir():
    if DATA_DIR is None:
        raise FileNotFoundError(
            "Data directory not found. Ensure the Data/ folder is included in the deployment "
            "or set DATA_DIR to its absolute path."
        )
    return DATA_DIR


def load_json(filename: str):
    """
    Load a JSON file from the data directory.
    """
    data_dir = _require_data_dir()
    file_path = data_dir / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_markdown(filename: str):
    """
    Load a Markdown file from the data directory.
    """
    data_dir = _require_data_dir()
    file_path = data_dir / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
