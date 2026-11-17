"""Automated tests for the FastAPI lab.  Run with:  pytest -v

Each test uses a fresh, empty, in-memory SQLite database,
so your real tasks.db is never touched.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from database import get_session
from main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_read_task(client):
    response = client.post("/tasks", json={"title": "Learn FastAPI", "priority": 5})
    assert response.status_code == 201
    task = response.json()
    assert task["id"] == 1
    assert task["done"] is False
    assert "created_at" in task

    response = client.get(f"/tasks/{task['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Learn FastAPI"


def test_validation_errors_return_422(client):
    assert client.post("/tasks", json={"title": "ab"}).status_code == 422          # too short
    assert client.post("/tasks", json={"title": "Valid", "priority": 9}).status_code == 422
    assert client.post("/tasks", json={}).status_code == 422                       # title missing


def test_list_and_filter(client):
    client.post("/tasks", json={"title": "Learn Git", "priority": 2})
    client.post("/tasks", json={"title": "Learn Docker", "priority": 5, "done": True})

    assert len(client.get("/tasks").json()) == 2
    assert len(client.get("/tasks?done=true").json()) == 1
    assert client.get("/tasks?search=Docker").json()[0]["title"] == "Learn Docker"
    # highest priority first
    assert client.get("/tasks").json()[0]["priority"] == 5


def test_partial_update(client):
    task_id = client.post("/tasks", json={"title": "Write README"}).json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True
    assert response.json()["title"] == "Write README"  # unchanged


def test_delete(client):
    task_id = client.post("/tasks", json={"title": "Temporary task"}).json()["id"]
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_stats(client):
    client.post("/tasks", json={"title": "Open task"})
    client.post("/tasks", json={"title": "Finished task", "done": True})
    assert client.get("/tasks/stats").json() == {"total": 2, "done": 1, "open": 1}


def test_missing_task_is_404(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
