# Lesson 18 — Dockerfile: Containerize Your FastAPI App

**Time:** 40 minutes  |  **You need:** Lessons 13 and 17 finished

---

## Goal

By the end of this lesson you will:

- write a **Dockerfile** for your `my_fastapi` project,
- **build** your own image with `docker build`,
- **run** your API in a container and open `/docs` in your browser,
- configure the app with **environment variables** (`-e`, `--env-file`),
- keep data with a **volume**,
- understand **layer caching** (why rebuilds are fast),
- *(optional)* **push** your image to **Docker Hub**,
- commit your Docker files to **GitHub**.

---

## Understand

### What is a Dockerfile?

A **Dockerfile** is a **recipe** for an image: a text file with step-by-step instructions.

```text
Dockerfile ──docker build──► Image ──docker run──► Container
 (recipe)                    (cake mix in a box)    (the cake, running)
```

### The instructions you'll use

| Instruction | Meaning | Example |
|---|---|---|
| `FROM` | Start from an existing image | `FROM python:3.13-slim` |
| `ENV` | Set an environment variable inside the image | `ENV PYTHONUNBUFFERED=1` |
| `WORKDIR` | "cd" into this folder (create it if needed) | `WORKDIR /app` |
| `COPY` | Copy files from your project into the image | `COPY requirements.txt .` |
| `RUN` | Run a command **while building** | `RUN pip install -r requirements.txt` |
| `EXPOSE` | Document which port the app uses | `EXPOSE 8000` |
| `CMD` | The command to run **when a container starts** | `CMD ["uvicorn", "main:app", ...]` |

`RUN` happens **once, at build time**. `CMD` happens **every time a container starts**.

### Layers and caching

Every instruction creates a **layer** (like a stack of transparent sheets). When you rebuild, Docker **reuses** every layer whose inputs didn't change. That's why we:

1. copy **`requirements.txt` first** and install packages (slow, rarely changes),
2. copy **our code last** (fast, changes all the time).

Then changing `main.py` only rebuilds the last small layer — the slow `pip install` is reused from cache.

---

## Do it now

> Stop `uvicorn` if it's running (the container will use port 8000). Terminal in **`my_fastapi`**. Docker Desktop running. `git status` should be clean.
>
> **Windows:** use a **PowerShell** (or Command Prompt) terminal for this lesson — Git Bash changes paths like `/app/data` and breaks Steps 6 and 8 (see Lesson 17).

### Step 1 — A requirements file for the image

The image doesn't know about your `.venv` — it needs its own list of packages. Create **`my_fastapi/requirements.txt`**:

```text
fastapi>=0.115,<1
uvicorn[standard]>=0.30,<1
sqlmodel>=0.0.24,<0.1
psycopg[binary]>=3.2,<4
```

(`psycopg` is the PostgreSQL driver — you need it in Lesson 19.)

### Step 2 — Read the app's name from an environment variable

A good app reads its **settings from environment variables**, so the **same image** can run with different settings (your laptop, test server, production). Open **`main.py`**:

1. Add `import os` as the **first** import line.
2. Below the imports, add:
   ```python
   APP_NAME = os.getenv("APP_NAME", "Study Tasks API")
   ```
3. Use it in two places:
   ```python
   app = FastAPI(
       title=APP_NAME,
       description="Day 3 FastAPI lab: a to-do list for your studies.",
       version="1.0.0",
       lifespan=lifespan,
   )
   ```
   ```python
   @app.get("/")
   def read_root():
       return {"message": f"Welcome to {APP_NAME}!", "docs": "/docs"}
   ```

`os.getenv("APP_NAME", "Study Tasks API")` = "the value of `APP_NAME`, or this default if it isn't set". Your `database.py` already does the same with `DATABASE_URL`.

Quick check without Docker: `uvicorn main:app --reload` → http://127.0.0.1:8000/ still says *Welcome to Study Tasks API!*. Stop it again (**Ctrl + C**).

### Step 3 — `.dockerignore`: what must NOT go into the image

Create **`my_fastapi/.dockerignore`**:

