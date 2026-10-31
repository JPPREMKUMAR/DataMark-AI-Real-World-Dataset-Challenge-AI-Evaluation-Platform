import numpy as np
from scipy import stats
def descriptive(values):
    x=np.asarray(values,dtype=float); x=x[np.isfinite(x)]
    if not len(x): raise ValueError("finite values required")
    return {"count":int(len(x)),"mean":float(x.mean()),"median":float(np.median(x)),
      "std":float(x.std(ddof=1)) if len(x)>1 else 0.0,"min":float(x.min()),"max":float(x.max())}
def confidence_interval_mean(values,confidence=.95):
    x=np.asarray(values,dtype=float); x=x[np.isfinite(x)]
    if len(x)<2: raise ValueError("at least two values required")
    lo,hi=stats.t.interval(confidence,len(x)-1,loc=x.mean(),scale=stats.sem(x))
    return {"mean":float(x.mean()),"lower":float(lo),"upper":float(hi),"confidence":confidence}
def pearson_correlation(x,y):
    if len(x)!=len(y) or len(x)<2: raise ValueError("equal length >=2 required")
    return float(stats.pearsonr(x,y).statistic)
