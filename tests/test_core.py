import pandas as pd,pytest
from datamark.profiling.profile import profile_dataframe
from datamark.preprocessing.clean import clean_dataframe
from datamark.evaluation.evaluator import evaluate_numeric,evaluate_json,weighted_score
from datamark.analytics.statistics import descriptive,confidence_interval_mean
from datamark.solvers.reference import ecommerce_revenue,month_over_month
from datamark.generators.tasks import build_tasks
from datamark.evaluation.sandbox import execute_python_submission
def test_profile():
 p=profile_dataframe(pd.DataFrame({"a":[1,2,None],"b":["a","b","c"]})); assert p["rows"]==3 and p["missing_values"]["a"]==1
def test_clean():
 x=clean_dataframe(pd.DataFrame({"First Name":["A","A"],"n":[1,1]})); assert len(x)==1 and "first_name" in x
def test_eval():
 assert evaluate_numeric(10,10.001)["passed"]; assert not evaluate_numeric(10,12)["passed"]; assert evaluate_json({"x":1},{"x":1})["passed"]
def test_weights():
 assert weighted_score({"a":1,"b":0},{"a":.75,"b":.25})==.75
 with pytest.raises(ValueError): weighted_score({}, {})
def test_statistics():
 assert descriptive([1,2,3])["mean"]==2
 ci=confidence_interval_mean([1,2,3,4]); assert ci["lower"]<ci["mean"]<ci["upper"]
 with pytest.raises(ValueError): descriptive([])
def test_reference():
 df=pd.DataFrame({"quantity":[2,1],"unit_price":[10,5],"discount_rate":[0,.2]})
 assert ecommerce_revenue(df)==24 and month_over_month(pd.Series([100,110]))==10
def test_tasks():
 t=build_tasks(); assert len(t)==150 and len({x["task_id"] for x in t})==150
def test_sandbox_fails_closed():
 assert execute_python_submission("print(1)")["status"]=="not_executed"
