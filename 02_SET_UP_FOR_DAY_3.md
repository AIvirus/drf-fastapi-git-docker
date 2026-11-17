# Lesson 02 — Set Up Your Computer for Day 3

**Time:** 30 minutes (+ download time for Docker Desktop)  |  **You need:** Lesson 01 finished

---

## Goal

By the end of this lesson you will have:

1. a fresh **virtual environment** for Day 3 with all Python packages installed,
2. **Postman** — an app for sending API requests,
3. **Git** — the version control tool (Lessons 14–16),
4. **Docker Desktop** — for containers (Lessons 17–19),

and you will call an API **from Python** for the first time.

---

## Understand

| Tool | What it is | Used in |
|---|---|---|
| **`.venv`** | A private box of Python packages for this project only (same as Day 2) | All lessons |
| **Django REST Framework (DRF)** | An add-on for Django that makes building APIs easy | 03–09 |
| **SimpleJWT** | An add-on for DRF that creates JWT login tokens | 08 |
| **FastAPI** | A different, fast, modern Python framework built only for APIs | 10–13 |
| **SQLModel** | Lets FastAPI save data in a database using Python classes | 13 |
| **pytest** | Runs automated tests | 13 |
| **Postman** | A desktop app to send any request (GET, POST, PUT, PATCH, DELETE) with headers and JSON | 03–09 |
| **Git** | Saves snapshots ("versions") of your code | 14–16 |
| **Docker Desktop** | Runs your app inside a "container" — a small, portable box | 17–19 |

Why a **new** `.venv` for Day 3? Each project should have its own packages. Day 3 needs packages Day 2 did not have (and later projects may need different versions). Keeping them separate avoids "it worked yesterday!" problems.

---

## Do it now

### Part A — Python packages

#### Step 1 — Open the Day-03 folder in VS Code

**File → Open Folder…** → choose the **`Day-03`** folder → **Select Folder**.

Open a terminal: **Terminal → New Terminal**. The line should end with `Day-03>`.

#### Step 2 — Check Python

```bash
python --version
```

You need **3.11, 3.12, 3.13 or 3.14**. (Mac/Linux: use `python3` if `python` is not found. Windows: you can also try `py --version`.)

#### Step 3 — Create and activate the virtual environment

```bash
python -m venv .venv
```

Activate it:

| Computer | Command |
|---|---|
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

The line now starts with **`(.venv)`**.

> **VS Code tip:** press **Ctrl + Shift + P** → **Python: Select Interpreter** → choose the one that shows `.venv`. New terminals will then activate it automatically.

#### Step 4 — Install the packages

```bash
pip install -r requirements.txt
```

This takes 1–3 minutes.

#### Step 5 — Check the important packages

```bash
python -c "import django, rest_framework, fastapi, sqlmodel; print('Django', django.get_version()); print('DRF', rest_framework.VERSION); print('FastAPI', fastapi.__version__)"
```

Expected (your numbers may be a little higher):

```text
Django 5.2.x
DRF 3.18.x
FastAPI 0.1xx.x
```

#### Step 6 — Call an API from Python

`fastapi[standard]` also installed **httpx**, a library for sending HTTP requests from Python. Try it:

```bash
python -c "import httpx; r = httpx.get('https://jsonplaceholder.typicode.com/posts/1'); print(r.status_code); print(r.json()['title'])"
```

Expected:

```text
200
sunt aut facere repellat provident occaecati excepturi optio reprehenderit
```

You just did in Python what the browser did in Lesson 01. `r.json()` turned the JSON text into a Python **dictionary**.

---

### Part B — Postman

1. Go to **https://www.postman.com/downloads/** and download the desktop app for your computer.
2. Install and open it. If it asks you to sign in, you can create a free account **or** look for **"Continue without an account"** / **"Skip"** (the wording changes between versions). An account lets you save your work online; it is not required.
3. Click **New → HTTP** (or the **+** tab).
4. Leave the method on **GET**, paste `https://jsonplaceholder.typicode.com/posts/1` and click **Send**.
5. At the bottom you see the JSON **Body**, and on the right **Status: 200 OK** and the time in ms.

Now try something a browser address bar cannot do — a **POST** with a JSON body:

1. Change **GET** to **POST**, URL `https://jsonplaceholder.typicode.com/posts`
2. Click **Body** → **raw** → choose **JSON** in the drop-down on the right.
3. Type:
   ```json
   {
     "title": "My first POST",
     "body": "Sent from Postman",
     "userId": 1
   }
   ```
4. Click **Send** → **Status: 201 Created** and the answer contains `"id": 101`.

> jsonplaceholder is a **fake** practice API: it answers like a real one but does not really save your post.

> **No Postman? (e.g. a locked office laptop)** You can use the **Thunder Client** or **REST Client** extension inside VS Code instead, or use the browser-based API pages that DRF (Lesson 03) and FastAPI (Lesson 10) give you for free.