```text
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
.git/
.env
*.db
*.sqlite3
.vscode/
```

Like `.gitignore`, but for `COPY . .`. It keeps the image **small** (no `.venv`), **clean** (no local `tasks.db`) and **safe** (no `.env` secrets baked into the image).

### Step 4 — Write the Dockerfile

Create **`my_fastapi/Dockerfile`** (exactly this name: capital **D**, **no** extension):

```dockerfile
# 1. Start from an official, small image that already has Python installed.
FROM python:3.13-slim

# 2. Python settings that are good inside containers:
#    don't write .pyc files, and print logs immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. All the next commands run inside /app (in the image).
WORKDIR /app

# 4. Install packages FIRST. Docker caches this step, so rebuilding after
#    a code change is fast (packages are only re-installed if requirements.txt changes).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Now copy our code (.dockerignore keeps .venv, tasks.db, .env etc. out).
COPY . .

# 6. Document which port the app listens on.
EXPOSE 8000

# 7. The command that runs when a container starts.
#    --host 0.0.0.0 = accept connections from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> VS Code may offer to install the **Docker** extension — say yes; it adds colours and helpful hints.

### Step 5 — Build the image

```bash
docker build -t study-tasks-api:1.0 .
```

| Part | Meaning |
|---|---|
| `-t study-tasks-api:1.0` | **tag** = name `study-tasks-api`, version `1.0` |
| `.` | the **build context**: "use the files in this folder" (don't forget the dot!) |

The first build takes 1–2 minutes (downloading packages). You see each step:

```text
 => [1/5] FROM docker.io/library/python:3.13-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .
 => exporting to image
 => naming to docker.io/library/study-tasks-api:1.0
```

```bash
docker images study-tasks-api
```

```text
IMAGE                 ID             DISK USAGE   CONTENT SIZE   EXTRA
study-tasks-api:1.0   63136469d1d2        288MB         68.5MB
```

(About 290 MB on disk. Older Docker versions show the columns `REPOSITORY  TAG  IMAGE ID  CREATED  SIZE`.)

### Step 6 — Run your API in a container

```bash
docker run -d -p 8000:8000 --name tasks study-tasks-api:1.0
```

Open **http://localhost:8000/docs** — your Swagger UI, served **from inside a Linux container**. 🎉

Create a task with **POST /tasks**, then **GET /tasks**. It works exactly like before.

```bash
docker logs tasks
```

```text
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     172.17.0.1:53422 - "GET /docs HTTP/1.1" 200 OK
INFO:     172.17.0.1:53422 - "POST /tasks HTTP/1.1" 201 Created
```

Look inside the running container:

```bash
docker exec -it tasks ls -la /app
```

You see `main.py`, `models.py`, `database.py`, `Dockerfile`, … and `tasks.db` (created by the app **inside** the container). **No** `.venv`, **no** `.git` — thanks to `.dockerignore`.

### Step 7 — Change settings with environment variables

Run a **second** container from the **same image** with a different name and port:

```bash
docker run -d -p 8001:8000 -e APP_NAME="Asha's Exam Planner" --name tasks2 study-tasks-api:1.0
```

- http://localhost:8000/ → `Welcome to Study Tasks API!`
- http://localhost:8001/ → `Welcome to Asha's Exam Planner!`
- http://localhost:8001/docs → the title changed too.

**Same image, different configuration.** That's the professional pattern: build once, configure per environment.

