#!/usr/bin/env python3

import argparse
from pathlib import Path
from datetime import datetime
import json
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "transcripts" / "processed" / "unassigned"
REGISTRY_DIR = PROJECT_ROOT / "transcripts" / "registry"


def normalize_vtt(text: str) -> str:
    """
    Basic WEBVTT normalizer (v1).
    Removes timestamps and WEBVTT headers.
    Keeps speaker labels if present.
    """
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.upper() == "WEBVTT":
            continue
        if re.match(r"\d\d:\d\d:\d\d\.\d+ -->", line):
            continue
        lines.append(line)
    return "\n".join(lines)


def normalize_plain(text: str) -> str:
    return text.strip()


def normalize_transcript(raw_path: Path) -> str:
    text = raw_path.read_text(encoding="utf-8", errors="ignore")

    if raw_path.suffix.lower() == ".vtt":
        return normalize_vtt(text)

    # Fallback for unknown formats
    return normalize_plain(text)


def extract_year_month(raw_path: Path) -> str:
    """
    Extract YYYY/MM from path if present.
    Returns YYYY_MM or 'unknown'.
    """
    parts = raw_path.parts
    for i in range(len(parts) - 1):
        if re.fullmatch(r"\d{4}", parts[i]) and re.fullmatch(r"\d{2}", parts[i + 1]):
            return f"{parts[i]}_{parts[i + 1]}"
    return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Ingest raw transcript")
    parser.add_argument("--raw", required=True, help="Path to raw transcript file")
    parser.add_argument("--source", required=True, help="Source (zoom, descript, vimeo, etc.)")

    args = parser.parse_args()

    raw_path = Path(args.raw)
    if not raw_path.exists():
        raise FileNotFoundError(raw_path)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

    year_month = extract_year_month(raw_path)
    base_name = raw_path.stem.lower().replace(" ", "_")

    transcript_id = f"{args.source}_{year_month}_{base_name}"

    processed_path = PROCESSED_DIR / f"{transcript_id}.md"
    registry_path = REGISTRY_DIR / f"{transcript_id}.json"

    if processed_path.exists():
        raise ValueError(f"Transcript already ingested: {processed_path}")

    normalized_text = normalize_transcript(raw_path)
    processed_path.write_text(normalized_text, encoding="utf-8")
    processed_path_rel = processed_path.relative_to(PROJECT_ROOT)

    registry = {
        "transcript_id": transcript_id,
        "source": args.source,
        "raw_path": str(raw_path),
        "processed_path": str(processed_path_rel),
        "assigned": False,
        "course_id": None,
        "lesson_id": None,
        "ingested_at": datetime.utcnow().isoformat(),
        "assignment_method": None,
    }

    registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    print("✅ Transcript ingested")
    print(f"   Transcript ID: {transcript_id}")
    print(f"   Processed MD:  {processed_path}")
    print(f"   Registry:      {registry_path}")


if __name__ == "__main__":
    main()