# Lesson 12 — CRUD Endpoints in FastAPI

**Time:** 35 minutes  |  **You need:** Lesson 11 finished

---

## Goal

By the end of this lesson your **Study Tasks API** will have full CRUD:

| Method | URL | Does | Success |
|---|---|---|---|
| `POST` | `/tasks` | create a task | **201** |
| `GET` | `/tasks` | list tasks (`?done=true/false`) | 200 |
| `GET` | `/tasks/{task_id}` | show one task | 200 |
| `PUT` | `/tasks/{task_id}` | replace a task | 200 |
| `PATCH` | `/tasks/{task_id}` | change some fields | 200 |
| `DELETE` | `/tasks/{task_id}` | delete a task | **204** |

A task that doesn't exist will return **404**. For now the tasks are stored in a Python **dictionary** (in memory). Lesson 13 moves them into a real database.

---

## Understand

### Storing data in memory

```python
tasks: dict[int, Task] = {}   # {1: Task(...), 2: Task(...)}
next_id = 1
```

- **Easy**: no database setup — perfect to learn CRUD.
- **Problem**: when the server restarts (every time you save with `--reload`!) everything is **gone**. That's why real apps use a database (Lesson 13).

### Returning errors: `HTTPException`

In Django you used `get_object_or_404`. In FastAPI you **raise** an exception:

```python
from fastapi import HTTPException

if task_id not in tasks:
    raise HTTPException(status_code=404, detail="Task not found")
```

FastAPI stops the function and sends `{"detail": "Task not found"}` with status **404**.

### Three models (from Lesson 11)

| Model | Fields | Used for |
|---|---|---|
| `TaskCreate` | title, description, priority, done | input for **POST** and **PUT** |
| `TaskUpdate` | the same, **all optional** | input for **PATCH** |
| `Task` | `TaskCreate` **+ `id`** | **output** |

---

## Do it now

### Step 1 — Rewrite `main.py`

Replace **all** of **`my_fastapi/main.py`** with this (the practice endpoints from Lesson 11 are removed to keep the file clean):

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Study Tasks API",
    description="Day 3 FastAPI lab: a to-do list for your studies.",
    version="1.0.0",
)


# ---------- Models ----------
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    priority: int = Field(default=3, ge=1, le=5)  # 1 = low ... 5 = urgent
    done: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    priority: int | None = Field(default=None, ge=1, le=5)
    done: bool | None = None


class Task(TaskCreate):
    id: int


# ---------- Our "database" (in memory) ----------
tasks: dict[int, Task] = {}
next_id = 1


