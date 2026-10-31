import sqlite3,json
from pathlib import Path
from uuid import uuid4
from datetime import datetime,timezone
class BenchmarkStore:
 def __init__(self,path="datamark.db"):
  self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
  with sqlite3.connect(self.path) as c:
   c.execute("CREATE TABLE IF NOT EXISTS runs(run_id TEXT PRIMARY KEY,task_id TEXT,dataset_version TEXT,created_at TEXT,score REAL,passed INTEGER,payload TEXT)")
 def record(self,task_id,dataset_version,result):
  rid=str(uuid4())
  with sqlite3.connect(self.path) as c:
   c.execute("INSERT INTO runs VALUES(?,?,?,?,?,?,?)",(rid,task_id,dataset_version,datetime.now(timezone.utc).isoformat(),float(result.get("score",0)),int(bool(result.get("passed"))),json.dumps(result)))
  return rid
