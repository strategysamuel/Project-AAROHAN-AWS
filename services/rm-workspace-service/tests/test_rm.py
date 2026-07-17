import pytest
import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rm_workspace_crud_and_intelligence():
    # 1. Fetch default seeded tasks
    tasks_res = client.get("/rm/tasks")
    assert tasks_res.status_code == 200
    assert len(tasks_res.json()) >= 2
    
    # 2. Register a new task
    task_payload = {
        "customer_id": 120,
        "title": "Call Aditya regarding GST delay",
        "description": "GST return was delayed by 5 days.",
        "due_date": (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)).isoformat(),
        "priority": "HIGH"
    }
    create_task = client.post("/rm/tasks", json=task_payload)
    assert create_task.status_code == 200
    assert create_task.json()["title"] == "Call Aditya regarding GST delay"
    
    # 3. Fetch default leads
    leads_res = client.get("/rm/leads")
    assert leads_res.status_code == 200
    assert len(leads_res.json()) >= 2
    
    # 4. Trigger Next Best Actions check
    actions_res = client.get("/rm/actions/120")
    assert actions_res.status_code == 200
    assert len(actions_res.json()) > 0
    assert actions_res.json()[0]["action_code"] in ["TRIGGER_CONSENT_RENEWAL", "SCHEDULE_CREDIT_CALL"]
    
    # 5. Call Chat assistant meeting preparation mock
    chat_res = client.post("/rm/assistant/chat", json={"prompt": "Prepare meeting details for Aditya Garments"})
    assert chat_res.status_code == 200
    assert "Gemini meeting prep brief:" in chat_res.json()["response"]
