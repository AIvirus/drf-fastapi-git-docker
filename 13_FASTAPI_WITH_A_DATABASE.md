# Lesson 13 — FastAPI with a Database (SQLModel + SQLite)

**Time:** 40 minutes  |  **You need:** Lesson 12 finished

---

## Goal

By the end of this lesson:

- your tasks will be saved in a **real database** and survive restarts,
- you will use **SQLModel** — database tables written as Python classes,
- you will understand **dependencies** (`Depends`) — FastAPI's way to give each request a database session,
- you will add **search, filters and paging** with SQL queries,
- you will run **automated tests** with **pytest**.

---

## Understand

### FastAPI has no built-in database

Django came with an ORM, migrations and admin. FastAPI doesn't — **you choose**. Common choices:

| Tool | What it is |
|---|---|
| **SQLModel** | Made by FastAPI's author. One class = Pydantic model **and** database table. Easiest to start. ← **we use this** |
| **SQLAlchemy** | The most popular Python ORM (SQLModel is built on top of it) |
| **Alembic** | Migrations for SQLAlchemy/SQLModel (like `makemigrations` + `migrate`) |

### SQLModel vs the Django ORM

| Django ORM (Day 2) | SQLModel |
|---|---|
| `class Task(models.Model)` | `class Task(SQLModel, table=True)` |
| `title = models.CharField(max_length=100)` | `title: str = Field(max_length=100)` |
| `python manage.py migrate` | `SQLModel.metadata.create_all(engine)` (creates missing tables) |
| `Task.objects.create(...)` | `session.add(task)` + `session.commit()` |
| `Task.objects.get(pk=3)` | `session.get(Task, 3)` |
| `Task.objects.filter(done=False)` | `session.exec(select(Task).where(Task.done == False)).all()` |
| `task.delete()` | `session.delete(task)` + `session.commit()` |

### Engine, session, commit

```text
engine   = the connection settings to the database (created once, when the app starts)
session  = one "conversation" with the database (one per request)
add()    = "I want to save this"   (prepared, not saved yet)
commit() = "save everything now"    (written to the database)
refresh()= "read it back"           (now it has its new id)
```

### Dependencies: `Depends(get_session)`

Every endpoint needs a database session, and it must be **closed** afterwards — even if there is an error. FastAPI's **dependency injection** does this:

```python
def get_session():
    with Session(engine) as session:   # open
        yield session                  # give it to the endpoint
                                       # closed automatically after the response

@app.get("/tasks")
def list_tasks(session: SessionDep):  # FastAPI calls get_session() for you
    ...
```

You write `get_session` once; every endpoint just **asks** for a session in its arguments.

---

## Do it now

> Stop uvicorn (**Ctrl + C**) while you create the files. Terminal must end with `my_fastapi>`.

### Step 1 — `database.py`: the connection

Create **`my_fastapi/database.py`**:

```python
import os

from sqlmodel import Session, SQLModel, create_engine

# SQLite file by default. Lesson 19 (Docker Compose) sets DATABASE_URL to PostgreSQL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# SQLite needs this one extra option when used by a web server; PostgreSQL does not.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    """Create every table that does not exist yet (like a tiny `migrate`)."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency: open one database session per request, then close it."""
    with Session(engine) as session:
        yield session
```

> `os.getenv("DATABASE_URL", "sqlite:///./tasks.db")` = "use the environment variable `DATABASE_URL` if it exists, otherwise a SQLite file called `tasks.db`". Today you use SQLite; in Lesson 19 Docker will give you PostgreSQL **without changing this code**.

### Step 2 — `models.py`: the table and the API models

Create **`my_fastapi/models.py`**:

```python
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now():
    return datetime.now(timezone.utc)


# The fields every task has, with their validation rules.
class TaskBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    priority: int = Field(default=3, ge=1, le=5)  # 1 = low ... 5 = urgent
    done: bool = False


# The TABLE in the database (table=True). Only the server sets id and created_at.
class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)


# What the client SENDS to create a task (no id, no created_at).
class TaskCreate(TaskBase):
    pass


# What the server SENDS BACK (always has id and created_at).
class TaskRead(TaskBase):
    id: int
    created_at: datetime


# What the client sends to CHANGE a task: every field is optional.
class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    priority: int | None = Field(default=None, ge=1, le=5)
    done: bool | None = None
```

Only **`Task`** has `table=True` → only it becomes a database table. The others are normal Pydantic models for input and output — the same idea as Lesson 12, but now they share their fields through `TaskBase` (no copy-paste).

### Step 3 — `main.py`: use the database

Replace **all** of **`my_fastapi/main.py`**:

