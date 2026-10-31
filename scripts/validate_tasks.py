import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from datamark.config import TASKS_FILE
x=json.loads(TASKS_FILE.read_text()); ids=[t["task_id"] for t in x]
required={"task_id","dataset_ref","dataset_version","domain","category","difficulty","problem_statement","input_schema","expected_output_schema","reference_answer","reference_implementation","explanation","evaluation_criteria","validation_rules","edge_cases","provenance"}
assert len(x)>=150 and len(set(ids))==len(x) and all(required<=t.keys() for t in x)
assert len({t["domain"] for t in x})==6
print("VALID:",len(x),"tasks across 6 domains")
