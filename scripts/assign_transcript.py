#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[1]

COURSES_DIR = PROJECT_ROOT / "courses" / "processed"
REGISTRY_DIR = PROJECT_ROOT / "transcripts" / "registry"


def main():
    parser = argparse.ArgumentParser(description="Assign transcript to lesson")
    parser.add_argument("--transcript", required=True, help="Transcript ID (without .md)")
    parser.add_argument("--course", required=True, help="Course ID")
    parser.add_argument("--lesson", required=True, help="Lesson ID")
    parser.add_argument("--method", default="manual", help="Assignment method")

    args = parser.parse_args()

    registry_path = REGISTRY_DIR / f"{args.transcript}.json"
    if not registry_path.exists():
        raise FileNotFoundError(f"Transcript registry not found: {registry_path}")

    course_path = COURSES_DIR / f"{args.course}.json"
    if not course_path.exists():
        raise FileNotFoundError(f"Course not found: {course_path}")

    registry = json.loads(registry_path.read_text())
    course = json.loads(course_path.read_text())

    if registry["assigned"]:
        raise ValueError("Transcript is already assigned")

    lesson_found = False

    for section in course["sections"]:
        for lesson in section["lessons"]:
            if lesson["id"] == args.lesson:
                lesson_found = True
                if lesson.get("transcript_path"):
                    raise ValueError("Lesson already has a transcript")
                lesson["transcript_path"] = registry["processed_path"]

    if not lesson_found:
        raise ValueError(f"Lesson ID not found in course: {args.lesson}")

    registry.update({
        "assigned": True,
        "course_id": args.course,
        "lesson_id": args.lesson,
        "assigned_at": datetime.utcnow().isoformat(),
        "assignment_method": args.method,
    })

    registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    course_path.write_text(json.dumps(course, indent=2), encoding="utf-8")

    print("✅ Transcript assigned")
    print(f"   Course: {args.course}")
    print(f"   Lesson: {args.lesson}")


if __name__ == "__main__":
    main()