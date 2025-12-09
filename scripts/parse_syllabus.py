import json
import re
import sys
from pathlib import Path
from slugify import slugify

"""
USAGE:
python scripts/parse_syllabus.py syllabus.txt courses/fundamentals.json
"""

# Match durations at the end like (19:22) or (1:02:19)
DURATION_REGEX = re.compile(r"\((\d+):(\d+)(?::(\d+))?\)$")

# Match (~40 hrs) or (40 hrs) or (about 40 hrs)
HOURS_REGEX = re.compile(r"\(.*?hrs?\)", re.IGNORECASE)


def strip_hours_from_title(title: str) -> str:
    """
    Remove (~40 hrs) or similar from course title
    or any other hours hint.
    """
    return HOURS_REGEX.sub("", title).strip()


def parse_duration_to_seconds(title_str: str):
    """
    Extract duration from a string like:
    "Some title (19:22)" or "Some (1:02:19)"
    Returns int seconds or None
    """
    match = DURATION_REGEX.search(title_str.strip())
    if not match:
        return None

    h = match.group(1)
    m = match.group(2)
    s = match.group(3)

    if s is not None:
        # HH:MM:SS
        hours = int(h)
        minutes = int(m)
        seconds = int(s)
        return hours * 3600 + minutes * 60 + seconds
    else:
        # MM:SS
        minutes = int(h)
        seconds = int(m)
        return minutes * 60 + seconds


def normalize_section_number(sec_str: str) -> str:
    """
    Convert '1' -> '01', '10' -> '10'
    """
    return sec_str.zfill(2)


def normalize_lesson_number(lesson_str: str) -> (str, str):
    """
    Convert '1.2' -> ('01', '02')
    """
    sec, les = lesson_str.split(".")
    return sec.zfill(2), les.zfill(2)


def parse_syllabus(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # First line = course title
    raw_course_title = lines[0]
    clean_title = strip_hours_from_title(raw_course_title)
    course_id = slugify(clean_title)

    sections = []
    current_section = None

    for line in lines[1:]:
        # Section: "1. Title"
        sec_match = re.match(r"^(\d+)\.\s+(.*)$", line)
        if sec_match:
            sec_number, sec_title = sec_match.groups()
            sec_norm = normalize_section_number(sec_number)

            current_section = {
                "id": f"{course_id}-{sec_norm}",
                "number": sec_norm,
                "title": sec_title.strip(),
                "lessons": []
            }
            sections.append(current_section)
            continue

        # Lesson: "1.1 Title (duration)"
        lesson_match = re.match(r"^(\d+\.\d+)\.\s+(.*)$", line)
        if lesson_match:
            lesson_number, lesson_title = lesson_match.groups()

            # parse duration
            duration_sec = parse_duration_to_seconds(lesson_title)
            # strip duration from the title
            clean_lesson_title = DURATION_REGEX.sub("", lesson_title).strip()

            # generate lesson ID
            sec_part, les_part = normalize_lesson_number(lesson_number)
            lesson_id = f"{course_id}-{sec_part}-{les_part}"

            lesson = {
                "id": lesson_id,
                "number": f"{sec_part}.{les_part}",
                "title": clean_lesson_title,
                "duration_seconds": duration_sec,
                "type": "video",
                "video_url": None,
                "transcript_path": None,
                "attachments": [],
                "quiz": None
            }

            if current_section is not None:
                current_section["lessons"].append(lesson)
            continue

    return {
        "id": course_id,
        "title": clean_title,
        "raw_title": raw_course_title,
        "sections": sections
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python parse_syllabus.py syllabus.txt output.json")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    text = input_file.read_text(encoding="utf-8")
    course_data = parse_syllabus(text)

    output_file.write_text(
        json.dumps(course_data, indent=2),
        encoding="utf-8"
    )

    print(f"Wrote course json to {output_file}")


if __name__ == "__main__":
    main()