```python
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Session, col, select

from database import create_db_and_tables, get_session
from models import Task, TaskCreate, TaskRead, TaskUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # runs once, when the server starts
    yield


app = FastAPI(
    title="Study Tasks API",
    description="Day 3 FastAPI lab: a to-do list for your studies.",
    version="1.0.0",
    lifespan=lifespan,
)

# "Give me a database session" — FastAPI calls get_session() for every request.
SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
def read_root():
    return {"message": "Welcome to Study Tasks API!", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(task_in: TaskCreate, session: SessionDep):
    task = Task.model_validate(task_in)
    session.add(task)
    session.commit()
    session.refresh(task)  # reload it: now it has an id and created_at
    return task


@app.get("/tasks", response_model=list[TaskRead], tags=["tasks"])
def list_tasks(
    session: SessionDep,
    done: bool | None = None,
    priority: Annotated[int | None, Query(ge=1, le=5)] = None,
    search: Annotated[str | None, Query(max_length=50)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    statement = select(Task)
    if done is not None:
        statement = statement.where(Task.done == done)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    if search:
        statement = statement.where(col(Task.title).contains(search))
    statement = statement.order_by(col(Task.priority).desc(), col(Task.id)).offset(offset).limit(limit)
    return session.exec(statement).all()


@app.get("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def read_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def update_task(task_id: int, task_in: TaskUpdate, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    changes = task_in.model_dump(exclude_unset=True)
    task.sqlmodel_update(changes)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
```

> We dropped `PUT` to keep the code short — `PATCH` is what most apps use for editing. (Adding PUT back is a "Try it yourself".)

### Step 4 — Run and create some tasks

```bash
uvicorn main:app --reload
```

A new file **`tasks.db`** appears in `my_fastapi` — that's your SQLite database.

In **/docs**, create these tasks with **POST /tasks**:

```json
{"title": "Learn SQLModel", "priority": 5}
```
```json
{"title": "Learn Git", "priority": 4}
```
```json
{"title": "Learn Docker", "description": "Images, containers, Compose", "priority": 4}
```
```json
{"title": "Buy notebook", "priority": 1, "done": true}
```

Each answer now also has `created_at`.

### Step 5 — The data survives a restart

Stop uvicorn (**Ctrl + C**), start it again, and **GET /tasks** — all 4 tasks are still there, sorted by priority (highest first). 🎉

### Step 6 — Try the query parameters

| Request | Returns |
|---|---|
| `GET /tasks?done=false` | 3 open tasks |
| `GET /tasks?priority=4` | Learn Git, Learn Docker |
| `GET /tasks?search=Learn` | the 3 "Learn ..." tasks |
| `GET /tasks?limit=2` | the first 2 |
| `GET /tasks?limit=2&offset=2` | the next 2 (page 2) |
| `GET /tasks?limit=500` | **422** — max is 100 |
| `PATCH /tasks/2` `{"done": true}` | Learn Git is done |
| `DELETE /tasks/4` | **204** |

### Step 7 — Look inside the database file

Open a **second terminal**, activate `.venv`, `cd my_fastapi`, and run:

```bash
python -c "import sqlite3; db = sqlite3.connect('tasks.db'); print(db.execute('SELECT id, title, priority, done FROM task').fetchall())"
```

```text
[(1, 'Learn SQLModel', 5, 0), (2, 'Learn Git', 4, 1), (3, 'Learn Docker', 4, 0)]
```

SQLModel created a table called **`task`** and stored your rows. (`done` is `0`/`1` — SQLite has no real true/false type.)

### Step 8 — Automated tests with pytest

Create **`my_fastapi/test_main.py`**:

```python
"""Run with:  pytest -v
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


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_read_task(client):
    response = client.post("/tasks", json={"title": "Learn FastAPI", "priority": 5})
    assert response.status_code == 201
    task = response.json()
    assert task["id"] == 1
    assert task["done"] is False

    response = client.get(f"/tasks/{task['id']}")
    assert response.json()["title"] == "Learn FastAPI"


def test_validation_errors_return_422(client):
    assert client.post("/tasks", json={"title": "ab"}).status_code == 422
    assert client.post("/tasks", json={"title": "Valid", "priority": 9}).status_code == 422


def test_partial_update(client):
    task_id = client.post("/tasks", json={"title": "Write README"}).json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert response.json()["done"] is True
    assert response.json()["title"] == "Write README"


def test_delete_then_404(client):
    task_id = client.post("/tasks", json={"title": "Temporary task"}).json()["id"]
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404
```

Run:

```bash
pytest -v
```