Many variables? Put them in a file. Create **`my_fastapi/.env`** (it's in `.gitignore` and `.dockerignore`):

```text
APP_NAME=Study Tasks API (from .env)
```

```bash
docker rm -f tasks2
```
```bash
docker run -d -p 8001:8000 --env-file .env --name tasks2 study-tasks-api:1.0
```

http://localhost:8001/ → `Welcome to Study Tasks API (from .env)!`

### Step 8 — The data problem, and volumes

Your tasks are in `/app/tasks.db` **inside** the container. Remove the container:

```bash
docker rm -f tasks
```
```bash
docker run -d -p 8000:8000 --name tasks study-tasks-api:1.0
```

**GET /tasks** → `[]`. The data died with the container!

A **volume** is storage that Docker keeps **outside** the container's life. We tell the app to put its database file in a folder that is a volume:

```bash
docker rm -f tasks
```
```bash
docker run -d -p 8000:8000 --name tasks -v tasks-data:/app/data -e DATABASE_URL=sqlite:////app/data/tasks.db study-tasks-api:1.0
```

| Part | Meaning |
|---|---|
| `-v tasks-data:/app/data` | a volume named `tasks-data`, mounted at `/app/data` in the container |
| `-e DATABASE_URL=sqlite:////app/data/tasks.db` | the app saves its database **in** that folder (4 slashes = absolute path `/app/data/tasks.db`) |

Create two tasks. Then destroy and recreate the container with the **same** command:

```bash
docker rm -f tasks
```
```bash
docker run -d -p 8000:8000 --name tasks -v tasks-data:/app/data -e DATABASE_URL=sqlite:////app/data/tasks.db study-tasks-api:1.0
```

**GET /tasks** → your two tasks are **still there**. 🎉 (`docker volume ls` lists the volume.)

### Step 9 — See layer caching

Change the welcome text in `main.py` (any small change), save, and rebuild:

```bash
docker build -t study-tasks-api:1.1 .
```

```text
 => CACHED [2/5] WORKDIR /app
 => CACHED [3/5] COPY requirements.txt .
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .
```

The slow `pip install` step is **CACHED** — the build takes a second or two. Only the code layer was rebuilt.

### Step 10 — Clean up containers

```bash
docker rm -f tasks tasks2
```

### Step 11 — (Optional) Push your image to Docker Hub

Share your image so any computer can run it with one command.

1. Create a free account at **https://hub.docker.com/signup**.
2. Log in from the terminal:
   ```bash
   docker login
   ```
   (It shows a code and a link — confirm in the browser. Docker Desktop may already be signed in.)
3. Tag the image with **your Docker Hub username**:
   ```bash
   docker tag study-tasks-api:1.1 YOUR-DOCKERHUB-USERNAME/study-tasks-api:1.1
   ```
4. Push:
   ```bash
   docker push YOUR-DOCKERHUB-USERNAME/study-tasks-api:1.1
   ```
5. Open https://hub.docker.com → **Repositories** — your image is there. Anyone can now run:
   ```bash
   docker run -p 8000:8000 YOUR-DOCKERHUB-USERNAME/study-tasks-api:1.1
   ```

> ⚠ Images on a free Docker Hub repository are **public** by default. That's why `.dockerignore` must keep `.env` and other secrets out.

### Step 12 — Save the Docker files in Git

```bash
git status
```

You should see `Dockerfile`, `.dockerignore`, `requirements.txt` and `main.py`. You should **not** see `.env`.

```bash
git add Dockerfile .dockerignore requirements.txt main.py
```
```bash
git commit -m "Add Dockerfile and read APP_NAME from environment"
```
```bash
git push
```

---

## Check

- [ ] `docker build` created `study-tasks-api:1.0`.
- [ ] http://localhost:8000/docs works from the container.
- [ ] Two containers from one image showed **different** `APP_NAME`s.
- [ ] Without a volume, data disappeared; **with** `-v tasks-data:/app/data`, it survived.
- [ ] A rebuild after a code change showed `CACHED` for the `pip install` step.
- [ ] `Dockerfile`, `.dockerignore`, `requirements.txt` are on GitHub; `.env` is **not**.

---

## What just happened?

### From code to running container

```text
my_fastapi/                docker build -t study-tasks-api:1.0 .
├── Dockerfile   ───────►  FROM python:3.13-slim          (layer 1, downloaded)
├── requirements.txt       WORKDIR /app                    (layer 2)
├── main.py                COPY requirements.txt .         (layer 3)
├── models.py              RUN pip install ...             (layer 4, the big one)
├── database.py            COPY . .                        (layer 5, your code)
└── .dockerignore                    │
                                     ▼
                           IMAGE study-tasks-api:1.0
                                     │ docker run -p 8000:8000 -e APP_NAME=...
                                     ▼
                           CONTAINER "tasks": uvicorn main:app --host 0.0.0.0 --port 8000
```

### Why `--host 0.0.0.0`?

By default uvicorn listens on `127.0.0.1` = "only connections from **inside this same machine**". Inside a container, "this machine" is the container itself — so the port mapping from your laptop couldn't reach it. `0.0.0.0` = "accept connections from anywhere", which lets Docker's port mapping in.

### Why no `--reload` in the Dockerfile?

`--reload` watches files for changes — useful while **developing** on your laptop, wasteful and risky in a container that should run the **same** code until you build a new image.

### Configuration through environment variables (the "12-factor" rule)

| ✘ Bad | ✔ Good |
|---|---|
| Password written in `main.py` | `os.getenv("DATABASE_URL")` |
| A different image for test and production | **One** image, different `-e` / `--env-file` |
| `.env` copied into the image | `.env` in `.dockerignore`, given at **run** time |

---

## Try it yourself

1. Run the tests **inside** a container: `docker run --rm study-tasks-api:1.1 python -m pytest -q`. It fails — why? (Hint: is `pytest` in `requirements.txt`? Is `httpx`?) Make it work with a **second** image built from a `Dockerfile.test` (`docker build -f Dockerfile.test -t study-tasks-test .`), or by adding the packages to a separate `requirements-dev.txt`.
2. Add a `HEALTHCHECK` to your Dockerfile:
   ```dockerfile
   HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
   ```
   Rebuild, run, and watch `docker ps` — the STATUS shows `(healthy)` after a few seconds.
3. Use `docker history study-tasks-api:1.1` to see every layer and its size. Which layer is the biggest?
4. Add a **Docker** section to your README: how to build and run the image.

---

## If it does not work

| Error | Fix |
|---|---|
| `failed to read dockerfile: open Dockerfile: no such file or directory` | The file must be called exactly `Dockerfile` (not `Dockerfile.txt`, not `dockerfile.txt`) and be in the folder where you run `docker build`. Windows: turn on **View → File name extensions** to check. |
| `"docker build" requires exactly 1 argument` | You forgot the **dot** at the end: `docker build -t study-tasks-api:1.0 .` |
| `ERROR: Could not find a version that satisfies the requirement ...` | Typo in `requirements.txt`, or no internet during the build. |
| Container stops right away | Run `docker logs tasks` — usually a Python error (typo in `main.py`). Fix it, **rebuild**, run again. |
| `ModuleNotFoundError` inside the container | The package isn't in `requirements.txt`. Your `.venv` doesn't count — the image only has what `requirements.txt` lists. Add it, rebuild. |
| Browser: "This site can't be reached" on localhost:8000 | Is the container running (`docker ps`)? Did you use `-p 8000:8000`? Does `CMD` use `--host 0.0.0.0`? |
| `port is already allocated` | Your `uvicorn --reload` (or another container) still uses 8000. Stop it, or use `-p 8002:8000`. |
| `The container name "/tasks" is already in use` | `docker rm -f tasks`, then run again. |
| I changed code but the container still shows the old version | A container runs the image it was started from. **Rebuild** the image, remove the old container, run a new one. |
| `ls: cannot access 'C:/Program Files/Git/app'` / the volume doesn't keep data | You're in **Git Bash**, which rewrites `/app` paths. Use PowerShell, or prefix the command with `MSYS_NO_PATHCONV=1 `. |
| `docker push`: `denied: requested access to the resource is denied` | Not logged in (`docker login`), or the tag doesn't start with **your** Docker Hub username. |

Compare with: [fastapi_lab/Dockerfile](fastapi_lab/Dockerfile), [fastapi_lab/.dockerignore](fastapi_lab/.dockerignore), [fastapi_lab/requirements.txt](fastapi_lab/requirements.txt), [fastapi_lab/main.py](fastapi_lab/main.py).

---

**Next:** [19_DOCKER_COMPOSE.md](19_DOCKER_COMPOSE.md)
