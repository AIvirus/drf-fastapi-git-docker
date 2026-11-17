# Lesson 17 — Docker Basics: Images, Containers and Docker Hub

**Time:** 35 minutes  |  **You need:** Docker Desktop installed and running (Lesson 02, Part D)

---

## Goal

By the end of this lesson you will:

- explain what **containerization** is and which problem it solves,
- explain **virtual machines vs containers**,
- explain **images**, **containers** and **Docker Hub**,
- run containers from ready-made images (Python, nginx, PostgreSQL),
- understand **port mapping** (`-p 8080:80`) and **environment variables** (`-e`),
- list, stop and remove containers and images.

---

## Understand

### The problem: "It works on my machine!" 🤷

Your FastAPI app works on your laptop. Your friend tries it and gets errors, because:

- they have Python 3.10, you have 3.13,
- they forgot to install `sqlmodel`,
- they're on Mac, you're on Windows,
- the server in the cloud runs Linux with different system libraries…

**Docker's answer:** pack the app **together with everything it needs** (the right Python, the packages, the settings) into one standard box — a **container**. The box runs the same way on every computer that has Docker.

```text
  Shipping before containers:           Shipping with containers:
  sacks, barrels, boxes of every        one standard steel container —
  size → slow, things break             every ship, train and truck can carry it
```

That's exactly where the name comes from.

### Virtual machines vs containers

```text
        VIRTUAL MACHINES                              CONTAINERS
 ┌─────────┐ ┌─────────┐ ┌─────────┐        ┌─────────┐ ┌─────────┐ ┌─────────┐
 │  App A  │ │  App B  │ │  App C  │        │  App A  │ │  App B  │ │  App C  │
 │ Libs    │ │ Libs    │ │ Libs    │        │  Libs   │ │  Libs   │ │  Libs   │
 │ Guest OS│ │ Guest OS│ │ Guest OS│        └─────────┘ └─────────┘ └─────────┘
 │ (whole  │ │ (whole  │ │ (whole  │        ┌─────────────────────────────────────┐
 │ Windows │ │ Linux)  │ │ Linux)  │        │       Docker Engine                  │
 └─────────┘ └─────────┘ └─────────┘        ├─────────────────────────────────────┤
 ┌─────────────────────────────────┐        │   Host operating system (one kernel) │
 │          Hypervisor             │        ├─────────────────────────────────────┤
 ├─────────────────────────────────┤        │             Hardware                 │
 │  Host OS + Hardware             │        └─────────────────────────────────────┘
 └─────────────────────────────────┘
```

| | Virtual machine | Container |
|---|---|---|
| Contains | A **whole operating system** + the app | Only the app + its libraries; **shares** the host's kernel |
| Size | Gigabytes | Megabytes |
| Starts in | Minutes | Seconds (or less) |
| How many on a laptop | A few | Dozens |
| Isolation | Very strong | Strong (good enough for most apps) |
| Example tools | VirtualBox, VMware, Hyper-V | Docker, Podman |

On Windows and Mac, Docker Desktop runs a small hidden Linux VM (via WSL 2 on Windows), and all your Linux containers share that one VM.

### Image vs container

| | **Image** | **Container** |
|---|---|---|
| What | A **read-only template**: files + settings + the command to run | A **running (or stopped) instance** of an image |
| Like… | A **recipe**, a **class**, an installer `.exe` | The **cake**, an **object**, the installed running program |
| How many | One image… | …can start **many** containers |
| Made by | `docker build` (Lesson 18) or `docker pull` | `docker run` |

### Docker Hub — the app store for images

