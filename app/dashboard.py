import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import streamlit as st,pandas as pd
from datamark.config import DATA_DIR
from datamark.generators.tasks import build_tasks
from datamark.profiling.profile import profile_dataframe
from datamark.ingestion.reader import read_dataset
from datamark.evaluation.evaluator import evaluate_numeric
st.set_page_config(page_title="DataMark AI",page_icon="📊",layout="wide")
st.title("DataMark AI")
st.caption("Dataset challenges · reproducible analytics · AI answer evaluation")
a,b,c=st.columns(3); a.metric("Benchmark tasks",150); b.metric("Domains",6); c.metric("Mode","Synthetic demo")
st.info("Offline demo mode. Bundled datasets are synthetic.")
tab1,tab2,tab3=st.tabs(["Dataset library","Challenge browser","Evaluate answer"])
with tab1:
 paths=list(DATA_DIR.rglob("*.csv")) if DATA_DIR.exists() else []
 st.write([str(p.relative_to(DATA_DIR)) for p in paths])
 if paths:
  p=st.selectbox("Dataset",paths); df=read_dataset(p); st.dataframe(df.head(30)); st.json(profile_dataframe(df))
 up=st.file_uploader("Upload CSV")
 if up:
  df=pd.read_csv(up); st.dataframe(df.head(50)); st.json(profile_dataframe(df))
with tab2:
 tasks=build_tasks(); dom=st.selectbox("Domain",["all"]+sorted({x["domain"] for x in tasks}))
 for t in [x for x in tasks if dom=="all" or x["domain"]==dom][:30]:
  with st.expander(f"{t['task_id']} · {t['difficulty']} · {t['category']}"): st.write(t["problem_statement"]); st.json(t["expected_output_schema"])
with tab3:
 expected=st.number_input("Expected",value=100.0); actual=st.number_input("Submitted",value=98.0)
 if st.button("Evaluate"): st.json(evaluate_numeric(expected,actual))
