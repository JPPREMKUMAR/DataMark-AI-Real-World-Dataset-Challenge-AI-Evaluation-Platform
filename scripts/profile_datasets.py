import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from datamark.config import DATA_DIR,REPORTS_DIR
from datamark.ingestion.reader import read_dataset
from datamark.profiling.profile import profile_dataframe
x={p.stem:profile_dataframe(read_dataset(p)) for p in (DATA_DIR/"raw").glob("*.csv")}
REPORTS_DIR.mkdir(exist_ok=True); (REPORTS_DIR/"dataset_profiles.json").write_text(json.dumps(x,indent=2)); print("Profiled",len(x),"datasets")
