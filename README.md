# DataMark AI
**Real-World Dataset Challenge & AI Evaluation Platform**

A reproducible Python portfolio platform for dataset ingestion, profiling, benchmark task
generation, reference analytics, numerical/JSON evaluation, benchmark reports, FastAPI and
Streamlit. All bundled demo records are **synthetic**, generated with a fixed random seed;
they are not represented as real-world collected data.

## Quick start (Python 3.11+)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/profile_datasets.py
python scripts/generate_tasks.py
python scripts/validate_tasks.py
pytest -v --cov=datamark
streamlit run app/dashboard.py
# second terminal
uvicorn datamark.api.main:app --reload --app-dir src
```
Dashboard: http://localhost:8501 · API docs: http://localhost:8000/docs

## What is included
Six generated domain datasets; 150 challenge records with metadata and difficulty; CSV/JSON/
Excel/Parquet ingestion; cleaning and data quality profiling; reference calculations; evaluation
rubrics; benchmark persistence and exports; REST API; dashboard; tests; notebooks and docs.

## Safety
Untrusted Python submissions are not executed. The adapter fails closed until a separate,
network-isolated sandbox with CPU, memory and time limits is configured. Healthcare examples
are synthetic operations records only, not clinical data. Demo API uploads have no auth; do not
expose publicly without authentication, rate limits, scanning and access controls.

## License
MIT. No third-party public dataset is redistributed in this initial release.
