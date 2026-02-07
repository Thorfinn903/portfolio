import json
from pathlib import Path

# Base path to /data directory
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_json(filename: str):
    """
    Load a JSON file from the data directory.
    """
    file_path = DATA_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_markdown(filename: str):
    """
    Load a Markdown file from the data directory.
    """
    file_path = DATA_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
