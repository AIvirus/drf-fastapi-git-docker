# Lesson 11 — Path & Query Parameters, Request Bodies and Pydantic

**Time:** 35 minutes  |  **You need:** Lesson 10 finished

---

## Goal

By the end of this lesson you will know the **three places** a client can put data, and how FastAPI reads each one:

| Where | Example | FastAPI reads it from… |
|---|---|---|
| **Path** parameter | `/tasks/7` | a `{name}` in the path |
| **Query** parameter | `/tasks?done=false&limit=5` | a function argument that is **not** in the path |
| **Request body** (JSON) | `{"title": "Learn Git"}` | a function argument whose type is a **Pydantic model** |

You will also make FastAPI **validate** everything automatically and control what you **send back** with a **response model**.

---

## Understand

### Type hints do the work

In FastAPI the **type hint** of each function argument tells FastAPI what to expect:

```python
@app.get("/squares/{number}")
def square(number: int):          # "number must be an integer"
    return {"square": number * number}
```

- `/squares/7` → FastAPI converts the text `"7"` into the **integer** `7` for you.
- `/squares/abc` → FastAPI **refuses** it with status **422** and a clear message. Your function is never called.

On Day 2 you had to write `int(request.GET.get("page", 1))` and handle errors yourself. Here, the type hint *is* the validation.

### What is Pydantic?

**Pydantic** is the library FastAPI uses for validation. You describe the shape of your data as a **class**:

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    priority: int = Field(default=3, ge=1, le=5)   # ge = greater or equal, le = less or equal
    done: bool = False
```

| Pydantic | DRF (Lesson 04) | Day 2 forms |
|---|---|---|
| `class TaskCreate(BaseModel)` | `class ArticleSerializer(serializers.ModelSerializer)` | `class ArticleForm(forms.ModelForm)` |
| `title: str = Field(min_length=3)` | `validate_title()` / model `max_length` | `clean_title()` |
| Invalid → **422** | Invalid → **400** | Invalid → form shows errors |

### 422 vs 400

FastAPI uses **422 Unprocessable Content** ("I understood your JSON, but the values are wrong") for validation errors. DRF uses **400 Bad Request**. Both are correct HTTP; frameworks just choose differently.

---

## Do it now

> Keep `uvicorn main:app --reload` running in `my_fastapi`. Every time you save, open http://127.0.0.1:8000/docs and try the new endpoint with **Try it out**.

### Step 1 — Path parameters

Add to **`main.py`**:

```python
@app.get("/squares/{number}")
def square(number: int):
    return {"number": number, "square": number * number}
```

Try:

| URL | Result |
|---|---|
| `/squares/7` | `{"number": 7, "square": 49}` |
| `/squares/abc` | **422** (see below) |

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "number"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "abc"
    }
  ]
}
```

Read it: **where** (`loc`: in the **path**, parameter **number**), **what** (`msg`), **what you sent** (`input`).

### Step 2 — Query parameters

Any argument that is **not** in the path is a **query parameter**. Give it a default value to make it optional:

```python
@app.get("/books")
def list_books(q: str | None = None, limit: int = 10, available: bool = False):
    return {"q": q, "limit": limit, "available": available}
```

| URL | Result |
|---|---|
| `/books` | `{"q": null, "limit": 10, "available": false}` (defaults) |
| `/books?q=python&limit=5` | `{"q": "python", "limit": 5, "available": false}` |
| `/books?available=yes` | `available: true` — FastAPI understands `true`, `1`, `yes`, `on` |
| `/books?limit=ten` | **422** — `loc: ["query", "limit"]` |

`str | None = None` means "a string, or nothing; default nothing" → **optional**.
An argument **without** a default (like `number: int` above) is **required**.

### Step 3 — Extra rules with `Path` and `Query`

```python
from typing import Annotated, Literal

from fastapi import FastAPI, Path, Query
```

(Change the first import line of `main.py` to these two lines.)

```python
@app.get("/students/{roll}")
def student(
    roll: Annotated[int, Path(ge=1, le=60, description="Roll number, 1 to 60")],
    show: Annotated[Literal["short", "full"], Query()] = "short",
):
    return {"roll": roll, "show": show}
```

| URL | Result |
|---|---|
| `/students/5` | `{"roll": 5, "show": "short"}` |
| `/students/5?show=full` | `{"roll": 5, "show": "full"}` |
| `/students/99` | **422** — `"Input should be less than or equal to 60"` |
| `/students/5?show=medium` | **422** — `"Input should be 'short' or 'full'"` |

In `/docs`, `show` appears as a **drop-down** with the two allowed values, and `roll` shows its description. `Annotated[type, rules]` = "this type, plus these extra rules".

### Step 4 — Request body with a Pydantic model

Add at the top of `main.py`:

```python
from pydantic import BaseModel, Field
```

Add the model and an endpoint:

```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    priority: int = Field(default=3, ge=1, le=5)   # 1 = low ... 5 = urgent
    done: bool = False


@app.post("/check-task")
def check_task(task: TaskCreate):
    return {"you_sent": task, "title_upper": task.title.upper()}
```

In `/docs`, open **POST /check-task** → **Try it out**. Swagger already shows an example body built from your model. Try these bodies:

