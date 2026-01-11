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
### Ingest Transcripts
```
python scripts/ingest_transcript.py --raw transcripts/raw/zoom/2026/01/Test_Transcript_Generation_transcript.vtt --source zoom
✅ Transcript ingested
   Transcript ID: zoom_2026_01_test_transcript_generation_transcript
   Processed MD:  /Users/abnagapp/WellnessAtlas-AcademyEngine/transcripts/processed/unassigned/zoom_2026_01_test_transcript_generation_transcript.md
   Registry:      /Users/abnagapp/WellnessAtlas-AcademyEngine/transcripts/registry/zoom_2026_01_test_transcript_generation_transcript.json
python scripts/ingest_transcript.py --raw transcripts/raw/zoom/2025/12/December_2025_Dipika_BuildingFriendshipWithClient.vtt --source zoom
```

### Assign Transcripts to course and lesson
```
python scripts/assign_transcript.py --transcript zoom_2025_12_december_2025_dipika_buildingfriendshipwithclient --course 1_fundamentals_of_wellness --lesson fundamentals-of-wellness-01-01 --method manual
✅ Transcript assigned
   Course: 1_fundamentals_of_wellness
   Lesson: fundamentals-of-wellness-01-01
   
python scripts/validate_courses.py
✔ VALID:   courses/processed/6_growth_momentum_through_clients.json
✔ VALID:   courses/processed/4_basics_of_client_program_tracking.json
✔ VALID:   courses/processed/8_advanced_sales_process_cross_sell.json
✔ VALID:   courses/processed/1_fundamentals_of_wellness.json
✔ VALID:   courses/processed/2_socialmedia_and_brand_building_basics.json
✔ VALID:   courses/processed/5_fundamentals_of_a_coaching_mindset.json
✔ VALID:   courses/processed/7_advanced_wellness_principles.json
✔ VALID:   courses/processed/3_basics_of_weightloss_sales_process.json
✔ VALID:   courses/processed/9_advanced_coaching_mindset.json

🎉 All course files are valid!
```

### Unassign Transcripts
```
python scripts/unassign_transcript.py zoom_2025_12_december_2025_dipika_buildingfriendshipwithclient
```

### Run Tests
```
make test
```