**Docker Hub** (https://hub.docker.com) is a **registry**: a public library of images. Official images exist for almost everything: `python`, `postgres`, `nginx`, `redis`, `node`, `ubuntu`…

An image name looks like:

```text
python:3.13-slim
└─┬──┘ └───┬───┘
 name     tag  (version/variant; default tag = "latest")
```

`docker run python:3.13-slim` → Docker looks on your computer → not there → **downloads (pulls)** it from Docker Hub → starts a container.

### How the pieces talk

```text
  You type:  docker run ...          Docker Engine (daemon)                Docker Hub
  ┌──────────────┐   commands   ┌─────────────────────────────┐   pull   ┌──────────────┐
  │ docker (CLI) │ ───────────► │ builds images, runs          │ ◄─────── │ python, nginx│
  │ in terminal  │              │ containers, manages networks │ ───────► │ postgres ... │
  └──────────────┘              └─────────────────────────────┘   push   └──────────────┘
```

---

## Do it now

> Docker Desktop must be **running** (whale icon in the taskbar/menu bar, "Engine running"). You don't need `.venv` for Docker commands.
>
> **Windows: use PowerShell or Command Prompt, not Git Bash.** Git Bash secretly rewrites paths that start with `/` — `/app` becomes `C:/Program Files/Git/app` — which breaks commands like `docker exec tasks ls /app` and `-v tasks-data:/app/data` in the next lessons. (If you must use Git Bash, put `MSYS_NO_PATHCONV=1 ` in front of the command.)

### Step 1 — Check Docker

```bash
docker version
```

You must see **both** a `Client:` and a `Server:` section. If `Server` shows an error → Docker Desktop isn't running (see *If it does not work*).

### Step 2 — Hello, world

```bash
docker run hello-world
```

```text
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

Read the numbered list it prints — it explains exactly the client → daemon → Docker Hub → container steps from the diagram above.

### Step 3 — List images and containers

```bash
docker images
```

```text
IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
hello-world:latest   1b44b5a3e06a       ...kB          ...kB
```

`hello-world` is tiny — a few kilobytes. The columns depend on your Docker version. Older versions show `REPOSITORY  TAG  IMAGE ID  CREATED  SIZE` instead — same information.

```bash
docker ps
```

Empty! `docker ps` shows only **running** containers. The hello-world container printed its message and **stopped**. Show all, including stopped:

```bash
docker ps -a
```

```text
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      NAMES
4f1c2a9e8b7d   hello-world   "/hello"   30 seconds ago   Exited (0) 29 seconds ago   eager_turing
```

Docker gave it a random funny name.

> A container lives **as long as its main program runs**. When the program ends, the container stops.

### Step 4 — Python in a container (without installing anything)

```bash
docker run -it --rm python:3.13-slim python
```

The first time, it downloads ~50 MB. Then:

```text
Python 3.13.x (main, ...) [GCC ...] on linux
>>>
```

You're in Python 3.13 **on Linux** — even on Windows. Try:

```python
>>> import platform
>>> platform.system()
'Linux'
>>> exit()
```

| Flag | Meaning |
|---|---|
| `-i` + `-t` (`-it`) | interactive + a terminal (so you can type) |
| `--rm` | remove the container automatically when it stops (keeps things tidy) |
| `python:3.13-slim` | the image |
| `python` | the command to run inside the container |

Now look **inside** the container's file system with a shell:

```bash
docker run -it --rm python:3.13-slim bash
```

```bash
ls /
cat /etc/os-release
pip list
exit
```

It's a tiny Debian Linux with Python. Nothing you do inside affects your laptop — and with `--rm` it's all thrown away.

### Step 5 — A web server and port mapping

```bash
docker run -d -p 8080:80 --name web nginx
```

| Flag | Meaning |
|---|---|
| `-d` | **detached**: run in the background, give me my terminal back |
| `-p 8080:80` | **port mapping**: my laptop's port **8080** → the container's port **80** |
| `--name web` | a name we choose (instead of a random one) |
| `nginx` | a popular web server image |

Open **http://localhost:8080** → **"Welcome to nginx!"** 🎉

```text
 Browser ──► localhost:8080 ──(Docker forwards)──► container "web" port 80 ──► nginx
             (YOUR laptop)                          (inside the container)
```

**Why is port mapping needed?** A container has its own private network. nginx listens on port 80 **inside** it. Without `-p`, nothing on your laptop can reach it. The format is always **`-p HOST:CONTAINER`** (outside:inside).

```bash
docker ps
```

```text
CONTAINER ID   IMAGE   COMMAND                  STATUS         PORTS                  NAMES
a7b8c9d0e1f2   nginx   "/docker-entrypoint.…"   Up 20 seconds  0.0.0.0:8080->80/tcp   web
```

### Step 6 — Logs, stop, start, remove

Reload http://localhost:8080 a few times, then:

```bash
docker logs web
```

You see one line per request — nginx's log. (`docker logs -f web` follows new lines live; **Ctrl + C** to stop following.)

```bash
docker stop web
```

http://localhost:8080 doesn't work any more.

```bash
docker start web
```

It works again. Now remove it for good:

```bash
docker stop web
```
```bash
docker rm web
```

### Step 7 — Environment variables (`-e`)

Many images are configured with **environment variables**. The official PostgreSQL image **requires** a password:

```bash
docker run -d --name demo-db -e POSTGRES_PASSWORD=learning123 -p 5433:5432 postgres:17
```

- `-e POSTGRES_PASSWORD=learning123` sets an environment variable **inside** the container.
- `-p 5433:5432` — PostgreSQL listens on 5432 inside; we use **5433** outside in case you already have something on 5432.

Wait ~5 seconds, then run SQL inside the container:

```bash
docker exec -it demo-db psql -U postgres -c "SELECT version();"
```

```text
PostgreSQL 17.x on x86_64-pc-linux-gnu, compiled by gcc ...
```

You have a real PostgreSQL server — no installation, no account, in one command. `docker exec` runs a command **inside a running** container.

Try without the password:

```bash
docker run --rm postgres:17
```

```text
Error: Database is uninitialized and superuser password is not specified.
       You must specify POSTGRES_PASSWORD to a non-empty value for the superuser.
```

The image **reads its settings from environment variables** — your own app will do the same in Lesson 18.

Clean up:

```bash
docker rm -f demo-db
```

(`-f` = stop and remove in one step.)

### Step 8 — Explore Docker Desktop and Docker Hub

1. Open **Docker Desktop** → **Containers** and **Images**: everything you did is visible here too — you can start, stop, delete and read logs by clicking.
2. Go to **https://hub.docker.com/_/python** → the **Tags** tab. Find `3.13-slim`. Notice the different variants: `3.13` (big, ~1 GB), `3.13-slim` (small), `3.13-alpine` (tiny, but sometimes causes problems with some packages).

### Step 9 — Clean up images

```bash
docker images
```
```bash
docker rmi hello-world
```

Keep `python:3.13-slim` and `postgres:17` — you'll use them in Lessons 18 and 19.

---

## Check

- [ ] `docker version` shows Client **and** Server.
- [ ] `hello-world` printed "Hello from Docker!".
- [ ] I ran Python 3.13 on Linux inside a container.
- [ ] nginx answered on http://localhost:8080 through port mapping.
- [ ] I used `docker ps`, `docker logs`, `docker stop`, `docker start`, `docker rm`.
- [ ] I started PostgreSQL with `-e POSTGRES_PASSWORD=...` and ran SQL with `docker exec`.
- [ ] I can explain image vs container, and VM vs container.

---

## What just happened?

### Docker commands so far

| Command | What it does |
|---|---|
| `docker run IMAGE` | Create **and** start a new container (pulls the image if needed) |
| `docker run -it --rm IMAGE CMD` | Interactive, throw away afterwards |
| `docker run -d -p 8080:80 --name NAME IMAGE` | Background, port mapping, a name |
| `docker run -e KEY=value ...` | Set an environment variable inside |
| `docker ps` / `docker ps -a` | Running / all containers |
| `docker logs [-f] NAME` | Show (follow) a container's output |
| `docker exec -it NAME CMD` | Run a command inside a **running** container |
| `docker stop` / `docker start` NAME | Stop / start again |
| `docker rm [-f] NAME` | Remove a container (`-f` even if running) |
| `docker images` | List images |
| `docker pull IMAGE` | Download an image without running it |
| `docker rmi IMAGE` | Remove an image |

### Where is the data?

When you `docker rm` a container, **everything written inside it is gone** — the files, the database rows. Containers are meant to be **disposable**. To keep data you use **volumes** (Lesson 19).

---

## Try it yourself

1. Run two nginx containers at the same time on ports **8081** and **8082** (names `web1`, `web2`). Open both in the browser. Try to start a third one on 8081 — read the error. Remove them all.
2. Run `docker run --rm python:3.13-slim python -c "print(2 ** 100)"`. The container runs one command, prints, and disappears.
3. Run `docker run --rm -e GREETING=Namaste python:3.13-slim python -c "import os; print(os.getenv('GREETING'))"`. How does the container program read the variable?
4. Run `docker system df` — how much disk space are your images and containers using?

---

## If it does not work

| Error | Fix |
|---|---|
| `failed to connect to the docker API ... dockerDesktopLinuxEngine` / `Cannot connect to the Docker daemon` / `error during connect` | Docker Desktop is **not running**. Start it and wait until it says **Engine running**. |
| `docker: command not found` / not recognized | Docker Desktop not installed, or the terminal was opened before installing. Close and reopen VS Code. |
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | Something already uses port 8080 (another container?). `docker ps` → stop it, or use another port: `-p 8090:80`. |
| `Conflict. The container name "/web" is already in use` | A container (maybe stopped) already has that name. `docker rm -f web`, then run again. |
| `the input device is not a TTY` (Git Bash on Windows) | Use PowerShell or Command Prompt, or prefix the command with `winpty`. |
| Pull is very slow / `TLS handshake timeout` | Network problem. Try again, or another network. Office networks sometimes block Docker Hub. |
| `toomanyrequests: You have reached your pull rate limit` | Docker Hub limits anonymous downloads. Wait a while, or create a free Docker Hub account and run `docker login`. |
| Docker Desktop: "WSL 2 is not installed" / "Virtualization not enabled" | See Lesson 02, Part D. |

---

**Next:** [18_DOCKERFILE_BUILD_AND_RUN.md](18_DOCKERFILE_BUILD_AND_RUN.md)
