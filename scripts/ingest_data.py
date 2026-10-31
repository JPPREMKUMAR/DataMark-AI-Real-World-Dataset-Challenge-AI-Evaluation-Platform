import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from datamark.config import DATA_DIR
from datamark.ingestion.reader import read_dataset
for p in (DATA_DIR/"raw").glob("*.csv"): print(p.name,read_dataset(p).shape)
