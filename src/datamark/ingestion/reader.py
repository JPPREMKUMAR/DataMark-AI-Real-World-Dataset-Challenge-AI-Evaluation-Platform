from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
def read_dataset(path, table=None):
    p=Path(path); ext=p.suffix.lower()
    if ext==".csv": return pd.read_csv(p)
    if ext==".json": return pd.read_json(p)
    if ext in {".xlsx",".xls"}: return pd.read_excel(p)
    if ext==".parquet": return pd.read_parquet(p)
    if ext in {".db",".sqlite"}:
        if not table: raise ValueError("SQLite table name required")
        with create_engine(f"sqlite:///{p}").connect() as c: return pd.read_sql_table(table,c)
    raise ValueError(f"Unsupported format: {ext}")
