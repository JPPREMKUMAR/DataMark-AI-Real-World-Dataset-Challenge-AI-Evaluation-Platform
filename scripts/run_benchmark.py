import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from datamark.evaluation.evaluator import evaluate_numeric
from datamark.reporting.reports import export_benchmark
r=[{"task_id":"DEMO-001",**evaluate_numeric(100,100)},{"task_id":"DEMO-002",**evaluate_numeric(250,247,abs_tol=5)}]
print(export_benchmark(r))
