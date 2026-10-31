
import sys
from pathlib import Path

# Make the src directory available for Python imports on Vercel
PROJECT_SRC = Path(__file__).resolve().parents[2]
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

from datamark.config import DATA_DIR, TASKS_FILE
from datamark.generators.tasks import build_tasks, write_tasks
from datamark.profiling.profile import profile_dataframe
from datamark.ingestion.reader import read_dataset
from datamark.evaluation.evaluator import evaluate_numeric

import json

app = FastAPI(title="DataMark AI API", version="1.0.0")


class Eval(BaseModel):
    expected: float
    actual: float
    abs_tol: float = Field(0.01, ge=0)
    rel_tol: float = Field(0.0001, ge=0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/datasets")
def datasets():
    return [
        {"dataset_id": p.stem, "path": str(p)}
        for p in DATA_DIR.rglob("*.csv")
    ] if DATA_DIR.exists() else []


@app.post("/datasets/upload")
async def upload(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()

    if ext not in {".csv", ".json", ".xlsx", ".xls", ".parquet"}:
        raise HTTPException(400, "unsupported file")

    content = await file.read()

    if len(content) > 25 * 1024 * 1024:
        raise HTTPException(413, "25 MB limit")

    dest = DATA_DIR / "external" / Path(file.filename).name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)

    return {
        "dataset_id": dest.stem,
        "filename": dest.name
    }


@app.get("/datasets/{dataset_id}")
def detail(dataset_id: str):
    found = list(DATA_DIR.rglob(dataset_id + ".csv"))

    if not found:
        raise HTTPException(404, "not found")

    df = read_dataset(found[0])

    return {
        "rows": len(df),
        "columns": list(df.columns)
    }


@app.get("/datasets/{dataset_id}/profile")
def profile(dataset_id: str):
    found = list(DATA_DIR.rglob(dataset_id + ".csv"))

    if not found:
        raise HTTPException(404, "not found")

    return profile_dataframe(read_dataset(found[0]))


@app.post("/datasets/{dataset_id}/clean")
def clean(dataset_id: str):
    from datamark.preprocessing.clean import clean_dataframe

    found = list(DATA_DIR.rglob(dataset_id + ".csv"))

    if not found:
        raise HTTPException(404, "not found")

    out = clean_dataframe(read_dataset(found[0]))
    dest = DATA_DIR / "processed" / (dataset_id + "_clean.csv")

    dest.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(dest, index=False)

    return {"saved_to": str(dest)}


@app.get("/tasks")
def tasks(limit: int = 50, domain: str | None = None):
    xs = (
        json.loads(TASKS_FILE.read_text())
        if TASKS_FILE.exists()
        else build_tasks()
    )

    if domain:
        xs = [x for x in xs if x["domain"] == domain]

    return xs[:max(1, min(limit, 500))]


@app.get("/tasks/{task_id}")
def task(task_id: str):
    for x in tasks(500):
        if x["task_id"] == task_id:
            return x

    raise HTTPException(404, "task not found")


@app.post("/tasks/generate")
def gen():
    return {"generated": len(write_tasks())}


@app.post("/tasks/validate")
def validate():
    xs = tasks(500)

    bad = [
        x["task_id"]
        for x in xs
        if not x.get("reference_answer") or not x.get("provenance")
    ]

    return {
        "total": len(xs),
        "valid": len(xs) - len(bad),
        "invalid": bad
    }


@app.post("/evaluate")
def evaluate(req: Eval):
    return evaluate_numeric(
        req.expected,
        req.actual,
        req.abs_tol,
        req.rel_tol
    )


@app.get("/benchmarks")
def benchmarks():
    return {"task_count": len(tasks(500))}


@app.post("/benchmarks/run")
def benchmark():
    return {
        "status": "ready",
        "instruction": "Run scripts/run_benchmark.py for local reproducible demo run."
    }


@app.get("/reports")
def reports():
    p = Path("reports")

    return {
        "files": [x.name for x in p.iterdir() if x.is_file()]
    } if p.exists() else {"files": []}


@app.get("/metrics")
def metrics():
    return {
        "task_count": len(tasks(500)),
        "domain_count": 6
    }
