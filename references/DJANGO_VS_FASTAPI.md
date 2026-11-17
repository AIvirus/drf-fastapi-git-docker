# Django (+ DRF) vs FastAPI — Which One, When?

Both are excellent, popular, production-ready Python frameworks. They make **different trade-offs**.

## At a glance

| | Django + Django REST Framework | FastAPI |
|---|---|---|
| Philosophy | "Batteries included" — everything decided for you | "Bring what you need" — small core, you choose the rest |
| First release | Django 2005, DRF 2011 | 2018 |
| Built for | Full web apps: HTML pages **and** APIs | APIs |
| ORM / database | Django ORM + migrations built in | None built in → SQLModel / SQLAlchemy + Alembic |
| Admin panel | ✔ Built in | ✘ (third-party options exist) |
| Users, login, sessions, permissions | ✔ Built in | ✘ You build or add them (e.g. OAuth2 + JWT utilities) |
| Validation | Serializers | Pydantic models (type hints) |
| API docs | Browsable API; OpenAPI via add-ons (e.g. drf-spectacular) | Swagger UI + ReDoc + OpenAPI **built in** |
| Async | Partial (improving) | Native from the start |
| Performance | Good | Very high (one of the fastest Python frameworks) |
| Code for a CRUD API | Very little (ModelViewSet + router) | More (write each endpoint) |
| Project structure | Fixed: project, apps, settings, urls | Free: one file or any structure |
| Learning curve | Bigger (many concepts) | Smaller to start; grows as you add parts |
| Server | WSGI (gunicorn) / ASGI | ASGI (uvicorn) |

## Same thing, side by side

**Return JSON**

```python
# DRF
@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello"})

# FastAPI
@app.get("/hello")
def hello():
    return {"message": "Hello"}
```

**Validate input**

```python
# DRF
class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    priority = serializers.IntegerField(min_value=1, max_value=5, default=3)

# FastAPI / Pydantic
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    priority: int = Field(default=3, ge=1, le=5)
```

**Full CRUD for a model**

```python
# DRF: ~6 lines + router.register(...)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# FastAPI: one function per endpoint (see Lessons 12-13), ~60 lines
```

**404**

```python
# DRF / Django
task = get_object_or_404(Task, pk=pk)

# FastAPI
task = session.get(Task, task_id)
if not task:
    raise HTTPException(status_code=404, detail="Task not found")
```

## Decision guide

Choose **Django + DRF** if most of these are true:
- You need an **admin panel** for staff to manage data.
- You need **user accounts, roles, permissions** quickly.
- The app has **many related models** (shop, school, hospital, CRM).
- You need **HTML pages and an API** in one project.
- The team already knows Django.

Choose **FastAPI** if most of these are true:
- You only need an **API** (no HTML pages, no admin).
- It's a **microservice**, or it **serves an AI/ML model** or an **AI agent's tools**.
- You need **high performance** or many concurrent/waiting connections (async, websockets, streaming).
- You want **automatic, always-correct API docs** for other teams or AI tools.
- You want a small codebase and to choose your own parts.

**Both** is common: Django for the main product, users and admin; FastAPI for a fast separate service (e.g. the AI recommendation engine). They talk to each other over HTTP — that's *API integration*.

## How this maps to the coming days

| Project | Likely fit |
|---|---|
| Day 4 — Blog Discovery & Recommendation | Django + DRF for articles, authors, categories, users, admin; a FastAPI service could serve recommendations |
| Day 5 — AI WarRoom | FastAPI is a natural fit for AI/LLM endpoints and agent tools; Django if you need rich data management and admin |
