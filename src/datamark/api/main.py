
import sys
import json
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Make the src directory available for Python imports on Vercel
PROJECT_SRC = Path(__file__).resolve().parents[2]

if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

from datamark.config import DATA_DIR, TASKS_FILE
from datamark.generators.tasks import build_tasks, write_tasks
from datamark.profiling.profile import profile_dataframe
from datamark.ingestion.reader import read_dataset
from datamark.evaluation.evaluator import evaluate_numeric


app = FastAPI(
    title="DataMark AI API",
    description="Dataset Challenge and AI Evaluation Platform",
    version="1.0.0"
)

# Allow the deployed React frontend and local Vite development server
ALLOWED_ORIGINS = [
    "https://datamarkaireal.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class Eval(BaseModel):
    expected: float
    actual: float
    abs_tol: float = Field(0.01, ge=0)
    rel_tol: float = Field(0.0001, ge=0)


# ============================================================
# ROOT - DATAMARK AI LANDING PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <meta name="description"
              content="DataMark AI - Dataset Challenge and AI Evaluation Platform">

        <title>DataMark AI | AI Evaluation Platform</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            html {
                scroll-behavior: smooth;
            }

            body {
                font-family: Inter, Arial, sans-serif;
                background: #080d19;
                color: #f8fafc;
                line-height: 1.6;
            }

            a {
                text-decoration: none;
            }

            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 8%;
                background: rgba(8, 13, 25, 0.95);
                border-bottom: 1px solid #1e293b;
                position: sticky;
                top: 0;
                z-index: 10;
            }

            .logo {
                font-size: 25px;
                font-weight: 800;
                color: #60a5fa;
            }

            .nav-links {
                display: flex;
                gap: 25px;
            }

            .nav-links a {
                color: #cbd5e1;
                font-size: 14px;
                transition: color 0.2s;
            }

            .nav-links a:hover {
                color: #60a5fa;
            }

            .hero {
                text-align: center;
                padding: 105px 20px 85px;
                background:
                    radial-gradient(
                        ellipse at top,
                        #172554 0%,
                        #080d19 65%
                    );
            }

            .tag {
                display: inline-block;
                padding: 7px 17px;
                border: 1px solid #1d4ed8;
                border-radius: 30px;
                background: #172554;
                color: #93c5fd;
                font-size: 13px;
                margin-bottom: 25px;
            }

            h1 {
                font-size: clamp(40px, 7vw, 72px);
                line-height: 1.12;
                font-weight: 850;
                letter-spacing: -2px;
                margin-bottom: 25px;
            }

            h1 span {
                color: #60a5fa;
            }

            .hero-description {
                max-width: 700px;
                margin: auto;
                color: #94a3b8;
                font-size: 17px;
            }

            .hero-buttons {
                margin-top: 35px;
            }

            .btn {
                display: inline-block;
                padding: 13px 25px;
                border-radius: 9px;
                margin: 7px;
                font-weight: 700;
                font-size: 14px;
                transition: 0.2s;
            }

            .btn-primary {
                background: #2563eb;
                color: white;
            }

            .btn-primary:hover {
                background: #1d4ed8;
                transform: translateY(-2px);
            }

            .btn-secondary {
                border: 1px solid #475569;
                color: white;
            }

            .btn-secondary:hover {
                border-color: #60a5fa;
                color: #93c5fd;
            }

            .container {
                max-width: 1150px;
                margin: auto;
                padding: 55px 25px 80px;
            }

            .section-title {
                font-size: 29px;
                margin-bottom: 10px;
            }

            .section-description {
                color: #94a3b8;
                margin-bottom: 25px;
            }

            .stats-grid {
                display: grid;
                grid-template-columns:
                    repeat(auto-fit, minmax(210px, 1fr));
                gap: 18px;
            }

            .card {
                background: #111a2b;
                border: 1px solid #263750;
                border-radius: 14px;
                padding: 25px;
                transition: transform 0.2s, border-color 0.2s;
            }

            .card:hover {
                transform: translateY(-4px);
                border-color: #3b82f6;
            }

            .stat-number {
                font-size: 35px;
                font-weight: 800;
                color: #60a5fa;
            }

            .card h3 {
                margin: 8px 0;
                font-size: 17px;
            }

            .muted {
                color: #94a3b8;
                font-size: 14px;
            }

            .online {
                color: #4ade80;
            }

            .section {
                margin-top: 65px;
            }

            .features-grid {
                display: grid;
                grid-template-columns:
                    repeat(auto-fit, minmax(230px, 1fr));
                gap: 18px;
                margin-top: 25px;
            }

            .feature-icon {
                font-size: 27px;
                margin-bottom: 12px;
            }

            .resources {
                margin-top: 25px;
                display: grid;
                grid-template-columns:
                    repeat(auto-fit, minmax(220px, 1fr));
                gap: 15px;
            }

            .resource-link {
                display: block;
                background: #111a2b;
                border: 1px solid #263750;
                border-radius: 10px;
                padding: 18px;
                color: #93c5fd;
                transition: 0.2s;
            }

            .resource-link:hover {
                border-color: #3b82f6;
                background: #172554;
            }

            .footer {
                border-top: 1px solid #263047;
                padding: 30px 20px;
                text-align: center;
                color: #94a3b8;
                font-size: 13px;
            }

            @media(max-width: 650px) {
                .navbar {
                    padding: 17px 5%;
                    flex-wrap: wrap;
                    gap: 15px;
                }

                .nav-links {
                    gap: 14px;
                }

                .nav-links a {
                    font-size: 12px;
                }

                .hero {
                    padding: 75px 18px;
                }

                .hero-description {
                    font-size: 15px;
                }

                .container {
                    padding: 40px 18px 60px;
                }
            }
        </style>
    </head>

    <body>

        <nav class="navbar">
            <div class="logo">DataMark AI</div>

            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/docs">API Docs</a>
                <a href="/datasets">Datasets</a>
                <a href="/health">Status</a>
            </div>
        </nav>

        <section class="hero">

            <div class="tag">
                AI DATASET CHALLENGE & EVALUATION PLATFORM
            </div>

            <h1>
                Build. Evaluate.<br>
                <span>Benchmark AI.</span>
            </h1>

            <p class="hero-description">
                Explore datasets, generate evaluation tasks,
                validate submissions and benchmark AI performance
                through a unified data evaluation platform.
            </p>

            <div class="hero-buttons">
                <a class="btn btn-primary" href="/docs">
                    Explore API Documentation →
                </a>

                <a class="btn btn-secondary" href="/datasets">
                    Explore Datasets
                </a>
            </div>

        </section>

        <main class="container">

            <section>
                <h2 class="section-title">Platform Overview</h2>

                <p class="section-description">
                    An overview of the currently deployed DataMark AI API.
                </p>

                <div class="stats-grid">

                    <div class="card">
                        <div class="stat-number">06</div>
                        <h3>Datasets</h3>
                        <p class="muted">
                            Six available dataset collections.
                        </p>
                    </div>

                    <div class="card">
                        <div class="stat-number">120K</div>
                        <h3>Data Records</h3>
                        <p class="muted">
                            Synthetic records across six datasets.
                        </p>
                    </div>

                    <div class="card">
                        <div class="stat-number">16</div>
                        <h3>API Operations</h3>
                        <p class="muted">
                            Dataset, task, evaluation and benchmark APIs.
                        </p>
                    </div>

                    <div class="card">
                        <div class="stat-number online">● Online</div>
                        <h3>Backend Status</h3>
                        <p class="muted">
                            FastAPI service deployed on Vercel.
                        </p>
                    </div>

                </div>
            </section>

            <section class="section">

                <h2 class="section-title">Platform Features</h2>

                <p class="section-description">
                    Explore the main capabilities of DataMark AI.
                </p>

                <div class="features-grid">

                    <div class="card">
                        <div class="feature-icon">📊</div>
                        <h3>Dataset Management</h3>
                        <p class="muted">
                            Discover, upload, inspect and profile datasets.
                        </p>
                    </div>

                    <div class="card">
                        <div class="feature-icon">🧠</div>
                        <h3>Task Generation</h3>
                        <p class="muted">
                            Generate structured tasks for evaluation workflows.
                        </p>
                    </div>

                    <div class="card">
                        <div class="feature-icon">⚡</div>
                        <h3>Evaluation Engine</h3>
                        <p class="muted">
                            Evaluate numerical answers using tolerance settings.
                        </p>
                    </div>

                    <div class="card">
                        <div class="feature-icon">📈</div>
                        <h3>Benchmarking</h3>
                        <p class="muted">
                            Access benchmark and reporting endpoints.
                        </p>
                    </div>

                </div>
            </section>

            <section class="section">

                <h2 class="section-title">Developer Resources</h2>

                <p class="section-description">
                    Access the deployed API and available resources.
                </p>

                <div class="resources">

                    <a class="resource-link" href="/docs">
                        <strong>Swagger API Documentation →</strong>
                        <p class="muted">Explore API operations and schemas.</p>
                    </a>

                    <a class="resource-link" href="/datasets">
                        <strong>Dataset Explorer →</strong>
                        <p class="muted">View available dataset collections.</p>
                    </a>

                    <a class="resource-link" href="/health">
                        <strong>Health Check →</strong>
                        <p class="muted">Check backend service response.</p>
                    </a>

                    <a class="resource-link" href="/metrics">
                        <strong>Platform Metrics →</strong>
                        <p class="muted">View task and domain metrics.</p>
                    </a>

                </div>

            </section>

        </main>

        <footer class="footer">
            <strong>DataMark AI</strong>
            <p>Dataset Challenge & AI Evaluation Platform</p>
            <p>Built for dataset exploration and AI evaluation.</p>
        </footer>

    </body>
    </html>
    """


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {"status": "ok"}


# ============================================================
# DATASET MANAGEMENT
# ============================================================

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


# ============================================================
# TASK MANAGEMENT
# ============================================================

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


# ============================================================
# EVALUATION
# ============================================================

@app.post("/evaluate")
def evaluate(req: Eval):
    return evaluate_numeric(
        req.expected,
        req.actual,
        req.abs_tol,
        req.rel_tol
    )


# ============================================================
# BENCHMARKS
# ============================================================

@app.get("/benchmarks")
def benchmarks():
    return {"task_count": len(tasks(500))}


@app.post("/benchmarks/run")
def benchmark():
    return {
        "status": "ready",
        "instruction": "Run scripts/run_benchmark.py for local reproducible demo run."
    }


# ============================================================
# REPORTS
# ============================================================

@app.get("/reports")
def reports():
    p = Path("reports")

    return {
        "files": [x.name for x in p.iterdir() if x.is_file()]
    } if p.exists() else {"files": []}


# ============================================================
# METRICS
# ============================================================

@app.get("/metrics")
def metrics():
    return {
        "task_count": len(tasks(500)),
        "domain_count": 6
    }
