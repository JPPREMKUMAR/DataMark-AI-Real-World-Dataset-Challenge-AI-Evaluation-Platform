import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import numpy as np,pandas as pd
from datamark.config import DATA_DIR,SEED
def main():
 r=np.random.default_rng(SEED); n=1200; dates=pd.date_range("2024-01-01",periods=n,freq="D")
 orders=pd.DataFrame({"order_id":range(1,n+1),"customer_id":r.integers(1,251,n),"product_id":r.integers(1,81,n),"order_date":dates,"quantity":r.integers(1,6,n),"unit_price":r.uniform(8,250,n).round(2),"discount_rate":r.choice([0,.05,.1,.15,.2],n)})
 frames={
 "ecommerce_orders":orders,
 "finance_transactions":pd.DataFrame({"transaction_id":range(n),"date":dates,"revenue":(orders.quantity*orders.unit_price*(1-orders.discount_rate)).round(2),"expense":r.uniform(5,180,n).round(2),"account":r.choice(["sales","ops","marketing"],n)}),
 "customer_profiles":pd.DataFrame({"customer_id":range(1,251),"age":r.integers(18,75,250),"region":r.choice(["north","south","east","west"],250),"signup_date":pd.date_range("2022-01-01",periods=250,freq="3D"),"segment":r.choice(["standard","silver","gold"],250)}),
 "operations_shipments":pd.DataFrame({"shipment_id":range(n),"warehouse":r.choice(["BLR","HYD","DEL","MUM"],n),"delivery_days":np.maximum(1,r.normal(3.8,1.4,n)).round(1),"inventory_units":r.integers(0,500,n),"late":r.choice([0,1],n,p=[.86,.14])}),
 "healthcare_appointments_synthetic":pd.DataFrame({"synthetic_record_id":range(600),"appointment_date":pd.date_range("2025-01-01",periods=600,freq="12h"),"department":r.choice(["general","dental","cardiology","pediatrics"],600),"wait_minutes":np.maximum(0,r.normal(32,15,600)).round(1),"appointment_status":r.choice(["completed","cancelled","no_show"],600,p=[.78,.12,.1])}),
 "software_issues":pd.DataFrame({"issue_id":range(800),"created_at":pd.date_range("2024-01-01",periods=800,freq="12h"),"severity":r.choice(["low","medium","high","critical"],800),"resolution_hours":np.maximum(.2,r.lognormal(2.2,.7,800)).round(1),"component":r.choice(["api","frontend","database","infra"],800),"reopened":r.choice([0,1],800,p=[.9,.1])})}
 for name,df in frames.items():
  p=DATA_DIR/"raw"/(name+".csv"); p.parent.mkdir(parents=True,exist_ok=True); df.to_csv(p,index=False)
  domain=name.split("_")[0]; q=Path("datasets")/domain; q.mkdir(parents=True,exist_ok=True); df.to_csv(q/(name+".csv"),index=False)
 print(f"Generated {len(frames)} synthetic datasets.")
if __name__=="__main__": main()
