import pandas as pd
def ecommerce_revenue(orders):
    return round(float((orders.quantity*orders.unit_price*(1-orders.discount_rate)).sum()),2)
def monthly_revenue(orders):
    x=orders.copy(); x["order_date"]=pd.to_datetime(x.order_date)
    x["revenue"]=x.quantity*x.unit_price*(1-x.discount_rate)
    return x.groupby(x.order_date.dt.to_period("M")).revenue.sum().sort_index()
def month_over_month(series):
    if len(series)<2 or series.iloc[-2]==0: return None
    return round(float((series.iloc[-1]/series.iloc[-2]-1)*100),2)
def customer_ltv(orders):
    x=orders.copy(); x["lifetime_value"]=x.quantity*x.unit_price*(1-x.discount_rate)
    return x.groupby("customer_id",as_index=False).agg(lifetime_value=("lifetime_value","sum"),
      order_count=("order_id","nunique")).sort_values("lifetime_value",ascending=False)
def sql_revenue_query():
    return "SELECT product_id, ROUND(SUM(quantity*unit_price*(1-discount_rate)),2) AS revenue FROM orders GROUP BY product_id ORDER BY revenue DESC;"
