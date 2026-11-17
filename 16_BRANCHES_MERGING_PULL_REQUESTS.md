# Lesson 16 — Branches, Merging and Pull Requests

**Time:** 45 minutes  |  **You need:** Lesson 15 finished

---

## Goal

By the end of this lesson you will:

- create and switch between **branches**,
- build a new feature on a branch without touching `main`,
- open a **pull request (PR)** on GitHub, review it and **merge** it,
- **merge** a branch locally,
- solve a **merge conflict**,
- write a professional **README**,
- know how teams **collaborate** on GitHub.

---

## Understand

### What is a branch?

A **branch** is a separate line of work. `main` is the "official", working version. When you build something new, you make a **new branch**, work there, and only bring it into `main` when it's finished and checked.

```text
main:              A ─── B ─────────────────── M        (M = merge commit / PR merged)
                          \                   /
feature/task-stats:        C ─── D ─── E ────┘
```

- While you work on C, D, E, **`main` stays safe** — it always works.
- Your teammates can work on **their own** branches at the same time.
- If the idea fails, just delete the branch. `main` never saw it.

A branch is very cheap in Git — it's just a **label pointing to a commit**.

### Merging

**Merging** = bringing the commits of one branch into another.

| Kind | When | Result |
|---|---|---|
| **Fast-forward** | `main` didn't change since the branch started | Git just moves the `main` label forward. No extra commit. |
| **Merge commit** (3-way merge) | Both branches have new commits | Git creates a new commit that joins them |
| **Conflict** | Both branches changed **the same lines** | Git asks **you** to choose |

### What is a pull request?

A **pull request (PR)** is GitHub's way of saying: *"I've finished work on branch X. Please review it and pull it into `main`."*

On a PR page your team can:
- read a **description** of the change,
- see **Files changed** (the diff),
- write **comments** on single lines and **approve** or **request changes**,
- see automatic **checks** (tests running on GitHub — Day 6, CI/CD),
- click **Merge**.

Nothing reaches `main` without being seen by at least one other person. This is how almost every software team works.

### The everyday team workflow

```text
1. git switch main  &&  git pull            ← start from the newest main
2. git switch -c feature/my-thing            ← new branch
3. edit, git add, git commit (many times)    ← small commits
4. git push -u origin feature/my-thing       ← upload the branch
5. Open a Pull Request on GitHub             ← ask for review
6. Fix review comments (commit + push again) ← the PR updates by itself
7. Merge the PR on GitHub, delete the branch
8. git switch main  &&  git pull             ← get the merged result
```

---

## Do it now

> Terminal in **`my_fastapi`**. Run `git status` — it should say *working tree clean*. If not, commit your changes first.

### Part A — A feature branch and a pull request

#### Step 1 — See your branches

```bash
git branch
```

```text
* main
```

The `*` shows the branch you're on.

#### Step 2 — Create a branch and switch to it

```bash
git switch -c feature/task-stats
```

```text
Switched to a new branch 'feature/task-stats'
```

(`-c` = create. Older tutorials use `git checkout -b feature/task-stats` — same thing.)

#### Step 3 — Build the feature

Add a statistics endpoint to **`main.py`** — **above** `@app.get("/tasks/{task_id}", ...)`:

```python
@app.get("/tasks/stats", tags=["tasks"])
def task_stats(session: SessionDep):
    tasks = session.exec(select(Task)).all()
    done = sum(1 for task in tasks if task.done)
    return {"total": len(tasks), "done": done, "open": len(tasks) - done}
```

> Already made `/tasks/stats` in Lesson 13's *Try it yourself*? Then build `GET /tasks/count-by-priority` instead, returning e.g. `{"1": 0, "2": 1, "3": 0, "4": 2, "5": 1}`.

And a test at the end of **`test_main.py`**:

```python
def test_stats(client):
    client.post("/tasks", json={"title": "Open task"})
    client.post("/tasks", json={"title": "Finished task", "done": True})
    assert client.get("/tasks/stats").json() == {"total": 2, "done": 1, "open": 1}
```

Run the tests:

```bash
pytest -q
```

All pass → commit:

```bash
git add main.py test_main.py
```
```bash
git commit -m "Add GET /tasks/stats endpoint with test"
```

#### Step 4 — Prove `main` is untouched

```bash
git switch main
```

Look at `main.py` in VS Code — **no `task_stats`**! Your files changed when you switched branches. Now go back:

```bash
git switch feature/task-stats
```

`task_stats` is back. 🪄 Same folder, two versions.

#### Step 5 — Push the branch

```bash
git push -u origin feature/task-stats
```

The output even shows a link:

```text
remote: Create a pull request for 'feature/task-stats' on GitHub by visiting:
remote:      https://github.com/YOUR-USERNAME/study-tasks-api/pull/new/feature/task-stats
```

#### Step 6 — Open a pull request

