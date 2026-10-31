FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app/src
RUN python scripts/generate_data.py && python scripts/generate_tasks.py
EXPOSE 8000 8501
CMD ["uvicorn","datamark.api.main:app","--host","0.0.0.0","--port","8000"]