```text
test_main.py::test_health PASSED
test_main.py::test_create_and_read_task PASSED
test_main.py::test_validation_errors_return_422 PASSED
test_main.py::test_partial_update PASSED
test_main.py::test_delete_then_404 PASSED

====================== 5 passed in 0.9s ======================
```

---

## Check

- [ ] `tasks.db` exists, and tasks survive a server restart.
- [ ] Every response has `id` and `created_at`.
- [ ] `?done=`, `?priority=`, `?search=`, `?limit=` and `?offset=` work; `limit=500` → **422**.
- [ ] PATCH and DELETE work; a missing task → **404**.
- [ ] `pytest -v` → **5 passed**.

---

## What just happened?

### One request, from start to end

```text
POST /tasks  {"title": "Learn SQLModel", "priority": 5}
  │
  ├─ Pydantic checks the body against TaskCreate          (bad → 422)
  ├─ FastAPI calls get_session() → a new Session          (Depends)
  ├─ create_task(task_in, session):
  │     Task.model_validate(task_in)  → a Task table object (id=None)
  │     session.add(task)             → prepared
  │     session.commit()              → INSERT INTO task ... (saved!)
  │     session.refresh(task)         → read back: id=1, created_at=...
  ├─ response_model=TaskRead filters the output → JSON, status 201
  └─ the session is closed (the `with` block in get_session ends)
```

### The `select()` query builder

```python
select(Task).where(Task.done == False).order_by(col(Task.priority).desc()).offset(0).limit(20)
```

becomes this SQL:

```sql
SELECT * FROM task WHERE done = 0 ORDER BY priority DESC LIMIT 20 OFFSET 0;
```

`col(...)` just tells VS Code "this is a database column", so `.desc()` and `.contains()` autocomplete without warnings.

### Why the tests didn't touch `tasks.db`

`app.dependency_overrides[get_session] = get_test_session` says: "whenever an endpoint asks for `get_session`, give it **this** one instead". The test version uses an **in-memory** database (`sqlite://`) that disappears after each test. Same idea as Django's temporary test database. This is one of the best features of dependencies: easy to **swap** for tests.

### `create_all` is not a full migration tool

`create_all()` creates tables that **don't exist yet**. It does **not** change an existing table. If you add a field to `Task` later, the old `tasks.db` won't get the new column. For learning, just delete `tasks.db` and restart. Real projects use **Alembic** migrations (like Django's `makemigrations` / `migrate`).

---

## Try it yourself

1. Add a `PUT /tasks/{task_id}` endpoint that replaces a task (use `TaskCreate` as input and `task.sqlmodel_update(task_in.model_dump())`).
2. Add `GET /tasks/stats` → `{"total": 4, "done": 1, "open": 3}`. (Remember: above `/tasks/{task_id}`!) Write a test for it.
3. Add a `due_date: date | None = None` field to `TaskBase` (`from datetime import date`). Stop the server, **delete `tasks.db`**, start again. Create a task with `"due_date": "2026-12-31"`. Try an invalid date like `"2026-13-45"`.
4. Run the finished lab's tests too: `cd ../fastapi_lab` then `pytest -v` (8 tests).

---

## If it does not work

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'sqlmodel'` | `.venv` not active, or `pip install -r requirements.txt` not done (run it in `Day-03`). |
| `ModuleNotFoundError: No module named 'database'` | Run uvicorn/pytest **inside `my_fastapi`**, where `database.py` is. |
| `sqlite3.OperationalError: no such table: task` | The `lifespan=lifespan` argument is missing in `FastAPI(...)`, so `create_all` never ran. |
| `sqlite3.OperationalError: table task has no column named ...` | You changed the model after the table was created. Stop the server, delete `tasks.db`, start again. |
| `ProgrammingError: SQLite objects created in a thread can only be used in that same thread` | `connect_args={"check_same_thread": False}` is missing in `database.py`. |
| pytest: `fixture 'client' not found` | The `@pytest.fixture` function must be called `client` and be in the same file (or in `conftest.py`). |
| pytest: `ERROR: file or directory not found` / `no tests ran` | The file must be called `test_*.py` and test functions must start with `test_`. |

Compare with: [fastapi_lab/main.py](fastapi_lab/main.py), [fastapi_lab/models.py](fastapi_lab/models.py), [fastapi_lab/database.py](fastapi_lab/database.py), [fastapi_lab/test_main.py](fastapi_lab/test_main.py).

---

**🎉 The first half of Day 3 is done!** You built two APIs with two different frameworks.

In the second half you will put **`my_fastapi`** on **GitHub** and into **Docker**.

**Next:** [14_GIT_BASICS.md](14_GIT_BASICS.md)
