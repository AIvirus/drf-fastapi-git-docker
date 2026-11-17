# Lesson 14 — Git Basics: Your Local Repository

**Time:** 40 minutes  |  **You need:** Lesson 13 finished, Git installed (Lesson 02)

---

## Goal

By the end of this lesson you will:

- explain what **version control** is and why every developer uses it,
- set up Git with your **name and email**,
- turn `my_fastapi` into a **Git repository**,
- understand the **three areas**: working directory → staging area → repository,
- use `git init`, `git status`, `git add`, `git commit`, `git log`, `git diff`,
- keep secrets and junk out of Git with **`.gitignore`**,
- undo a mistake.

---

## Understand

### Version control in one picture

Without version control:

```text
main.py   main_v2.py   main_final.py   main_final_REALLY.py   main_final_fixed_asha.py
```

With **version control**, you have **one** `main.py` and a full **history** of every saved version — who changed what, when and why — and you can go back to any version.

| Without Git | With Git |
|---|---|
| Copies of files with strange names | One file, full history |
| "Who broke this?" — nobody knows | `git log` shows who, when and why |
| Emailing ZIP files to teammates | Everyone works on the same repository |
| Afraid to try new ideas | Try it on a **branch**; throw it away if it fails (Lesson 16) |

### Git vs GitHub

| **Git** | **GitHub** |
|---|---|
| A **program** on your computer | A **website** that stores Git repositories online |
| Works offline | Needs internet |
| Saves the history of your project | Shares it, backs it up, adds pull requests, issues, reviews |
| Made in 2005 by Linus Torvalds (creator of Linux) | A company (owned by Microsoft). Alternatives: GitLab, Bitbucket |

Git is the **camera**; GitHub is the **online photo album**. This lesson is only Git; Lesson 15 adds GitHub.

### The three areas — the most important idea in Git

```text
  WORKING DIRECTORY          STAGING AREA               LOCAL REPOSITORY
  (your files, as you        ("the box" of changes      (.git folder: the history
   edit them in VS Code)      for the next snapshot)     of all snapshots/commits)

     main.py  ───git add───►   main.py  ───git commit───►  commit a1b2c3 "Add tasks API"
     (changed)                 (ready)                     commit 9f8e7d "First commit"
```

Think of a **photo studio**:

1. **Working directory** — people walk around the studio (you edit files freely).
2. **`git add`** — you ask some people to step onto the stage (choose which changes go into the next photo).
3. **`git commit`** — click! A photo of the stage is taken and put in the album **forever**, with a caption (the commit message).

Why the stage in the middle? So you can choose: "this commit is only the bug fix, not the half-finished new feature in the other file."

### What is a commit?

A **commit** is a snapshot of your project with:
- a unique id (a **hash** like `a1b2c3d`),
- the **author** (name + email),
- the **date**,
- a **message** that explains **why** you made the change,
- a link to the commit before it.

---

## Do it now

### Step 1 — Tell Git who you are (once per computer)

```bash
git config --global user.name "Your Name"
```
```bash
git config --global user.email "you@example.com"
```
```bash
git config --global init.defaultBranch main
```

- Use the **same email** you will use for GitHub in Lesson 15 (GitHub uses it to connect commits to your account).
- `init.defaultBranch main` names the first branch `main` (the modern standard).

Windows only — make line endings behave nicely:

```bash
git config --global core.autocrlf true
```

Check:

```bash
git config --global --list
```

You see `user.name=...`, `user.email=...`, `init.defaultbranch=main`.

### Step 2 — Go to your project

The terminal must be in **`my_fastapi`**. Stop uvicorn if it is running.

```bash
cd my_fastapi
```

(If you are in `Day-03`. Check with `pwd` on Mac/Linux or look at the end of the prompt on Windows.)

### Step 3 — Create the repository

```bash
git init
```

```text
Initialized empty Git repository in .../Day-03/my_fastapi/.git/
```

Git created a **hidden** folder `.git` — that *is* the repository (the album). Never edit or delete it by hand.

> ⚠ Run `git init` **only inside `my_fastapi`**. Don't run it in your home folder or `Day-03` — then Git would track everything in there.

