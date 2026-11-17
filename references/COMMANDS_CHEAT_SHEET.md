# Commands Cheat Sheet — Day 3

## Every time you open a new terminal

| Computer | Activate `.venv` (from the `Day-03` folder) |
|---|---|
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

Then go into your project: `cd my_api` (DRF) or `cd my_fastapi` (FastAPI, Git, Docker).

## One-time setup (Lesson 02)

| Command | Run from | What it does |
|---|---|---|
| `python -m venv .venv` | `Day-03` | Create the virtual environment |
| `pip install -r requirements.txt` | `Day-03` | Install DRF, FastAPI, SQLModel, pytest… |
| `git --version` / `docker --version` | anywhere | Check Git / Docker are installed |

## Django REST Framework (run from `my_api`, where `manage.py` is)

| Command | What it does | Lesson |
|---|---|---|
| `django-admin startproject config .` | New project in this folder | 03 |
| `python manage.py startapp NAME` | New app (add to `INSTALLED_APPS`) | 03, 07 |
| `python manage.py makemigrations journal` | Create migration files from models | 04 |
| `python manage.py migrate` | Create/update tables | 03, 04, 07 |
| `python manage.py createsuperuser` | Admin user | 04 |
| `python manage.py runserver` | Start at http://127.0.0.1:8000/ | 03 |
| `python manage.py shell` | Python with Django loaded | 04 |
| `python manage.py test` | Run the tests | 09 |

| URL | What |
|---|---|
| `/api/` | API root (router) |
| `/api-auth/login/` | Log in to the browsable API |
| `/api/auth/token/` | Username + password → simple token |
| `/api/auth/jwt/`, `/api/auth/jwt/refresh/` | JWT pair / new access token |
| `/admin/` | Django admin |

Headers: `Authorization: Token <key>` · `Authorization: Bearer <access>`

## FastAPI (run from `my_fastapi`)

| Command | What it does | Lesson |
|---|---|---|
| `uvicorn main:app --reload` | Start at http://127.0.0.1:8000/ (Ctrl + C to stop) | 10 |
| `uvicorn main:app --reload --port 8001` | Use another port | 10 |
| `fastapi dev main.py` | Same as the first line, nicer output | 10 |
| `pytest -v` | Run the tests | 13 |

| URL | What |
|---|---|
| `/docs` | Swagger UI |
| `/redoc` | ReDoc |
| `/openapi.json` | OpenAPI description |

## Git (run from inside the repository, e.g. `my_fastapi`)

| Command | What it does | Lesson |
|---|---|---|
| `git config --global user.name "Name"` | Set your name (once) | 14 |
| `git config --global user.email "you@example.com"` | Set your email (once) | 14 |
| `git config --global init.defaultBranch main` | First branch is `main` (once) | 14 |
| `git init` | Create a repository here | 14 |
| `git status` | What changed? What is staged? | 14 |
| `git add FILE` / `git add .` | Stage changes | 14 |
| `git commit -m "Message"` | Save a snapshot | 14 |
| `git commit -am "Message"` | Stage all tracked changes + commit | 16 |
| `git diff` / `git diff --staged` | Show unstaged / staged changes | 14 |
| `git log --oneline --graph --all` | History (q to quit) | 14, 16 |
| `git restore FILE` | Throw away unstaged changes ⚠ | 14 |
| `git restore --staged FILE` | Unstage | 14 |
| `git rm --cached FILE` | Stop tracking a file (keep it on disk) | 14 |
| `git remote add origin URL` | Connect to GitHub | 15 |
| `git remote -v` | Show remotes | 15 |
| `git push -u origin main` | First push of a branch | 15 |
| `git push` / `git pull` | Upload / download + merge | 15 |
| `git fetch` | Download without merging | 15 |
| `git clone URL [folder]` | Copy a repository from GitHub | 15 |
| `git branch` | List branches | 16 |
| `git switch -c NAME` | Create + switch to a branch | 16 |
| `git switch NAME` | Switch branch | 16 |
| `git merge NAME` | Merge NAME into the current branch | 16 |
| `git merge --abort` | Give up a conflicted merge | 16 |
| `git branch -d NAME` | Delete a merged branch | 16 |
| `git stash` / `git stash pop` | Put changes aside / bring them back | 16 |

Daily loop: `git switch main` → `git pull` → `git switch -c feature/x` → edit → `git add` → `git commit` → `git push -u origin feature/x` → **pull request** → merge → `git switch main` → `git pull`.

## Docker (any folder; build commands from the folder with the Dockerfile)

| Command | What it does | Lesson |
|---|---|---|
| `docker version` | Client + Server (engine running?) | 17 |
| `docker run IMAGE` | Create + start a container | 17 |
| `docker run -it --rm IMAGE CMD` | Interactive, delete afterwards | 17 |
| `docker run -d -p 8000:8000 --name NAME IMAGE` | Background, port mapping, name | 17, 18 |
| `docker run -e KEY=value` / `--env-file .env` | Environment variables | 17, 18 |
| `docker run -v VOLUME:/path` | Mount a named volume | 18 |
| `docker ps` / `docker ps -a` | Running / all containers | 17 |
| `docker logs [-f] NAME` | Output (follow) | 17 |
| `docker exec -it NAME CMD` | Run a command in a running container | 17 |
| `docker stop` / `start` / `rm -f` NAME | Stop / start / remove | 17 |
| `docker images` / `docker rmi IMAGE` | List / remove images | 17 |
| `docker build -t NAME:TAG .` | Build an image (don't forget the dot) | 18 |
| `docker tag SRC USER/NAME:TAG` | Name an image for Docker Hub | 18 |
| `docker login` / `docker push USER/NAME:TAG` | Upload to Docker Hub | 18 |
| `docker volume ls` | List volumes | 18, 19 |
| `docker system df` | Disk usage | 17 |

## Docker Compose (run from the folder with `compose.yaml`)

| Command | What it does |
|---|---|
| `docker compose up --build` | Build and start everything (logs here; Ctrl + C stops) |
| `docker compose up -d` | Start in the background |
| `docker compose ps` | Status |
| `docker compose logs [-f] [SERVICE]` | Logs |
| `docker compose exec SERVICE CMD` | Command inside a service, e.g. `docker compose exec db psql -U tasks -d tasks` |
| `docker compose down` | Stop + remove containers (keep volumes) |
| `docker compose down -v` | …and delete volumes (data!) ⚠ |
| `docker compose config` | Validate the file |
