data:
	python scripts/generate_data.py
tasks:
	python scripts/generate_tasks.py
test:
	pytest -v --cov=datamark
api:
	uvicorn datamark.api.main:app --reload
dashboard:
	streamlit run app/dashboard.py
