#!/usr/bin/env python3

"""
Validates all course definitions against the Course ontology.
Looks for files inside /courses/**/course.yaml
"""

from pathlib import Path
import yaml
from backend.app.models.ontology import Course


def validate_course(file: Path):
    data = yaml.safe_load(file.read_text())
    Course(**data)


def main():
    base = Path("courses/processed")
    files = list(base.rglob("*.json"))
    
    if not files:
        print("No course.yaml files found.")
        return
    
    errors_found = False
    
    for file in files:
        try:
            validate_course(file)
            print(f"✔ VALID:   {file}")
        except Exception as e:
            errors_found = True
            print(f"✘ INVALID: {file}")
            print(f"    Error: {e}")
    
    if errors_found:
        exit(1)
    else:
        print("\n🎉 All course files are valid!")


if __name__ == "__main__":
    main()

