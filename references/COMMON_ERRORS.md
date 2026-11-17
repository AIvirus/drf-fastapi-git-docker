# Common Errors and How to Fix Them — Day 3

**How to read an error:** start with the **last line** of the red text. It names the problem. Then look a few lines up for the **file name and line number**. For an API, look at the **status code** first ([HTTP_STATUS_CODES.md](HTTP_STATUS_CODES.md)). Fix **one** thing, then try again.

**Never** "fix" an error by turning off security (permissions, CSRF, authentication) or by committing secrets.

---

## Setup

| Error | Cause | Fix |
|---|---|---|
| `running scripts is disabled on this system` | PowerShell blocks the activate script | Use Command Prompt + `.venv\Scripts\activate.bat`, or once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `No module named rest_framework` / `fastapi` / `sqlmodel` | `.venv` not active or packages not installed | Activate `.venv`; `pip install -r requirements.txt` from `Day-03` |
| `Could not open requirements file` | Wrong folder | `cd` to `Day-03` |
| `git` / `docker` / `uvicorn` not recognized | Not installed, or old terminal | Install; **close and reopen VS Code**; for uvicorn activate `.venv` |
| `address already in use` / `port is already allocated` | Port 8000 busy (Django, uvicorn or a container) | Stop the other one (`Ctrl + C`, `docker ps` → `docker rm -f NAME`) or use another port |

## Django REST Framework