**Good:**
```json
{"title": "Learn Pydantic", "priority": "4"}
```
→ **200**:
```json
{"you_sent": {"title": "Learn Pydantic", "description": null, "priority": 4, "done": false}, "title_upper": "LEARN PYDANTIC"}
```
Notice: `"4"` (text) became `4` (number), and the missing fields got their **defaults**.

**Bad — two problems at once:**
```json
{"title": "ab", "priority": 9}
```
→ **422**, with **both** errors:
```json
{
  "detail": [
    {"type": "string_too_short", "loc": ["body", "title"], "msg": "String should have at least 3 characters", "input": "ab", "ctx": {"min_length": 3}},
    {"type": "less_than_equal", "loc": ["body", "priority"], "msg": "Input should be less than or equal to 5", "input": 9, "ctx": {"le": 5}}
  ]
}
```

**Missing title:** `{}` → **422** `"Field required"`.

Also try it in **Postman**: `POST http://127.0.0.1:8000/check-task`, Body → raw → JSON.

### Step 5 — Response models: control what goes OUT

Sometimes the data you receive must **not** all be sent back — a password, for example. Add:

```python
class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)


class UserPublic(BaseModel):
    username: str


@app.post("/users", response_model=UserPublic, status_code=201)
def create_user(user: UserCreate):
    # (we don't save it anywhere yet — this is only a demo)
    return user
```

POST `{"username": "asha", "password": "super-secret-123"}` → **201**:

```json
{"username": "asha"}
```

The function returned the **whole** user, but `response_model=UserPublic` **filtered** the output: the password was removed. `status_code=201` changed the success code from 200 to **201 Created**.

Look at `/docs` → **Schemas** (bottom of the page): your models `TaskCreate`, `UserCreate`, `UserPublic` are documented automatically.

---

## Check

- [ ] `/squares/7` works and `/squares/abc` gives **422** with `loc: ["path", "number"]`.
- [ ] `/books` uses default values; `/books?limit=ten` gives **422**.
- [ ] `/students/99` and `?show=medium` give **422**.
- [ ] `POST /check-task` accepts good data and fills defaults; bad data gives **422** with all errors.
- [ ] `POST /users` returns **201** and **no password**.

---

## What just happened?

### How FastAPI decides where each argument comes from

```text
@app.post("/students/{roll}")
def f(roll: int,           ← name is in the path            → PATH parameter
      show: str = "short", ← simple type, not in the path   → QUERY parameter
      task: TaskCreate):   ← a Pydantic model               → JSON BODY
```

### What Pydantic did for you

1. **Parsed** the JSON text into Python.
2. **Converted** types where it is safe (`"4"` → `4`).
3. **Checked** every rule (`min_length`, `ge`, `le`, required fields).
4. **Collected all errors** and FastAPI returned them as **422**.
5. Gave your function a ready **object**: `task.title`, `task.priority` — with autocomplete in VS Code.

### Useful `Field` / `Query` / `Path` rules

| Rule | For | Meaning |
|---|---|---|
| `min_length`, `max_length` | text | length limits |
| `pattern=r"^[a-z]+$"` | text | must match a regular expression |
| `gt`, `ge`, `lt`, `le` | numbers | >, ≥, <, ≤ |
| `default=...` | all | value when missing (makes it optional) |
| `description="..."` | all | shown in `/docs` |
| `examples=[...]` | all | example values in `/docs` |

### Input model vs output model

A very common pattern — you'll use it in the next lessons:

| Model | Has | Used for |
|---|---|---|
| `TaskCreate` | title, description, priority, done | what the client **sends** to create |
| `TaskUpdate` | the same, but **all optional** | what the client sends to **change** (PATCH) |
| `Task` / `TaskRead` | everything **+ `id`** (+ `created_at`) | what the server **sends back** |

The client should never choose the `id` — the server does. Same rule as "the client never chooses the author" in DRF.

---

## Try it yourself

1. Make `GET /add?a=5&b=7` return `{"result": 12}`. What happens with `/add?a=5` (no `b`)?
2. Add `tags: list[str] = []` to `TaskCreate`. Send `{"title": "Docker", "tags": ["devops", "day3"]}`. What happens with `"tags": "devops"` (not a list)?
3. Add an email to `UserCreate` with a simple pattern: `email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$")`. Test a good and a bad email.
4. Make `/books` reject `limit` above 50 using `Annotated[int, Query(ge=1, le=50)] = 10`.

---

## If it does not work

| Problem | Fix |
|---|---|
| `NameError: name 'Annotated' is not defined` | `from typing import Annotated, Literal` at the top. |
| `NameError: name 'BaseModel' is not defined` | `from pydantic import BaseModel, Field` at the top. |
| A body field shows up as a **query** parameter in `/docs` | The argument's type must be a **Pydantic model** class (`task: TaskCreate`), not `dict` or `str`. |
| **422** `"Field required"` with `loc: ["body"]` | You sent no body, or Postman sends it as text. Postman: **Body → raw → JSON**. |
| **422** `"JSON decode error"` | Invalid JSON: use **double quotes**, no trailing comma, `true`/`false`/`null` in lowercase. |
| `/students/5` gives 404 | The path in the decorator must be `"/students/{roll}"` with curly braces, and the function argument must be called `roll`. |

Compare with: [fastapi_lab/models.py](fastapi_lab/models.py) (it uses SQLModel, which is Pydantic + database — Lesson 13).

---

**Next:** [12_FASTAPI_CRUD.md](12_FASTAPI_CRUD.md)
