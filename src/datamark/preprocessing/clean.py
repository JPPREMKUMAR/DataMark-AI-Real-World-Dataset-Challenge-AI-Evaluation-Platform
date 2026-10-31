import pandas as pd
def clean_dataframe(df,drop_duplicates=True):
    x=df.copy()
    x.columns=[str(c).strip().lower().replace(" ","_") for c in x.columns]
    if drop_duplicates: x=x.drop_duplicates()
    for c in x.select_dtypes("object"): x[c]=x[c].replace(r"^\\s*$",pd.NA,regex=True)
    return x
