from fastapi.testclient import TestClient

from {{ cookiecutter.__package_slug }}.{{ cookiecutter.__package_slug }} import create_app


def test_task_list_and_tasks_endpoints():
    app = create_app()
    client = TestClient(app)

    # create list
    r = client.post("/task-lists/", json={"name": "Inbox"})
    assert r.status_code == 200
    tl = r.json()

    # list lists
    r = client.get("/task-lists/")
    assert r.status_code == 200
    assert any(x["name"] == "Inbox" for x in r.json())

    # create task
    r = client.post("/tasks/", json={"task_list_id": tl["id"], "title": "t1"})
    assert r.status_code == 200
    t = r.json()

    # list by list
    r = client.get(f"/tasks/by-list/{tl['id']}")
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # complete
    r = client.post(f"/tasks/{t['id']}/complete")
    assert r.status_code == 200
    assert r.json()["is_completed"] is True
