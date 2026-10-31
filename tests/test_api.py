from fastapi.testclient import TestClient
from datamark.api.main import app
c=TestClient(app)
def test_health(): assert c.get("/health").json()["status"]=="ok"
def test_tasks(): assert len(c.get("/tasks?limit=150").json())==150
def test_eval(): assert c.post("/evaluate",json={"expected":2,"actual":2}).json()["passed"]
def test_validation(): assert c.post("/tasks/validate").json()["valid"]==150
