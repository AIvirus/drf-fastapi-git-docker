import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Session, col, select

from database import create_db_and_tables, get_session
from models import Task, TaskCreate, TaskRead, TaskUpdate

# Lesson 18: read settings from environment variables (with a sensible default).
APP_NAME = os.getenv("APP_NAME", "Study Tasks API")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # runs once, when the server starts
    yield


app = FastAPI(
    title=APP_NAME,
    description="Day 3 FastAPI lab: a to-do list for your studies.",
    version="1.0.0",
    lifespan=lifespan,
)

# "Give me a database session" — FastAPI calls get_session() for every request.
SessionDep = Annotated[Session, Depends(get_session)]


# Lesson 10: the first endpoint
@app.get("/")
def read_root():
    return {"message": f"Welcome to {APP_NAME}!", "docs": "/docs"}


# Lesson 18: Docker and servers use this to check that the app is alive.
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# CRUD (Lessons 12 + 13)
# ---------------------------------------------------------------------------
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
    # Lesson 11: query parameters -> /tasks?done=false&priority=5&search=docker
    statement = select(Task)
    if done is not None:
        statement = statement.where(Task.done == done)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    if search:
        statement = statement.where(col(Task.title).contains(search))
    statement = statement.order_by(col(Task.priority).desc(), col(Task.id)).offset(offset).limit(limit)
    return session.exec(statement).all()


# Lesson 16: added on a feature branch. Must be ABOVE /tasks/{task_id}.
@app.get("/tasks/stats", tags=["tasks"])
def task_stats(session: SessionDep):
    tasks = session.exec(select(Task)).all()
    done = sum(1 for task in tasks if task.done)
    return {"total": len(tasks), "done": done, "open": len(tasks) - done}


@app.get("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def read_task(task_id: int, session: SessionDep):
    # Lesson 11: path parameter -> /tasks/3
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def update_task(task_id: int, task_in: TaskUpdate, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # exclude_unset=True -> only the fields the client actually sent
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
    # 204 No Content -> return nothing