### Step 4 — Ask Git what's going on

```bash
git status
```

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .pytest_cache/
        __pycache__/
        database.py
        main.py
        models.py
        tasks.db
        test_main.py

nothing added to commit but untracked files present (use "git add" to track)
```

**Untracked** = Git sees these files but doesn't save them yet.

Wait — we don't want `__pycache__/`, `.pytest_cache/` or `tasks.db` in our history! They're generated files (and a database can contain private data).

### Step 5 — Create `.gitignore`

Create a new file **`my_fastapi/.gitignore`** (the name starts with a dot):

```gitignore
# Python and tool caches
__pycache__/
*.py[cod]
.pytest_cache/

# Virtual environments
.venv/
venv/

# Local databases (each developer has their own)
*.db
*.sqlite3

# Secrets — NEVER commit these
.env

# Editor / OS files
.vscode/
.DS_Store
Thumbs.db
```

```bash
git status
```

```text
Untracked files:
        .gitignore
        database.py
        main.py
        models.py
        test_main.py
```

The junk is gone from the list. ✔

### Step 6 — Stage your files (`git add`)

```bash
git add .gitignore main.py models.py database.py test_main.py
```

(Or `git add .` = "add everything that isn't ignored". Always run `git status` first so you know what "everything" is!)

```bash
git status
```

```text
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   database.py
        new file:   main.py
        new file:   models.py
        new file:   test_main.py
```

The files are now on the **stage** (green in most terminals).

### Step 7 — Take the snapshot (`git commit`)

```bash
git commit -m "Add Study Tasks API with SQLModel database and tests"
```

```text
[main (root-commit) 3f2a1bc] Add Study Tasks API with SQLModel database and tests
 5 files changed, 230 insertions(+)
 create mode 100644 .gitignore
 ...
```

```bash
git status
```

```text
On branch main
nothing to commit, working tree clean
```

**"Working tree clean"** = everything is saved in the repository.

### Step 8 — Make a change and see the whole cycle

Open **`main.py`** and add a new endpoint (above `/tasks/{task_id}`, e.g. right after `/health`):

```python
@app.get("/version")
def version():
    return {"version": "1.0.0"}
```

Save, then:

```bash
git status
```

```text
Changes not staged for commit:
        modified:   main.py
```

See **exactly** what changed:

```bash
git diff
```

```diff
+@app.get("/version")
+def version():
+    return {"version": "1.0.0"}
```

Lines starting with **`+`** were added, **`-`** removed. (Press **q** to quit if the output fills the screen.)

Stage and commit:

```bash
git add main.py
```
```bash
git commit -m "Add /version endpoint"
```

### Step 9 — Read the history (`git log`)

```bash
git log
```

```text
commit 8c4d2e1f... (HEAD -> main)
Author: Your Name <you@example.com>
Date:   Tue Nov 17 22:10:00 2026 +0530

    Add /version endpoint

commit 3f2a1bc9...
Author: Your Name <you@example.com>
Date:   Tue Nov 17 22:00:00 2026 +0530

    Add Study Tasks API with SQLModel database and tests