| Error / symptom | Cause | Fix |
|---|---|---|
| `TemplateDoesNotExist: rest_framework/api.html` | `rest_framework` missing in `INSTALLED_APPS` | Add `"rest_framework"` |
| `.accepted_renderer not set on Response` | Missing `@api_view` | Put `@api_view([...])` above the function |
| `405 Method Not Allowed` | Method not in `@api_view([...])` / view doesn't support it | Add the method, or use the right URL (list vs detail) |
| `NOT NULL constraint failed: ...author_id` / `Cannot assign AnonymousUser` | Saved without an author / not logged in | `perform_create` with `serializer.save(author=self.request.user)` + permission `IsAuthenticatedOrReadOnly` |
| `Field name 'x' is not valid for model` | Typo in `fields` | Check the model |
| `Relational field must provide a queryset argument` | `PrimaryKeyRelatedField` without `queryset` | Add `queryset=Category.objects.all()` or `read_only=True` |
| `basename argument not specified` | ViewSet has `get_queryset()` but no `queryset` | `router.register("articles", ArticleViewSet, basename="article")` |
| `no such table: authtoken_token` | `authtoken` app not migrated | Add `"rest_framework.authtoken"`, run `migrate` |
| `401 Authentication credentials were not provided.` | No/wrong `Authorization` header | `Token <key>` or `Bearer <access>` — check spelling and the space |
| `401 Invalid token.` | Token deleted / mistyped | Get a new token |
| `401 Token is invalid or expired` (`token_not_valid`) | JWT expired, wrong type (refresh used as access) or changed | Refresh it (`/api/auth/jwt/refresh/`) or log in again |
| `403 You do not have permission` | Logged in, but a permission class says no | That's correct behaviour — or check your permission logic |
| `403 CSRF Failed` (Postman) | Postman sends a session cookie | Use a token header; delete cookies in Postman |
| `400 {"title": ["..."]}` | Validation failed | Read the message — fix the data you send |
| `404 No Article matches the given query.` | Wrong id, or not in `get_queryset()` (e.g. someone else's draft) | Correct id / correct user |
| List not paginated | `PAGE_SIZE` outside `REST_FRAMEWORK` | Put it inside the dict |
| `InsecureKeyLengthWarning` | `SECRET_KEY` < 32 characters | Generate a proper key |

## FastAPI

| Error / symptom | Cause | Fix |
|---|---|---|
| `Error loading ASGI app. Could not import module "main"` | Wrong folder or file name | `cd my_fastapi`; file must be `main.py` |
| `Attribute "app" not found in module "main"` | Variable not named `app` | `app = FastAPI()` |
| `422` with `"loc": ["path", ...]` | Path value has wrong type/rule | e.g. `/tasks/abc` — send an integer |
| `422` with `"loc": ["query", ...]` | Query value wrong | e.g. `limit=500` > max 100 |
| `422` with `"loc": ["body", ...]` / `"Field required"` | Body missing/invalid | Postman: Body → raw → **JSON**; check required fields |
| `422 JSON decode error` | Invalid JSON | Double quotes, no trailing commas, `true/false/null` |
| `/tasks/stats` → 422 "unable to parse string as an integer" | Route order | Define `/tasks/stats` **above** `/tasks/{task_id}` |
| `UnboundLocalError: next_id` | Missing `global next_id` | Add it in `create_task` |
| `no such table: task` | `create_all` didn't run | `lifespan=lifespan` in `FastAPI(...)` |
| `table task has no column named ...` | Model changed after table creation | Delete `tasks.db` (learning only) and restart |
| `SQLite objects created in a thread...` | Missing SQLite option | `connect_args={"check_same_thread": False}` |
| pytest `no tests ran` | Wrong names | File `test_*.py`, functions `test_*` |

## Git and GitHub

| Error | Cause | Fix |
|---|---|---|
| `fatal: not a git repository` | Wrong folder / no `git init` | `cd my_fastapi` |
| `Author identity unknown` | Name/email not set | `git config --global user.name/user.email` |
| `nothing added to commit` | Forgot `git add` | `git add FILE` |
| A strange editor opened (Vim) | `git commit` without `-m` | **Esc**, `:q!`, **Enter**; use `-m "..."` |
| `Support for password authentication was removed` | Typed GitHub password | Browser sign-in (Windows), `gh auth login`, or a Personal Access Token |
| `Repository not found` | Wrong URL / wrong account | `git remote -v`; `git remote set-url origin URL` |
| `! [rejected] ... (fetch first)` | GitHub has commits you don't | `git pull`, then `git push` |
| `refusing to merge unrelated histories` | GitHub repo created with a README | `git pull origin main --allow-unrelated-histories` |
| `src refspec main does not match any` | No commits / branch named `master` | Commit first; `git branch -M main` |
| `Your local changes would be overwritten` | Uncommitted changes | Commit or `git stash` first |
| `CONFLICT (content): Merge conflict in FILE` | Same lines changed on both branches | Edit the file, remove `<<<<<<< ======= >>>>>>>`, `git add`, `git commit` (or `git merge --abort`) |
| `.env` / `tasks.db` shows in `git status` | `.gitignore` missing / wrong place / file already tracked | `.gitignore` next to `main.py`; `git rm --cached FILE` |
| **Pushed a secret** | — | **Rotate the secret immediately.** Deleting it in a new commit is not enough. |

## Docker

| Error | Cause | Fix |
|---|---|---|
| `failed to connect to the docker API` / `Cannot connect to the Docker daemon` / `error during connect` | Docker Desktop not running | Start it; wait for **Engine running** |
| `WSL 2 installation is incomplete` / `Virtualization not enabled` | Windows requirements | `wsl --update` (Admin PowerShell); enable virtualization in BIOS |
| `"docker build" requires exactly 1 argument` | Missing `.` | `docker build -t NAME .` |
| `failed to read dockerfile` | File name wrong (`Dockerfile.txt`) | Exactly `Dockerfile`, no extension |
| `ModuleNotFoundError` in container | Package not in `requirements.txt` | Add it, rebuild |
| Container exits immediately | Error at startup | `docker logs NAME` |
| `This site can't be reached` | No `-p`, container stopped, or no `--host 0.0.0.0` | Check `docker ps` and the Dockerfile `CMD` |
| `container name ... already in use` | Old container exists | `docker rm -f NAME` |
| Code change not visible | Old image | Rebuild (`docker build` / `docker compose up --build`) |
| `the input device is not a TTY` | Git Bash on Windows | Use PowerShell, or `winpty docker ...` |
| `cannot access 'C:/Program Files/Git/app'` / volume path ignored | Git Bash rewrites paths starting with `/` | Use PowerShell, or prefix with `MSYS_NO_PATHCONV=1 ` |
| Docker Desktop closes on start: `remove ...\AppData\Local\Docker\run\dockerInference` (or `docker-secrets-engine\engine.sock`): `The file cannot be accessed by the system` | A broken leftover socket file that Windows can't delete | Quit Docker Desktop, then delete it from WSL: `wsl -- rm -f /mnt/c/Users/YOUR-WINDOWS-USER/AppData/Local/Docker/run/dockerInference` (same for the other file), start Docker again |
| `toomanyrequests` | Docker Hub rate limit | Wait, or `docker login` |
| `password authentication failed for user "tasks"` (Compose) | Volume created with an older password | `docker compose down -v` (deletes data) and `up` again |
| `could not translate host name "db"` | Wrong service name / not in same Compose file | Service must be `db`; URL `@db:5432` |
| `yaml: ... did not find expected key` | Indentation | Spaces only, 2 per level, space after `:` and `-` |
| `docker-compose: command not found` | Old syntax | `docker compose` (space) |
| Data gone | `down -v` or no volume | Use a named volume; don't use `-v` unless you mean it |
