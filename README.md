# rest-apis-github-docker-from-zero

A step-by-step, self-learning Day 3 course for beginners who finished Day 2 (Django). Build a **Django REST Framework** API (serializers, ViewSets, routers, permissions, Token + JWT auth, Postman, tests), then a **FastAPI** app (path/query parameters, Pydantic, CRUD, Swagger UI, SQLModel database). In the second half, put your project on **GitHub** (commits, branches, pull requests) and **containerize** it with **Docker** and **Docker Compose** (API + PostgreSQL). Every lesson says what to read, what to run, and what you should see.

## Start here

Open **[00_START_HERE.md](00_START_HERE.md)** and follow the lessons in order (00 to 20).

| Folder | What is inside |
|---|---|
| `00_...` to `20_...` | The lessons. Read, run, check, then go to the next one. |
| `drf_lab/` | Finished Django REST Framework project (answer key, Lessons 03–09) |
| `fastapi_lab/` | Finished FastAPI project + Dockerfile + compose.yaml (answer key, Lessons 10–19) |
| `postman/` | Ready-made Postman collection for the DRF API |
| `practice/` | Workbook questions and answers |
| `references/` | Cheat sheet, common errors, glossary, HTTP status codes, Django vs FastAPI, professional habits |

## Quick setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
source .venv/bin/activate         # macOS / Linux
pip install -r requirements.txt
```

You also need **Postman**, **Git** and **Docker Desktop** — Lesson 02 shows how to install them.

Private values (secret keys, passwords) go in a `.env` file, which is never uploaded (see `.gitignore`).