# ---------- General endpoints ----------
@app.get("/")
def read_root():
    return {"message": "Welcome to Study Tasks API!", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- CRUD ----------
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(task_in: TaskCreate):
    global next_id
    task = Task(id=next_id, **task_in.model_dump())
    tasks[next_id] = task
    next_id += 1
    return task


@app.get("/tasks", response_model=list[Task], tags=["tasks"])
def list_tasks(done: bool | None = None):
    result = list(tasks.values())
    if done is not None:
        result = [task for task in result if task.done == done]
    return result


@app.get("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def read_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.put("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def replace_task(task_id: int, task_in: TaskCreate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = Task(id=task_id, **task_in.model_dump())
    return tasks[task_id]


@app.patch("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def update_task(task_id: int, task_in: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    changes = task_in.model_dump(exclude_unset=True)   # only the fields the client sent
    tasks[task_id] = tasks[task_id].model_copy(update=changes)
    return tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
```

Save. Uvicorn reloads.

### Step 2 — Do every CRUD action in Swagger UI

Open **http://127.0.0.1:8000/docs**. The task endpoints are grouped under **tasks** (that's what `tags=["tasks"]` does).

1. **POST /tasks** → Try it out → body:
   ```json
   {"title": "Learn FastAPI CRUD", "priority": 5}
   ```
   → **201** `{"title": "Learn FastAPI CRUD", "description": null, "priority": 5, "done": false, "id": 1}`
2. Create two more:
   ```json
   {"title": "Practise Git commands", "priority": 4}
   ```
   ```json
   {"title": "Read about Docker", "description": "Images vs containers", "priority": 2}
   ```
3. **GET /tasks** → a list of 3 tasks.
4. **PATCH /tasks/{task_id}** with `task_id` = `1`, body `{"done": true}` → only `done` changed; the title is still there.
5. **GET /tasks** with `done` = `true` → only task 1. With `false` → tasks 2 and 3.
6. **PUT /tasks/{task_id}** with `task_id` = `2`, body `{"title": "Practise Git branches"}` → the title changed, and **every other field went back to its default** (`priority` became 3!). That's the difference between PUT and PATCH.
7. **DELETE /tasks/{task_id}** with `3` → **204**, empty body.
8. **GET /tasks/{task_id}** with `3` → **404** `{"detail": "Task not found"}`.
9. **PATCH** task 1 with `{"priority": 10}` → **422** — the `TaskUpdate` rules still apply.

### Step 3 — Do the same in Postman

Create a Postman collection **`Study Tasks (FastAPI)`** with a collection variable `baseUrl` = `http://127.0.0.1:8000` and these requests: `Create task`, `List tasks`, `Get task`, `Update task (PATCH)`, `Delete task`. Add a Post-response script to `Create task` that saves the id (like Lesson 09):

```javascript
pm.test("Status is 201", () => pm.response.to.have.status(201));
pm.collectionVariables.set("taskId", pm.response.json().id);
```

Use `{{baseUrl}}/tasks/{{taskId}}` in the others. Run the collection.

### Step 4 — See the problem with memory

Add an empty line anywhere in `main.py` and **save**. Uvicorn reloads. Now **GET /tasks** →

```json
[]
```

All your tasks are **gone**. Fixing this is the next lesson.

---

## Check

- [ ] POST → **201** with a new `id` each time.
- [ ] GET list, GET one, `?done=` filter work.
- [ ] PATCH changes only what you send; PUT replaces everything.
- [ ] DELETE → **204**; GET of a deleted task → **404**.
- [ ] Invalid data → **422**.
- [ ] My Postman collection runs.

---

## What just happened?

### The CRUD pattern, step by step

| Action | Code | Key idea |
|---|---|---|
| Create | `Task(id=next_id, **task_in.model_dump())` | The **server** chooses the id. `model_dump()` turns the model into a dict; `**` spreads it into arguments. |
| List | `list(tasks.values())` + filter | Optional query parameter `done` |
| Read | `tasks[task_id]` | 404 if missing |
| Replace (PUT) | build a **new** `Task` from `TaskCreate` | Missing fields → **defaults** |
| Update (PATCH) | `model_dump(exclude_unset=True)` + `model_copy(update=...)` | Only the fields the client **actually sent** change |
| Delete | `del tasks[task_id]` | Return nothing → **204** |

### `exclude_unset=True` — the PATCH secret

The client sends `{"done": true}`. `TaskUpdate` then contains `title=None, description=None, priority=None, done=True`.

- `task_in.model_dump()` → `{"title": None, "description": None, "priority": None, "done": True}` → would **erase** the title! ✘
- `task_in.model_dump(exclude_unset=True)` → `{"done": True}` → only what the client **sent**. ✔

### Status codes you chose

| Code | Where | How |
|---|---|---|
| 200 | default for every endpoint | nothing to do |
| 201 | POST | `status_code=status.HTTP_201_CREATED` |
| 204 | DELETE | `status_code=status.HTTP_204_NO_CONTENT` |
| 404 | missing task | `raise HTTPException(404, ...)` |
| 422 | bad input | automatic (Pydantic) |

`status.HTTP_201_CREATED` is just the number `201` with a readable name.

### Compare with DRF

In DRF a `ModelViewSet` gave you all of this in **5 lines**, because it knew your Django model and database. FastAPI makes you write each endpoint — more code, but you **see and control** everything. Neither is "better"; they make different trade-offs.

---

## Try it yourself

1. Add a query parameter `min_priority: int = 1` to `GET /tasks` that only returns tasks with `priority >= min_priority`.
2. Add `GET /tasks/stats` that returns `{"total": 3, "done": 1, "open": 2}`.
   ⚠ Put it **above** `@app.get("/tasks/{task_id}")` in the file. Why? Try putting it below and calling `/tasks/stats` — read the error. (FastAPI checks paths **in order**, and `"stats"` is not an integer.)
3. Make `POST /tasks` refuse a **duplicate title** with **409 Conflict**: `raise HTTPException(status_code=409, detail="A task with this title already exists")`.
4. Add `POST /tasks/{task_id}/complete` that sets `done = True` and returns the task.

---

## If it does not work

| Problem | Fix |
|---|---|
| `UnboundLocalError: local variable 'next_id' referenced before assignment` | You forgot `global next_id` as the first line of `create_task`. |
| PATCH erases other fields | Use `model_dump(exclude_unset=True)`. |
| DELETE gives an error about the response body | A 204 response must have **no body** — don't `return` anything from `delete_task`. |
| `/tasks/stats` → **422** "unable to parse string as an integer" | Route order: define `/tasks/stats` **before** `/tasks/{task_id}`. |
| All tasks disappeared | Normal! Memory is cleared on every reload. Lesson 13 fixes it. |
| `TypeError: Task() got multiple values for keyword argument 'id'` | Don't put `id` in `TaskCreate` — only in `Task`. |

Compare with: [fastapi_lab/lesson12_in_memory.py](fastapi_lab/lesson12_in_memory.py).

---

**Next:** [13_FASTAPI_WITH_A_DATABASE.md](13_FASTAPI_WITH_A_DATABASE.md)
