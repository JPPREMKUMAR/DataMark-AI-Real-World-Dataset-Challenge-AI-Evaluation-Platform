def benchmark_summary(results):
    if not results: return {"runs":0,"mean_score":0.0,"pass_rate":0.0}
    return {"runs":len(results),"mean_score":round(sum(float(x.get("score",0)) for x in results)/len(results),4),
      "pass_rate":round(sum(bool(x.get("passed")) for x in results)/len(results),4)}
