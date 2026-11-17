# `fastapi_lab` — The Finished Study Tasks API (Answer Key for Lessons 10–19)

This folder is the **finished** FastAPI project — what you build yourself in Lessons 10–19 inside `my_fastapi/`.

Use it to **compare** (e.g. `my_fastapi/main.py` ↔ `fastapi_lab/main.py`) or to **preview** the result.

> Learning tip: don't copy this folder into your repository. Type the code in the lessons — that's how it sticks.

---

## Files

| File | Lesson | What it is |
|---|---|---|
| `main.py` | 10–13, 16, 18 | The API: CRUD endpoints, filters, `/health`, `/tasks/stats`, `APP_NAME` from the environment |
| `lesson12_in_memory.py` | 12 | CRUD with a Python dictionary (no database) |
| `models.py` | 11, 13 | SQLModel table `Task` + `TaskCreate`, `TaskRead`, `TaskUpdate` |
| `database.py` | 13 | Engine, `create_db_and_tables()`, `get_session()`; `DATABASE_URL` from the environment |
| `test_main.py` | 13, 16 | 9 pytest tests using an in-memory database |
| `requirements.txt` | 18 | Packages the image installs |
| `Dockerfile`, `.dockerignore` | 18 | Build recipe for the image |
| `compose.yaml` | 19 | API + PostgreSQL |
| `.env.example` | 18, 19 | Copy to `.env` for your own values |

(The small practice endpoints from the Git lessons, like `/version`, are not included.)

---

## Option 1 — Run with Python (Lessons 10–13)

From the `Day-03` folder, with `.venv` active:

```bash
cd fastapi_lab
```
```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs. A `tasks.db` SQLite file is created here.

The in-memory version from Lesson 12:

```bash
uvicorn lesson12_in_memory:app --reload
```

Run the tests:

```bash
pytest -v
```

`9 passed`

## Option 2 — Run with Docker (Lesson 18)

```bash
docker build -t study-tasks-api:lab .
```
```bash
docker run -d -p 8000:8000 --name tasks-lab -e APP_NAME="Lab Tasks" study-tasks-api:lab
```

Open http://localhost:8000/docs. Stop and remove: `docker rm -f tasks-lab`.

## Option 3 — Run with Docker Compose + PostgreSQL (Lesson 19)

```bash
copy .env.example .env          # Windows   (macOS/Linux: cp .env.example .env)
```

Edit `.env` and choose your own `POSTGRES_PASSWORD`. Then:

```bash
docker compose up --build
```

Open http://localhost:8000/docs. Look into the database:

```bash
docker compose exec db psql -U tasks -d tasks -c "SELECT * FROM task;"
```

Stop: **Ctrl + C**, then `docker compose down` (add `-v` to also delete the database volume).

> Stop `uvicorn` and any other container on port 8000 first.

---

## Endpoints

| Method | URL | Description |
|---|---|---|
| GET | `/` | Welcome message (shows `APP_NAME`) |
| GET | `/health` | `{"status": "ok"}` |
| POST | `/tasks` | Create a task → 201 |
| GET | `/tasks` | List: `?done=`, `?priority=`, `?search=`, `?offset=`, `?limit=` (max 100) |
| GET | `/tasks/stats` | `{"total", "done", "open"}` |
| GET | `/tasks/{id}` | One task → 404 if missing |
| PATCH | `/tasks/{id}` | Change some fields |
| DELETE | `/tasks/{id}` | Delete → 204 |

## Environment variables

| Variable | Default | Used for |
|---|---|---|
| `APP_NAME` | `Study Tasks API` | Title in `/docs` and the welcome message |
| `DATABASE_URL` | `sqlite:///./tasks.db` | Database connection (Compose sets PostgreSQL) |
| `POSTGRES_PASSWORD` | `change-me-local-only` | Only read by `compose.yaml` (from `.env`) |

## Safety

Never commit `.env`. The Compose setup is for development on your own computer.
