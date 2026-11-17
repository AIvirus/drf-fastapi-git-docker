# Lesson 19 — Docker Compose: Your API + PostgreSQL Together

**Time:** 35 minutes  |  **You need:** Lesson 18 finished

---

## Goal

By the end of this lesson you will:

- describe a **multi-container** app in one **`compose.yaml`** file,
- run your FastAPI app **and** a **PostgreSQL** database with **one command**,
- understand how containers **find each other by name**,
- keep database data in a **named volume**,
- use `docker compose up / ps / logs / exec / down`.

---

## Understand

### Why Docker Compose?

Real apps have **several parts**: an API, a database, maybe Redis, a worker… Starting each with a long `docker run ... -e ... -p ... -v ...` command is slow and easy to get wrong.

**Docker Compose** lets you write all of that **once** in a YAML file:

```text
                docker compose up
                       │
   ┌───────────────────┴───────────────────┐
   ▼                                       ▼
┌──────────────────────┐   network    ┌──────────────────────┐
│ service "api"         │ ───────────► │ service "db"          │
│ built from Dockerfile │  host "db"   │ image postgres:17     │
│ port 8000 → 8000      │  port 5432   │ volume pgdata         │
└──────────────────────┘              └──────────────────────┘
        ▲
        │ http://localhost:8000
     your browser
```

| `docker run` (Lesson 18) | Docker Compose |
|---|---|
| One container per command | All containers, one command |
| Settings typed every time | Settings saved in `compose.yaml` (and in Git!) |
| You create networks yourself | Compose creates a **network**; services reach each other **by name** |

### YAML in 30 seconds

YAML is a simple format for settings. **Indentation (spaces, never tabs) shows structure**:

```yaml
services:          # a dictionary key
  api:             # 2 spaces in → belongs to "services"
    ports:
      - "8000:8000"  # "-" = an item in a list
```

### Service names are hostnames

Inside the Compose network, the API reaches the database at the hostname **`db`** — the service's name. That's why the connection string will be:

```text
postgresql+psycopg://tasks:PASSWORD@db:5432/tasks
                     └user┘ └pass┘  └host┘└port┘└database┘
```

(Not `localhost`! Inside the `api` container, `localhost` means the **api container itself**.)

---

## Do it now

> Terminal in **`my_fastapi`**. Docker Desktop running. Remove old containers from Lesson 18 if they still exist: `docker rm -f tasks tasks2`.

### Step 1 — Put the database password in `.env`

Open **`my_fastapi/.env`** (from Lesson 18) and add a line, with a password you choose:

```text
APP_NAME=Study Tasks API (from .env)
POSTGRES_PASSWORD=pick-your-own-local-password
```

Compose reads `.env` **automatically** and replaces `${POSTGRES_PASSWORD}` in `compose.yaml` with this value. The password stays out of Git (`.env` is in `.gitignore`).

### Step 2 — Write `compose.yaml`

Create **`my_fastapi/compose.yaml`**:

```yaml
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: tasks
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-change-me-local-only}
      POSTGRES_DB: tasks
    volumes:
      - pgdata:/var/lib/postgresql/data   # keep the data when the container is removed
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tasks -d tasks"]
      interval: 3s
      timeout: 3s
      retries: 10

  api:
    build: .
    ports:
      - "8000:8000"          # your computer's port 8000 -> the container's port 8000
    environment:
      APP_NAME: Study Tasks API (Docker Compose)
      # "db" is the name of the service above. Compose gives each service a hostname.
      DATABASE_URL: postgresql+psycopg://tasks:${POSTGRES_PASSWORD:-change-me-local-only}@db:5432/tasks
    depends_on:
      db:
        condition: service_healthy   # wait until PostgreSQL is ready

volumes:
  pgdata:
```

> `${POSTGRES_PASSWORD:-change-me-local-only}` = "the value from `.env`, or `change-me-local-only` if it isn't set".

Let Compose check your file and show it with the values filled in:

```bash
docker compose config
```

If there's a YAML mistake, it tells you the line. (⚠ This output shows your password — don't share it.)

### Step 3 — Start everything

```bash
docker compose up --build
```

`--build` = build the `api` image from your Dockerfile first. You see the logs of **both** services, each line prefixed with its name:

