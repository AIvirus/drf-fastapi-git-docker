"""Answer key for Lesson 12: CRUD with a Python dictionary instead of a database.

Run it with:   uvicorn lesson12_in_memory:app --reload
Data disappears every time the server restarts — Lesson 13 fixes that with a database.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Study Tasks API (in memory)")


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    priority: int = Field(default=3, ge=1, le=5)
    done: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    priority: int | None = Field(default=None, ge=1, le=5)
    done: bool | None = None


class Task(TaskCreate):
    id: int


# Our "database": a dictionary {id: Task}
tasks: dict[int, Task] = {}
next_id = 1


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    global next_id
    task = Task(id=next_id, **task_in.model_dump())
    tasks[next_id] = task
    next_id += 1
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks(done: bool | None = None):
    result = list(tasks.values())
    if done is not None:
        result = [task for task in result if task.done == done]
    return result


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.put("/tasks/{task_id}", response_model=Task)
def replace_task(task_id: int, task_in: TaskCreate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = Task(id=task_id, **task_in.model_dump())
    return tasks[task_id]


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_in: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    changes = task_in.model_dump(exclude_unset=True)
    tasks[task_id] = tasks[task_id].model_copy(update=changes)
    return tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
