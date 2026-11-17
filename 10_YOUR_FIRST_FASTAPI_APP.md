# Lesson 10 — Your First FastAPI App

**Time:** 25 minutes  |  **You need:** Lesson 02 finished (Lessons 03–09 recommended)

---

## Goal

By the end of this lesson you will:

- know what **FastAPI** is and **when to choose it instead of Django**,
- create and run a FastAPI app with **uvicorn**,
- see your API's **automatic documentation** (Swagger UI and ReDoc),
- call your endpoints from Swagger UI and Postman.

---

## Understand

### What is FastAPI?

**FastAPI** is a modern Python framework made **only for building APIs**. It is small, very fast, and uses normal Python **type hints** (`name: str`, `age: int`) to:

- **read** data from the URL and the request body,
- **validate** it automatically,
- **convert** it to the right Python types,
- and **write the API documentation for you**.

It's used by Microsoft, Uber, Netflix and many AI companies — most Python AI/ML model servers and AI agent backends are built with FastAPI.

### Django (+ DRF) vs FastAPI

| | Django + DRF | FastAPI |
|---|---|---|
| Type | "Batteries included" full web framework | Small, focused API framework |
| Comes with | ORM, migrations, admin, users, sessions, templates, forms | Routing, validation, docs. You choose the rest. |
| Validation | Serializers | **Pydantic** models (type hints) |
| API docs | Browsable API (docs need an add-on) | **Swagger UI + ReDoc built in** |
| Async (`async def`) | Partly | Built in from the start |
| Speed | Fast enough for most sites | One of the fastest Python frameworks |
| Learning curve | Bigger (many parts) | Smaller to start |
| Database | Django ORM included | Bring your own (SQLModel, SQLAlchemy…) — Lesson 13 |

**When to choose which?**

| Choose **Django + DRF** when… | Choose **FastAPI** when… |
|---|---|
| You need an **admin panel**, user accounts, HTML pages *and* an API | You only need an **API** (no HTML pages) |
| It is a big business app with many models (shop, school, CRM) | It's a **microservice** or serves an **AI/ML model** |
| You want everything decided for you | You want something small and you choose the parts |
| Your team already knows Django | You need very high speed / many waiting connections (async) |

Many companies use **both**: Django for the main product and admin, FastAPI for small fast services (for example the AI service). More: [references/DJANGO_VS_FASTAPI.md](references/DJANGO_VS_FASTAPI.md).

### What is uvicorn?

FastAPI is the **app** (your code). It needs a **server program** to receive HTTP requests and pass them to your app. That server is **uvicorn** — like `manage.py runserver` in Django.

```text
Postman / browser ──HTTP──► uvicorn (server) ──► FastAPI app (main.py) ──► your function
```

---

## Do it now

> If your Django server is still running, stop it with **Ctrl + C** — both use port **8000**.

### Step 1 — Create the project folder

Make sure the terminal is in **`Day-03`** (not inside `my_api`). If it ends with `my_api>`, type `cd ..` first.

```bash
mkdir my_fastapi
```
```bash
cd my_fastapi
```

> This folder becomes your **Git repository** in Lesson 14 and your **Docker image** in Lesson 18. You'll build everything for the rest of the day here.

### Step 2 — Write the app

In VS Code, create **`my_fastapi/main.py`**:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Study Tasks API",
    description="Day 3 FastAPI lab: a to-do list for your studies.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Study Tasks API!", "docs": "/docs"}


@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI!"}
```

Save.

### Step 3 — Run it

```bash
uvicorn main:app --reload
```

```text
INFO:     Will watch for changes in these directories: ['...\\Day-03\\my_fastapi']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Application startup complete.
```

| Part | Meaning |
|---|---|
| `main` | the file `main.py` |
| `app` | the variable `app = FastAPI()` inside it |
| `--reload` | restart automatically when you save a file (only for development) |

> **Another way:** `fastapi dev main.py` does the same thing with a nicer screen. Both are fine; the lessons use `uvicorn` because Docker uses it too (Lesson 18).

### Step 4 — Call it

- http://127.0.0.1:8000/ → `{"message":"Welcome to Study Tasks API!","docs":"/docs"}`
- http://127.0.0.1:8000/hello → `{"message":"Hello from FastAPI!"}`
- http://127.0.0.1:8000/banana → `{"detail":"Not Found"}` (status **404**)

Notice: FastAPI URLs here have **no slash at the end** (`/hello`, not `/hello/`). Django usually uses a final slash. Both styles are fine — just be consistent.

### Step 5 — The magic: automatic docs

Open **http://127.0.0.1:8000/docs**

This is **Swagger UI**, generated from your code. You wrote **zero** documentation.

1. Click **GET /hello** → **Try it out** → **Execute**.
2. Look at the **Curl** command, the **Request URL**, the **Response body** and the **Code 200**.

Now open **http://127.0.0.1:8000/redoc** — the same documentation in a different, read-only style (**ReDoc**).

And **http://127.0.0.1:8000/openapi.json** — the raw description of your API in the **OpenAPI** standard. Swagger UI and ReDoc are just two viewers for this file. Postman can even **import** it (Postman → Import → paste the URL) to create a collection automatically.

### Step 6 — Add an endpoint and watch the docs update

Add this to the end of `main.py` and save:

```python
@app.get("/about")
def about():
    return {
        "course": "Applied AI and API Integration",
        "day": 3,
        "topics": ["DRF", "FastAPI", "Git", "Docker"],
    }