```text
 ✔ Network my_fastapi_default    Created
 ✔ Volume "my_fastapi_pgdata"    Created
 ✔ Container my_fastapi-db-1     Healthy
 ✔ Container my_fastapi-api-1    Created
db-1   | ... database system is ready to accept connections
api-1  | INFO:     Started server process [1]
api-1  | INFO:     Application startup complete.
api-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Notice the order: `db` became **Healthy** first, **then** `api` started — that's `depends_on: condition: service_healthy`.

### Step 4 — Use the API

Open **http://localhost:8000/** → `{"message": "Welcome to Study Tasks API (Docker Compose)!", ...}`

Open **http://localhost:8000/docs** and create a few tasks:

```json
{"title": "Tasks saved in PostgreSQL", "priority": 5}
```
```json
{"title": "Learn Docker Compose", "priority": 4}
```

The code is **the same** as with SQLite — only `DATABASE_URL` changed. SQLModel created the `task` table in PostgreSQL at startup.

### Step 5 — Look into PostgreSQL

Open a **second terminal** in `my_fastapi` (the first one is busy showing logs):

```bash
docker compose ps
```

```text
NAME               IMAGE              SERVICE   STATUS                   PORTS
my_fastapi-api-1   my_fastapi-api     api       Up 2 minutes             0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
my_fastapi-db-1    postgres:17        db        Up 2 minutes (healthy)   5432/tcp
```

Notice: `db` has **no** port mapping to your laptop — only the `api` container can reach it. Safer!

Run SQL **inside** the `db` container:

```bash
docker compose exec db psql -U tasks -d tasks -c "SELECT id, title, priority, done FROM task;"
```

```text
 id |           title           | priority | done
----+---------------------------+----------+------
  1 | Tasks saved in PostgreSQL |        5 | f
  2 | Learn Docker Compose      |        4 | f
(2 rows)
```

Your API's data, in a real PostgreSQL database. (`\dt` lists tables if you open an interactive session with `docker compose exec db psql -U tasks -d tasks`; `\q` quits.)

See the logs of one service only:

```bash
docker compose logs api
```

### Step 6 — Stop, start again: data survives

In the first terminal press **Ctrl + C** (stops the containers). Then remove them:

```bash
docker compose down
```

```text
 ✔ Container my_fastapi-api-1  Removed
 ✔ Container my_fastapi-db-1   Removed
 ✔ Network my_fastapi_default  Removed
```

The containers are **gone**. Start again — this time in the background with `-d`:

```bash
docker compose up -d
```

**GET http://localhost:8000/tasks** → your tasks are **still there**, because PostgreSQL's files live in the **volume** `pgdata`, not in the container.

```bash
docker volume ls
```

```text
DRIVER    VOLUME NAME
local     my_fastapi_pgdata
local     tasks-data
```

### Step 7 — Clean up completely (when you want to)

```bash
docker compose down -v
```

`-v` also deletes the **volumes** → the database is **empty** next time. Use it only when you really want to throw the data away.

### Step 8 — Commit and push

```bash
git status
```

You should see `compose.yaml` — and **not** `.env`.

```bash
git add compose.yaml
```
```bash
git commit -m "Add Docker Compose with PostgreSQL"
```
```bash
git push
```

Anyone can now clone your repository, create a `.env` with a password, run `docker compose up --build`, and have **your API + PostgreSQL** running in a minute — no Python, no PostgreSQL installation needed. That's the power of containerization.

---

## Check

- [ ] `docker compose up --build` starts `db` (healthy) and then `api`.
- [ ] http://localhost:8000/docs works and tasks are saved in **PostgreSQL** (I saw them with `psql`).
- [ ] After `docker compose down` and `up -d`, my tasks are still there.
- [ ] I know what `down -v` does.
- [ ] `compose.yaml` is on GitHub; `.env` is not.

---

## What just happened?

### Docker Compose commands

| Command | Does |
|---|---|
| `docker compose up` | Create and start all services (logs in this terminal; **Ctrl + C** stops) |
| `docker compose up -d` | Same, in the background |
| `docker compose up --build` | Rebuild images first (after changing your code or Dockerfile!) |
| `docker compose ps` | Status of the services |
| `docker compose logs [-f] [service]` | Logs (follow, one service) |
| `docker compose exec SERVICE CMD` | Run a command in a running service |
| `docker compose stop` / `start` | Stop / start without removing |
| `docker compose down` | Stop and **remove** containers and the network (volumes stay) |
| `docker compose down -v` | …and **delete the volumes** (data gone!) |
| `docker compose config` | Check the file and show it with variables filled in |

### Reading the `compose.yaml`

| Key | Meaning | `docker run` equivalent |
|---|---|---|
| `image: postgres:17` | Use a ready-made image | `docker run postgres:17` |
| `build: .` | Build from the Dockerfile in this folder | `docker build .` |
| `ports: - "8000:8000"` | Port mapping host:container | `-p 8000:8000` |
| `environment:` | Environment variables | `-e KEY=value` |
| `volumes: - pgdata:/var/lib/...` | Mount a named volume | `-v pgdata:/var/lib/...` |
| `depends_on` + `condition: service_healthy` | Start order: wait for the healthcheck | — |
| `healthcheck` | A command Docker runs to check the service is ready | `--health-cmd` |
| top-level `volumes: pgdata:` | Declare the named volume | `docker volume create` |

### Same image, same code — different database

| Where | `DATABASE_URL` | Database |
|---|---|---|
| Your laptop (`uvicorn`) | not set → `sqlite:///./tasks.db` | SQLite file |
| Lesson 18 container + volume | `sqlite:////app/data/tasks.db` | SQLite file in a volume |
| Docker Compose | `postgresql+psycopg://tasks:...@db:5432/tasks` | PostgreSQL container |
| A real server (Day 6) | e.g. your Neon URL | Managed PostgreSQL in the cloud |

