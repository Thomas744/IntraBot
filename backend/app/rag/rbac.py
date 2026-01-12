from pathlib import Path
from typing import Dict, List

BASE_DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "Fintech-data"

ROLE_DOCUMENT_MAP: Dict[str, List[str]] = {
    "finance": ["finance"],
    "marketing": ["marketing"],
    "hr": ["hr"],
    "engineering": ["engineering"],
    "employees": ["general"],
    "c_level": ["finance", "marketing", "hr", "engineering", "general"],
}


def get_allowed_dirs(role: str) -> List[Path]:
    role = role.lower()
    if role not in ROLE_DOCUMENT_MAP:
        raise ValueError("Invalid role")

    dirs = []
    for folder in ROLE_DOCUMENT_MAP[role]:
        path = BASE_DATA_PATH / folder
        if path.exists():
            dirs.append(path)
    return dirs


def roles_for_department(department: str) -> List[str]:
    return sorted(
        role for role, deps in ROLE_DOCUMENT_MAP.items()
        if department in deps
    )
