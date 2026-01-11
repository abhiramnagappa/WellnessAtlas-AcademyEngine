import json
from pathlib import Path
from typing import List

from backend.app.models.ontology import Course


COURSES_DIR = Path("courses/processed")


def load_all_courses() -> List[Course]:
    courses = []

    for file in sorted(COURSES_DIR.glob("*.json")):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            course = Course(**data)
            courses.append(course)

    return courses