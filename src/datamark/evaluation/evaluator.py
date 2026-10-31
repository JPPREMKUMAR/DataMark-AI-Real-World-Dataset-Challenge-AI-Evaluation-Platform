import math
def evaluate_numeric(expected,actual,abs_tol=.01,rel_tol=.0001):
    try:
        e,a=float(expected),float(actual)
        ok=math.isfinite(e) and math.isfinite(a) and math.isclose(e,a,abs_tol=abs_tol,rel_tol=rel_tol)
        return {"score":1.0 if ok else 0.0,"passed":ok,"absolute_error":abs(e-a),"expected":e,"actual":a}
    except (ValueError,TypeError): return {"score":0.0,"passed":False,"error":"numeric values required"}
def evaluate_json(expected,actual):
    ok=expected==actual
    return {"score":float(ok),"passed":ok}
def weighted_score(criteria,weights):
    if not weights or any(v<0 for v in weights.values()) or sum(weights.values())<=0:
        raise ValueError("non-negative weights with positive total required")
    return round(sum(criteria.get(k,0)*v for k,v in weights.items())/sum(weights.values()),4)
def evaluate_text_contains(terms,answer):
    hits=[x for x in terms if x.casefold() in answer.casefold()]
    return {"score":len(hits)/max(len(terms),1),"passed":len(hits)==len(terms),"matched":hits}