---

### Part C — Git

Check whether Git is already installed:

```bash
git --version
```

If you see `git version 2.x.x` → done, skip to Part D.

If you see "not recognized" / "command not found":

| Computer | Install |
|---|---|
| **Windows** | Download from **https://git-scm.com/downloads/win** → run the installer. Keep the default options, **except**: on the screen *"Adjusting the name of the initial branch in new repositories"* choose **"Override the default branch name"** and type **`main`**. |
| **macOS** | Run `xcode-select --install` in Terminal (or `brew install git` if you use Homebrew). |
| **Linux (Ubuntu/Debian)** | `sudo apt update && sudo apt install git` |

**Close VS Code completely and open it again** (so the terminal finds Git), activate `.venv`, and run `git --version` again.

---

### Part D — Docker Desktop

Docker Desktop is a big download (~600 MB) and needs a restart on Windows. **Start it now; you only need it in Lesson 17.** Continue with Lesson 03 while it downloads.

| Computer | Install |
|---|---|
| **Windows 10/11** | Download from **https://www.docker.com/products/docker-desktop/** → run the installer → keep **"Use WSL 2 instead of Hyper-V"** ticked → restart when asked. If it says WSL needs an update, open PowerShell **as Administrator** and run `wsl --update`. |
| **macOS** | Download the right version: **Apple chip** (M1/M2/M3/M4) or **Intel chip** ( → About This Mac tells you). Drag Docker to Applications and open it. |
| **Linux** | Follow **https://docs.docker.com/desktop/setup/install/linux/** (or install Docker Engine: https://docs.docker.com/engine/install/). |

Open Docker Desktop once and accept the terms. (Docker Desktop is free for personal use, education and small companies.) Wait until the bottom-left says **"Engine running"** (green).

Then in a **new** terminal:

```bash
docker --version
```

Expected: `Docker version 2x.x.x, build ...`

---

## Check

- [ ] The terminal line starts with `(.venv)` and ends with `Day-03>`.
- [ ] Step 5 printed versions for Django, DRF and FastAPI.
- [ ] Step 6 printed `200` and a title.
- [ ] Postman: GET → **200 OK**; POST → **201 Created**.
- [ ] `git --version` prints a version.
- [ ] `docker --version` prints a version (or Docker is still downloading — that is OK for now).

---

## What just happened?

- `pip install -r requirements.txt` read the list of packages and installed them **only inside `.venv`**.
- `httpx.get(...)` sent an HTTP **GET** request, exactly like the browser did, and `r.json()` converted the JSON into Python objects. Later, your **own** apps will call **your own** APIs like this — and so will AI agents.
- Postman lets you choose **any** method, add **headers** (like login tokens) and a **JSON body**. You will use it a lot today.

---

## Try it yourself

1. In Postman, send `DELETE https://jsonplaceholder.typicode.com/posts/1`. What status code do you get?
2. In Postman, send `PATCH https://jsonplaceholder.typicode.com/posts/1` with body `{"title": "Changed"}`. What does the answer contain — only the title, or the whole post?
3. In Python, print how many posts user 1 has:
   ```bash
   python -c "import httpx; print(len(httpx.get('https://jsonplaceholder.typicode.com/posts', params={'userId': 1}).json()))"
   ```
   `params=` builds the `?userId=1` query parameter for you.

---

## If it does not work

| Problem | Fix |
|---|---|
| `running scripts is disabled on this system` (PowerShell) | Use **Command Prompt** and `.venv\Scripts\activate.bat`, or run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `Could not open requirements file` | You are in the wrong folder. The terminal must end with `Day-03>`. Use `cd` to go there. |
| `No module named rest_framework` / `fastapi` | `.venv` is not active (no `(.venv)` at the start), or Step 4 failed. Activate and run Step 4 again. |
| `pip install` fails building `psycopg` | Very rare with `psycopg[binary]`. You can remove the `psycopg` line from `requirements.txt` for today — you only need it to connect to PostgreSQL from your own computer. |
| httpx: `ConnectError` / SSL error | Check your internet. Office networks sometimes block requests — try a hotspot. |
| `git` / `docker` not recognized after installing | **Close VS Code fully and reopen it.** The old terminal does not know about newly installed programs. |
| Docker Desktop: "WSL 2 installation is incomplete" | Open PowerShell **as Administrator**: `wsl --install` (or `wsl --update`), then restart the computer. |
| Docker Desktop: "Virtualization must be enabled" | Virtualization is switched off in your computer's BIOS/UEFI. Search "enable virtualization" + your laptop brand, or ask your IT team. You can still do Lessons 01–16. |

---

**Next:** [03_YOUR_FIRST_DRF_API.md](03_YOUR_FIRST_DRF_API.md)
