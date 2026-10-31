from pathlib import Path
p=Path("reports/sample_metrics.json")
print(p.read_text() if p.exists() else "Run scripts/run_benchmark.py first.")
