from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[2]
DATA_DIR=Path(os.getenv("DATAMARK_DATA_DIR",ROOT/"data"))
TASKS_FILE=ROOT/"benchmarks"/"tasks.json"
REPORTS_DIR=ROOT/"reports"
SEED=int(os.getenv("DATAMARK_RANDOM_SEED","42"))
