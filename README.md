# WellnessAtlas-AcademyEngine

A toolkit for organizing, updating, and enriching (eventually) the Wellness Atlas Academy curriculum.

# Prerequisites
```
pip install python-slugify
pip install chromadb
pip install sentence-transformers
```

## Development
Course Ontology Schema is present inside docs/ontology.schema.json

Copy the course headings to a file inside courses/raw. Example courses/raw/1_fundamental_of_wellness.txt

Run this command to generate course ontology
```
python scripts/parse_syllabus.py courses/raw/<raw_file>.txt courses/processed/<file_to_be_created>.json
```
Example
```
python scripts/parse_syllabus.py courses/raw/1_fundamentals_of_wellness.txt courses/processed/1_fundamentals_of_wellness.json
```

If you change anything in ontology.py, make sure you generate the schema.
To Generate/Regenerate (I said regenerate, not degenerate :-)) the schema, you can use
```
export PYTHONPATH=.
python scripts/generate_schema.py
```

Make sure you validate course ontology everytime you generate the schema
or everytime you generate a new version of a course.
To validate generated course ontology against the schema, you can use
```
(base) xxxx@xxxx-mac WellnessAtlas-AcademyEngine % pwd
/Users/xxxx/WellnessAtlas-AcademyEngine
export PYTHONPATH=.
python scripts/validate_courses.py
✔ VALID:   courses/processed/1_fundamentals_of_wellness.json

🎉 All course files are valid!
```
### Run UI
```
streamlit run ui/app.py
```

### Run Tests
```
make test
```
