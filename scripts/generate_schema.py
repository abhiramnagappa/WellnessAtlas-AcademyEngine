#!/usr/bin/env python3

"""
Generates a JSON schema from the Course model
and stores it in docs/ontology_schema.json
"""

import json
from pathlib import Path
from backend.app.models.ontology import Course

SCHEMA_PATH = Path("docs/ontology_schema.json")


def main():
    schema = Course.model_json_schema()
    SCHEMA_PATH.write_text(json.dumps(schema, indent=2))
    print(f"Schema generated at {SCHEMA_PATH.resolve()}")


if __name__ == "__main__":
    main()

