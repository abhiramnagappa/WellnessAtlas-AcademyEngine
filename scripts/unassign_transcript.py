#!/usr/bin/env python3

import json
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = PROJECT_ROOT / "transcripts" / "registry"
UNASSIGNED_DIR = PROJECT_ROOT / "transcripts" / "processed" / "unassigned"


def load_registry_entry(transcript_id: str) -> dict:
    path = REGISTRY_DIR / f"{transcript_id}.json"
    if not path.exists():
        print(f"❌ Registry entry not found: {path}")
        sys.exit(1)
    return json.loads(path.read_text()), path


def save_registry_entry(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2))


def main():
    if len(sys.argv) < 2:
        print("Usage: python unassign_transcript.py <transcript_id>")
        sys.exit(1)

    transcript_id = sys.argv[1]

    entry, registry_path = load_registry_entry(transcript_id)

    if not entry.get("assigned"):
        print(f"ℹ Transcript '{transcript_id}' is already unassigned")
        return

    current_path = PROJECT_ROOT / entry["processed_path"]
    UNASSIGNED_DIR.mkdir(parents=True, exist_ok=True)
    new_path = UNASSIGNED_DIR / current_path.name

    print("🔄 Unassigning transcript")
    print(f"  Course : {entry['course_id']}")
    print(f"  Lesson : {entry['lesson_id']}")
    print(f"  File   : {current_path} → {new_path}")

    shutil.move(current_path, new_path)

    # Update registry entry
    entry.update({
        "assigned": False,
        "course_id": None,
        "lesson_id": None,
        "assignment_method": None,
        "processed_path": str(new_path.relative_to(PROJECT_ROOT)),
    })

    save_registry_entry(registry_path, entry)

    print("✅ Transcript successfully unassigned")


if __name__ == "__main__":
    main()