Not one line of Python changed. This is why we read settings from **environment variables**.

### Development vs production

Compose is perfect for **development** and small deployments: one command gives every developer the same setup. For big production systems, the same images often run on platforms like **Kubernetes**, AWS ECS or Render — you'll see deployment and CI/CD on Day 6.

---

## Try it yourself

1. Add a web UI for the database: add this service to `compose.yaml`, run `docker compose up -d`, open http://localhost:8080 and log in (System: PostgreSQL, Server: `db`, Username: `tasks`, Password: yours, Database: `tasks`):
   ```yaml
     adminer:
       image: adminer
       ports:
         - "8080:8080"
       depends_on:
         - db
   ```
2. Change the welcome text in `main.py`. Run `docker compose up -d` — did it change? Now run `docker compose up -d --build`. Why is `--build` needed?
3. Scale it: remove `ports:` from `api`, then run `docker compose up -d --scale api=2`. What does `docker compose ps` show? (Then put `ports:` back.) Why can't two containers both use host port 8000?
4. **Big challenge:** containerize your **DRF project** (`my_api`) the same way: a `Dockerfile` (CMD `python manage.py runserver 0.0.0.0:8000` for learning, or `gunicorn config.wsgi --bind 0.0.0.0:8000`), a `compose.yaml` with PostgreSQL, and `DATABASE_URL` read with `dj-database-url` like in [drf_lab/config/settings.py](drf_lab/config/settings.py). Don't forget `python manage.py migrate` (hint: `docker compose exec api python manage.py migrate`) and `ALLOWED_HOSTS`.
5. Add a **Docker** section to your README: *"Run with Docker: create `.env` with `POSTGRES_PASSWORD=...`, then `docker compose up --build`"*. Commit and push.

---

## If it does not work

| Error | Fix |
|---|---|
| `no configuration file provided: not found` | You are not in `my_fastapi`, or the file isn't called `compose.yaml` (`docker-compose.yml` also works). |
| `yaml: line 12: did not find expected key` / `mapping values are not allowed` | Indentation problem. Use **spaces only** (2 per level), and a space after every `:` and `-`. Compare with [fastapi_lab/compose.yaml](fastapi_lab/compose.yaml). |
| `docker-compose: command not found` | Use `docker compose` (with a **space**). The old `docker-compose` (with a dash) is the retired version 1. |
| `Bind for 0.0.0.0:8000 failed: port is already allocated` | A container from Lesson 18 (`docker rm -f tasks tasks2`) or your `uvicorn` still uses 8000. |
| api: `password authentication failed for user "tasks"` | The volume was created earlier with a **different** password (PostgreSQL only sets the password the first time). `docker compose down -v` (deletes the data!) and `up` again. |
| api: `could not translate host name "db"` / `Connection refused` | The service must be called `db`, and `DATABASE_URL` must use `@db:5432`. `depends_on` with `service_healthy` makes the api wait. |
| api: `ModuleNotFoundError: No module named 'psycopg'` | `psycopg[binary]` is missing from `requirements.txt`. Add it, then `docker compose up --build`. |
| Code changes don't show up | Use `docker compose up -d --build`. |
| Data is gone after restart | You used `down -v`, or the `volumes:` lines are missing. |

Compare with: [fastapi_lab/compose.yaml](fastapi_lab/compose.yaml), [fastapi_lab/README.md](fastapi_lab/README.md).

---

**Next:** [20_FINAL_CHECKLIST_AND_WHATS_NEXT.md](20_FINAL_CHECKLIST_AND_WHATS_NEXT.md)
