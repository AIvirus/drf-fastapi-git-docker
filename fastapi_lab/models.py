from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now():
    return datetime.now(timezone.utc)


# Lesson 11 + 13: the fields every task has, with their validation rules.
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
