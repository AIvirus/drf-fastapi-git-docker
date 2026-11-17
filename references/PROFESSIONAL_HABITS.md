# Professional Habits — APIs, Git and Docker

Small habits that make you look (and work) like someone from a real software team.

## Designing APIs

- **Nouns in URLs, methods as verbs.** `GET /articles/`, `DELETE /articles/7/` — not `/deleteArticle?id=7`.
- **Plural resource names** and a consistent style (all with a final `/` in Django, all without in FastAPI — just be consistent).
- **Correct status codes.** 201 for create, 204 for delete, 4xx for client mistakes. Never answer an error with `200 {"error": ...}`.
- **Validate everything** that comes in. Bad input must give a **4xx**, never a 500.
- **The server decides** ownership and ids (`author`, `id`, `created_at`) — never the client's JSON.
- **Never return secrets** (`password`, tokens of other users). Use `write_only` (DRF) / `response_model` (FastAPI).
- **Paginate lists.** Never return "everything".
- **Version** big APIs when breaking changes are needed: `/api/v1/...`.
- **Document it.** OpenAPI/Swagger, a Postman collection and a README with examples.

## Security

- `SECRET_KEY`, database passwords, API keys → **environment variables / `.env`**, never in code, never in Git, never in a Docker image.
- Short-lived access tokens; refresh tokens kept safe.
- Permissions on the **server**. Hiding a button in the frontend is not security.
- Return **404** (not 403) for objects a user shouldn't even know exist (e.g. other people's drafts).
- `DEBUG = False` on real servers (Day 2, Lesson 17).
- Leaked a secret? **Rotate it immediately** — deleting it from Git is not enough.

## Testing

- Every endpoint: one test for the **happy path**, at least one for **bad input**, one for **permissions**.
- Tests must be **independent** (fresh database each time) and **fast**.
- Run tests **before every commit** and **before every push**. (Day 6 will make GitHub run them automatically.)
- Share a **Postman collection** with frontend developers and testers.

## Git

- `git status` before `git add`; `git diff --staged` before `git commit`.
- **Small commits**, one logical change each.
- **Good messages**: a verb + what (+ why). `Fix 500 when task title is empty`.
- **Never commit**: `.env`, `.venv/`, `__pycache__/`, `*.db`, IDE folders, big generated files. Set up `.gitignore` **before** the first commit.
- **Pull before you start**, push when something is finished.
- **Never work directly on `main`** in a team. Branch → PR → review → merge.
- Branch names: `feature/...`, `fix/...`, `docs/...`, `refactor/...`.
- Don't rewrite history that others already pulled (`push --force` on shared branches).

## Pull requests and reviews

- One PR = one topic. Small PRs get reviewed faster and better.
- A description with **What / Why / How to test**.
- Review others kindly and specifically: *"This returns 200 on delete; should it be 204?"* rather than *"wrong"*.
- Fix review comments with new commits on the same branch — the PR updates itself.

## README

Every repository needs one: what it is, features, tech stack, how to install and run, how to test, endpoints/usage examples, environment variables, (Docker), author/license.

## Docker

- Small, official base images (`python:3.13-slim`); pin versions (`postgres:17`, not just `postgres`).
- Copy `requirements.txt` and install **before** copying code (layer cache).
- A `.dockerignore` from day one.
- Configuration via **environment variables**; one image for all environments.
- One process/service per container; connect services with Compose.
- Data in **volumes**, never only inside a container.
- Don't put secrets in `Dockerfile` (`ENV PASSWORD=...`) — they stay in the image layers.
- Next steps for production images (Day 6): run as a **non-root user**, add a `HEALTHCHECK`, use gunicorn/uvicorn workers, scan images for vulnerabilities.
