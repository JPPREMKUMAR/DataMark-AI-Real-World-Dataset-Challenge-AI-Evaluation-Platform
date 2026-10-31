import pandas as pd
def profile_dataframe(df):
    n,m=df.shape
    missing=df.isna().sum()
    completeness=1-float(missing.sum()/max(n*m,1))
    uniqueness=1-float(df.duplicated().sum()/max(n,1))
    informative=sum(df[c].nunique(dropna=True)>1 for c in df.columns)/max(m,1)
    return {"rows":n,"columns":m,"column_types":{c:str(t) for c,t in df.dtypes.items()},
      "missing_values":{c:int(v) for c,v in missing.items()},
      "missing_percent":{c:round(float(df[c].isna().mean()*100),2) for c in df.columns},
      "duplicate_rows":int(df.duplicated().sum()),
      "data_quality_score":round(100*(.6*completeness+.25*uniqueness+.15*informative),2),
      "numeric_summary":df.describe().to_dict() if len(df.select_dtypes("number").columns) else {}}