```

The terminal shows `WatchFiles detected changes in 'main.py'. Reloading...`. Refresh **/docs** — **GET /about** is already there.

---

## Check

- [ ] `uvicorn main:app --reload` runs without errors.
- [ ] `/`, `/hello` and `/about` return JSON.
- [ ] `/docs` shows Swagger UI with all endpoints, and **Try it out → Execute** works.
- [ ] `/redoc` and `/openapi.json` open.

---

## What just happened?

```text
1. GET /hello arrives at uvicorn
2. FastAPI finds the function decorated with @app.get("/hello")
3. It calls hello()  → returns a Python dict
4. FastAPI converts the dict to JSON and sends it with status 200
```

### Compare with Django REST Framework

| | DRF (Lesson 03) | FastAPI |
|---|---|---|
| Files you needed | `settings.py`, project `urls.py`, app `urls.py`, `views.py` | **one file**: `main.py` |
| Connect URL to function | `path("hello/", views.hello)` in `urls.py` | `@app.get("/hello")` right above the function |
| Allow a method | `@api_view(["GET"])` | `@app.get(...)`, `@app.post(...)`, `@app.put(...)`, `@app.patch(...)`, `@app.delete(...)` |
| Return | `Response({...})` | just `return {...}` |
| Run | `python manage.py runserver` | `uvicorn main:app --reload` |
| Docs | Browsable API | Swagger UI `/docs`, ReDoc `/redoc` |

### `def` or `async def`?

You'll often see FastAPI examples with `async def`:

```python
@app.get("/hello")
async def hello():
    return {"message": "Hello"}
```

Simple rule for today: **use normal `def`**. FastAPI runs normal functions in a thread pool, so they don't block each other. Use `async def` only when everything you call inside is also `async` (for example an async HTTP client or async database driver). Mixing them wrongly (calling slow normal code inside `async def`) makes your API **slower**, not faster.

### What is OpenAPI?

**OpenAPI** is a world standard for describing REST APIs in a JSON/YAML file: every URL, method, parameter, request body and response. Because FastAPI creates it for you, many tools can use your API automatically: Swagger UI, Postman, code generators for mobile apps — and **AI agents**, which read OpenAPI descriptions to learn which "tools" they can call.

---

## Try it yourself

1. Add a `GET /time` endpoint that returns the current server time. Hint:
   ```python
   from datetime import datetime

   return {"now": datetime.now().isoformat()}
   ```
2. Add `tags=["general"]` to each decorator, e.g. `@app.get("/hello", tags=["general"])`. How does `/docs` change?
3. Add a **docstring** to a function (a `"""text"""` as its first line). Where does it appear in `/docs`?
4. In Postman, **Import** → **Link** → `http://127.0.0.1:8000/openapi.json`. Postman builds a collection with all your endpoints.

---

## If it does not work

| Error | Fix |
|---|---|
| `uvicorn` is not recognized | `.venv` not active, or packages not installed. Activate it (Lesson 02). Or run `python -m uvicorn main:app --reload`. |
| `Error loading ASGI app. Could not import module "main"` | You are not in the `my_fastapi` folder, or the file isn't called `main.py`. The terminal must end with `my_fastapi>`. |
| `Error loading ASGI app. Attribute "app" not found in module "main"` | The variable must be called exactly `app` (or change the command: `main:my_variable`). |
| `[Errno 10048] ... address already in use` / `[Errno 98]` | Something else (your Django server?) uses port 8000. Stop it, or run `uvicorn main:app --reload --port 8001`. |
| `/docs` is blank | Swagger UI loads its files from the internet (a CDN). Check your internet connection. |
| Changes don't appear | Did you save? Did you start with `--reload`? |

Compare with: [fastapi_lab/main.py](fastapi_lab/main.py) (the finished version — it has more endpoints).

---

**Next:** [11_PARAMETERS_AND_PYDANTIC.md](11_PARAMETERS_AND_PYDANTIC.md)
