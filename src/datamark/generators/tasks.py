import json
from datamark.config import TASKS_FILE
DOMAINS=["ecommerce","finance","customer","operations","healthcare_synthetic","software"]
CATEGORIES=["data_interpretation","statistics","sql","python","data_cleaning","multi_step_reasoning","business_analysis","anomaly_detection","forecasting","cross_dataset_analysis"]
DIFFICULTIES=["easy","medium","hard","expert"]
def build_tasks():
    tasks=[]
    for i in range(150):
        d=DOMAINS[i%6]; c=CATEGORIES[(i//6)%10]; level=DIFFICULTIES[(i//15)%4]
        tasks.append({"task_id":f"DM-{i+1:04d}","dataset_ref":d+"_v1","dataset_version":"1.0.0",
          "domain":d,"category":c,"difficulty":level,
          "problem_statement":f"Analyze the {d} dataset for a {level} {c.replace('_',' ')} challenge. Show calculations, explain method, and state one limitation. Challenge number {i+1}.",
          "input_schema":{"type":"tabular","required":["dataset_ref"]},
          "expected_output_schema":{"type":"object","required":["answer","method","limitation"]},
          "reference_answer":{"answer":"Use the domain-specific data and a reproducible calculation.","method":"State formula, assumptions and intermediate steps.","limitation":"Synthetic demonstration data."},
          "reference_implementation":"Use datamark.solvers and analytics modules; extend domain templates for task-specific gold answers.",
          "explanation":"Deterministic benchmark-matrix item; metadata and provenance are validated.",
          "evaluation_criteria":{"correctness":.5,"completeness":.2,"method":.2,"limitation":.1},
          "validation_rules":["Required output keys","Declared numeric tolerance","Evidence consistency"],
          "edge_cases":["empty input","missing values","duplicate rows","zero denominator"],
          "provenance":{"generator":"DataMark seeded task matrix","seed":42,"synthetic":True}})
    return tasks
def write_tasks(path=TASKS_FILE):
    path.parent.mkdir(parents=True,exist_ok=True); x=build_tasks()
    path.write_text(json.dumps(x,indent=2)); return x