```

Shorter version:

```bash
git log --oneline
```

```text
8c4d2e1 (HEAD -> main) Add /version endpoint
3f2a1bc Add Study Tasks API with SQLModel database and tests
```

`HEAD` = "where you are now".

### Step 10 — Undo mistakes

**A) Undo changes you haven't staged** (go back to the last commit):

Delete the whole `/health` endpoint from `main.py` by accident and save. Then:

```bash
git restore main.py
```

The endpoint is back. ⚠ This throws away your **unsaved-in-Git** changes to that file — use it carefully.

**B) Unstage a file** (take it off the stage, keep the changes):

```bash
git restore --staged main.py
```

**C) See an old version of a file:**

```bash
git show 3f2a1bc:main.py
```

(Use **your** first commit's id from `git log --oneline`.) It prints `main.py` as it was in the first commit — without `/version`.

---

## Check

- [ ] `git config --global --list` shows my name, email and `init.defaultbranch=main`.
- [ ] `my_fastapi` has a `.git` folder (hidden) and a `.gitignore` file.
- [ ] `git status` does **not** list `tasks.db`, `__pycache__/` or `.pytest_cache/`.
- [ ] `git log --oneline` shows **2 commits**.
- [ ] I used `git diff` to see a change before committing it.
- [ ] I used `git restore` to undo a change.

---

## What just happened?

### The commands so far

| Command | Area it works on | What it does |
|---|---|---|
| `git init` | — | Create a new repository (`.git` folder) here |
| `git status` | all three | **Your best friend.** What changed? What's staged? |
| `git add <file>` | working → **staging** | Put changes on the stage |
| `git commit -m "msg"` | staging → **repository** | Save a snapshot with a message |
| `git diff` | working vs staging | What did I change (not yet staged)? |
| `git diff --staged` | staging vs last commit | What will the next commit contain? |
| `git log` / `--oneline` | repository | The history |
| `git restore <file>` | working | Throw away unstaged changes |
| `git restore --staged <file>` | staging → working | Unstage, keep the change |

### The life of a file

```text
untracked ──git add──► staged ──git commit──► committed (unmodified)
                          ▲                          │ you edit it
                          └────── git add ◄──── modified
```

### Good commit messages

| ✘ Bad | ✔ Good |
|---|---|
| `update` | `Add /version endpoint` |
| `fix` | `Fix 500 error when task title is empty` |
| `asdf` | `Return 404 instead of 500 for missing tasks` |
| `changes 17 Nov` | `Add search and paging to GET /tasks` |

Rules of thumb: start with a **verb** (Add, Fix, Remove, Update, Refactor), say **what** and if needed **why**, keep the first line under ~70 characters. One commit = **one logical change**.

### Why `.gitignore` matters so much

- **Secrets** (`.env`, API keys, passwords): once pushed to GitHub, consider them **stolen** — bots scan GitHub for keys within minutes. Even if you delete the file later, it stays in the **history**.
- **Generated files** (`__pycache__`, `.venv`): huge, different on every computer, can be re-created.
- **Local databases** (`*.db`): every developer has their own data.

---

## Try it yourself

1. Add a **`README.md`** to `my_fastapi` with a title and one sentence about the project. Commit it with a good message. (You'll improve it in Lesson 16.)
2. Change two files (e.g. `main.py` and `README.md`), but commit **only** `README.md`. Then commit `main.py` separately. Check with `git log --oneline` that you have two separate commits.
3. Create a file `secret.env` with `API_KEY=12345`. Run `git status` — is it listed? Add `*.env` to `.gitignore` and check again. Commit the `.gitignore` change, then delete `secret.env`.
4. Run `git log --oneline --stat`. What extra information do you see?

---

## If it does not work

| Problem | Fix |
|---|---|
| `fatal: not a git repository` | You are not inside `my_fastapi` (or you didn't run `git init`). |
| `Author identity unknown *** Please tell me who you are` | Do Step 1 (`user.name` and `user.email`). |
| `nothing added to commit but untracked files present` | You forgot `git add` before `git commit`. |
| Commit opened a strange editor (Vim) | You ran `git commit` without `-m "..."`. In Vim: press **Esc**, type `:q!` and **Enter**, then commit again with `-m`. |
| `git log` shows `:` at the bottom and doesn't stop | It's a pager. Press **q** to quit. |
| `warning: in the working copy of 'main.py', LF will be replaced by CRLF` | Normal on Windows with `core.autocrlf true` — just a notice, not an error. |
| `tasks.db` is still in `git status` | The `.gitignore` file must be in `my_fastapi` (next to `main.py`), named exactly `.gitignore` (not `.gitignore.txt`). |
| I committed `tasks.db` before adding `.gitignore` | `git rm --cached tasks.db` (removes it from Git, keeps the file), then commit. |
| `git status` lists files from **outside** `my_fastapi` | You ran `git init` in the wrong folder. Delete that wrong `.git` folder (show hidden files), then `cd` into `my_fastapi` and run `git init` there. |

---

**Next:** [15_GITHUB_PUSH_PULL_CLONE.md](15_GITHUB_PUSH_PULL_CLONE.md)