1. Open your repository on GitHub. A yellow box says **"feature/task-stats had recent pushes"** → click **Compare & pull request**.
2. Check: **base: `main`** ← **compare: `feature/task-stats`**.
3. **Title:** `Add task statistics endpoint`
4. **Description** — a good PR description answers *what, why, how to test*:
   ```markdown
   ## What
   Adds `GET /tasks/stats` that returns the total, done and open task counts.

   ## Why
   The frontend dashboard needs a quick summary without downloading every task.

   ## How to test
   1. `uvicorn main:app --reload`
   2. Create a few tasks in `/docs`, mark one as done
   3. Open `/tasks/stats`
   4. `pytest -q` → all tests pass (new test: `test_stats`)
   ```
5. **Create pull request**.

#### Step 7 — Review it

1. Click the **Files changed** tab. You see the diff: green lines added.
2. Hover over a line → click the blue **+** → write a comment, e.g. *"Nice — maybe we could also count high-priority tasks later."* → **Add single comment**.
3. (In a team, a **reviewer** would click **Review changes → Approve**. GitHub doesn't let you approve your own PR — that's on purpose.)

#### Step 8 — Merge it

1. Back on the **Conversation** tab → **Merge pull request** → **Confirm merge**.
2. Click **Delete branch** (the work is now in `main`; the branch label isn't needed).
3. Go to the **Code** tab → `main.py` now contains `task_stats`.

#### Step 9 — Update your laptop

```bash
git switch main
```
```bash
git pull
```
```bash
git branch -d feature/task-stats
```

`git log --oneline` now shows your feature commit **and** a "Merge pull request #1 …" commit.

---

### Part B — A professional README (merged locally)

A **README.md** is the front page of your repository — the first thing employers, teammates and *future you* read. GitHub shows it under the file list. It's written in **Markdown** (the same format as these lessons).

#### Step 10 — Branch, write, commit

```bash
git switch -c docs/readme
```

Replace **`README.md`** with (change the name and username):

````markdown
# Study Tasks API

A small REST API to manage study tasks, built with **FastAPI**, **SQLModel** and **SQLite**.
Made during Day 3 of the *Applied AI and API Integration* course.

## Features

- Create, list, read, update and delete tasks (CRUD)
- Filter by `done` and `priority`, search by title, paging with `offset`/`limit`
- Task statistics (`/tasks/stats`)
- Automatic validation (Pydantic) and interactive docs (Swagger UI)
- Automated tests with pytest

## Tech stack

Python 3 · FastAPI · SQLModel · SQLite · Uvicorn · pytest

## Run it locally

```bash
git clone https://github.com/YOUR-USERNAME/study-tasks-api.git
cd study-tasks-api
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install fastapi "uvicorn[standard]" sqlmodel pytest httpx
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs

## API endpoints

| Method | URL | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks (`?done=`, `?priority=`, `?search=`, `?offset=`, `?limit=`) |
| GET | `/tasks/stats` | Count of total / done / open tasks |
| GET | `/tasks/{id}` | Get one task |
| PATCH | `/tasks/{id}` | Update some fields |
| DELETE | `/tasks/{id}` | Delete a task |

Example:

```json
POST /tasks
{"title": "Learn Docker", "priority": 4}
```

## Run the tests

```bash
pytest -v
```

## Author

Your Name — [GitHub](https://github.com/YOUR-USERNAME)
````

Save, then:

```bash
git add README.md
```
```bash
git commit -m "Write README with setup, endpoints and tests"
```

#### Step 11 — Merge it locally

```bash
git switch main
```
```bash
git merge docs/readme
```

```text
Updating 1a2b3c4..5d6e7f8
Fast-forward
 README.md | 52 ++++++++++++++++++++++++
```

**Fast-forward** — `main` had no new commits, so Git just moved the label. Clean up and push:

```bash
git branch -d docs/readme
```
```bash
git push
```

Open your repository on GitHub — the README is shown, nicely formatted, below the files. 🎉

> In a team you'd use a PR for this too. Merging locally is fine for your own projects — and it's good to know both ways.

---

### Part C — Your first merge conflict (on purpose)

Conflicts are normal. Let's create one safely so it isn't scary when it happens for real.

#### Step 12 — Two branches change the same line

```bash
git switch -c change-welcome
```

In `main.py` change the welcome line in `read_root` to:

```python
    return {"message": "Welcome to the Study Tasks API — happy learning!", "docs": "/docs"}
```

```bash
git commit -am "Make welcome message friendlier"
```

(`-am` = add all **already-tracked** changed files + commit, in one step.)

Now go back to `main` and change the **same line** differently:

```bash
git switch main
```

```python
    return {"message": "Welcome to Study Tasks API v1!", "docs": "/docs"}
```

```bash
git commit -am "Show version in welcome message"
```

#### Step 13 — Merge → conflict!

```bash
git merge change-welcome
```

```text
Auto-merging main.py
CONFLICT (content): Merge conflict in main.py
Automatic merge failed; fix conflicts and then commit the result.
```

Open **`main.py`** in VS Code:

```python
<<<<<<< HEAD
    return {"message": "Welcome to Study Tasks API v1!", "docs": "/docs"}
=======
    return {"message": "Welcome to the Study Tasks API — happy learning!", "docs": "/docs"}
>>>>>>> change-welcome
```

| Marker | Meaning |
|---|---|
| `<<<<<<< HEAD` … `=======` | **Your** version (the branch you're on: `main`) |
| `=======` … `>>>>>>> change-welcome` | The **incoming** version (the branch you're merging) |

#### Step 14 — Resolve it

VS Code shows buttons above the conflict: **Accept Current Change | Accept Incoming Change | Accept Both Changes | Compare Changes**. You can also just **edit the text by hand** — the goal is that the final file is correct and **all three marker lines are gone**. Let's combine both ideas:

```python
    return {"message": "Welcome to Study Tasks API v1 — happy learning!", "docs": "/docs"}
```

Save. Check that the app still works (`pytest -q`). Then finish the merge:

```bash
git add main.py
```
```bash
git commit -m "Merge change-welcome: combine both welcome messages"
```
```bash
git branch -d change-welcome
```
```bash
git push
```

Conflict solved. The rule: **Git can't guess which version is right — a human decides.**

---

## Check

- [ ] I created a branch, committed on it, and saw that `main` didn't change.
- [ ] My PR #1 on GitHub has a description, a comment, and is **Merged** (purple).
- [ ] My README shows on the repository's front page.
- [ ] I created, resolved and committed a merge conflict.
- [ ] `git branch` shows only `main`; `git status` says *working tree clean*.
- [ ] `git log --oneline --graph` shows the branch lines joining. (Try it!)

---

## What just happened?

### Branch commands

| Command | Does |
|---|---|
| `git branch` | List local branches (`*` = current) |
| `git switch -c <name>` | Create a branch and switch to it |
| `git switch <name>` | Switch to an existing branch |
| `git merge <name>` | Bring `<name>`'s commits into the **current** branch |
| `git branch -d <name>` | Delete a branch that's already merged |
| `git push -u origin <name>` | Upload a branch to GitHub (first time) |
| `git log --oneline --graph --all` | Draw the branch history |

### Branch naming habits

`feature/task-stats`, `fix/404-on-missing-task`, `docs/readme`, `refactor/split-models`. Lowercase, dashes, a prefix that says what kind of work it is.

### How teams collaborate on GitHub

| Way | How | Used for |
|---|---|---|
| **Collaborators** | Repository → Settings → **Collaborators** → Add people. They push branches to **your** repository and open PRs. | Your team / classmates |
| **Forks** | Someone clicks **Fork** → gets their own copy → pushes there → opens a PR back to you. | Open source (you don't know the contributors) |
| **Branch protection** | Settings → **Branches** → rule for `main`: "Require a pull request before merging", "Require approvals", "Require status checks" | Stop anyone pushing directly to `main` |
| **Issues** | The **Issues** tab: bug reports and to-do items. A PR description with `Closes #3` closes issue 3 when merged. | Planning, bug tracking |

---

## Try it yourself

1. **Team exercise** (with a classmate): add each other as **collaborators**. Each person: clone the other's repository, create a branch, add a small endpoint (e.g. `/tasks/oldest`), push and open a PR. **Review** your partner's PR (comment + approve), then they merge it.
2. Create an **issue** in your repository: *"Add a PUT endpoint"*. Create a branch, add `PUT /tasks/{task_id}`, open a PR with `Closes #<issue number>` in the description, and merge it. What happened to the issue?
3. Add a **branch protection rule** for `main` (Settings → Branches → Add rule → `main` → *Require a pull request before merging*). Now try `git push` directly on `main` — what happens?
4. Add a "Docker" section to your README after Lessons 18–19.

---

## If it does not work

| Problem | Fix |
|---|---|
| `error: Your local changes to the following files would be overwritten by checkout` | Commit your changes first (or `git stash`, switch, then `git stash pop`). |
| `error: The branch 'x' is not fully merged` | You tried `git branch -d` on a branch that isn't merged. Merge it first, or `-D` to delete it anyway (loses those commits!). |
| No "Compare & pull request" button on GitHub | Go to **Pull requests → New pull request**, choose base `main` and compare `feature/task-stats`. |
| PR says "Can't automatically merge" | There's a conflict with `main`. Locally: `git switch feature/...`, `git pull origin main`, resolve the conflict, commit, push. The PR updates. |
| During a conflict I want to give up | `git merge --abort` → everything goes back to how it was before the merge. |
| VS Code doesn't show the Accept buttons | Edit the file by hand — delete the `<<<<<<<`, `=======`, `>>>>>>>` lines and keep the code you want. |
| `git commit -am` didn't include a new file | `-a` only adds files Git **already tracks**. New files need `git add <file>` first. |
| The README table/code doesn't look formatted on GitHub | Markdown needs blank lines before tables and code blocks, and code blocks need three backticks on their own line. |

---

**Next:** [17_DOCKER_BASICS.md](17_DOCKER_BASICS.md)
