import json
from pathlib import Path
import pandas as pd
from datamark.metrics.metrics import benchmark_summary
def export_benchmark(results,out_dir="reports"):
 p=Path(out_dir); p.mkdir(parents=True,exist_ok=True); summary=benchmark_summary(results)
 (p/"sample_metrics.json").write_text(json.dumps({"summary":summary,"results":results},indent=2))
 if results: pd.DataFrame(results).to_csv(p/"benchmark_results.csv",index=False)
 (p/"benchmark_results.md").write_text("# Benchmark Results\\n\\n"+str(summary)+"\\n")
 return summary
