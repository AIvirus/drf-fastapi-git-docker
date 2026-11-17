# Lesson 15 — GitHub: Push, Pull and Clone

**Time:** 35 minutes  |  **You need:** Lesson 14 finished, an email address

---

## Goal

By the end of this lesson:

- you will have a **GitHub account** and a **repository** called `study-tasks-api`,
- your local `my_fastapi` will be **connected** to it (a "remote"),
- you will **push** your commits to GitHub,
- you will **clone** the repository into a second folder (like a teammate would),
- you will **pull** changes that were made somewhere else.

---

## Understand

### Local and remote repositories

```text
     YOUR LAPTOP                                   GITHUB (the "remote", called origin)
 ┌───────────────────┐        git push        ┌──────────────────────────────┐
 │ my_fastapi/.git   │ ─────────────────────► │ github.com/you/study-tasks-api│
 │ (local repository)│ ◄───────────────────── │ (remote repository)           │
 └───────────────────┘        git pull        └──────────────────────────────┘
                                                        │  git clone
                                                        ▼
                                              ┌───────────────────┐
                                              │ TEAMMATE'S LAPTOP │
                                              └───────────────────┘
```

| Command | Direction | Meaning |
|---|---|---|
| `git remote add origin <url>` | — | "My online copy lives at this URL. Call it `origin`." |
| `git push` | laptop → GitHub | Upload my new commits |
| `git pull` | GitHub → laptop | Download new commits and merge them into my files |
| `git clone <url>` | GitHub → new folder | Download the **whole** repository, with full history, the first time |

Remember: `git commit` only saves on **your laptop**. Nobody else sees it until you `git push`.

### Public or private?

- **Public**: anyone on the internet can **see** the code (only you can change it). Great for a **portfolio** — employers look at GitHub profiles.
- **Private**: only you and people you invite can see it.

Either way: **never push secrets.** Your `.gitignore` from Lesson 14 already keeps `.env` and `*.db` out.

---

## Do it now

### Step 1 — Create a GitHub account

1. Go to **https://github.com/signup**.
2. Use the **same email** you set in `git config user.email` (Lesson 14). Choose a professional username — it will be in your project URLs (e.g. `asha-dev`, not `coolboy123`).
3. Verify your email.

> Recommended: turn on **two-factor authentication** (Settings → Password and authentication). GitHub requires it for most accounts anyway.

### Step 2 — Create an empty repository

1. Top-right **+** → **New repository**.
2. **Repository name:** `study-tasks-api`
3. **Description:** `FastAPI + SQLModel to-do API for studying (Day 3)`
4. **Public** (or Private if you prefer).
5. ⚠ Leave **everything else unticked**: **no** README, **no** .gitignore, **no** license. (Your local repository already has commits; an empty GitHub repository avoids a conflict on the first push.)
6. **Create repository**.

GitHub shows a page "…or push an existing repository from the command line". Keep it open.

### Step 3 — Connect your local repository to GitHub

In the terminal, inside **`my_fastapi`** (replace `YOUR-USERNAME`):

```bash
git remote add origin https://github.com/YOUR-USERNAME/study-tasks-api.git
```

Check:

```bash
git remote -v
```

```text
origin  https://github.com/YOUR-USERNAME/study-tasks-api.git (fetch)
origin  https://github.com/YOUR-USERNAME/study-tasks-api.git (push)
```

### Step 4 — Push!

```bash
git push -u origin main
```

**The first time, Git must log in to GitHub:**

| Computer | What happens |
|---|---|
| **Windows** (Git from git-scm.com) | A window opens → **Sign in with your browser** → **Authorize** Git Credential Manager. Done; Windows remembers it. |
| **macOS / Linux** | GitHub does **not** accept your account password here. Easiest: install the GitHub CLI (https://cli.github.com/) and run `gh auth login` → GitHub.com → HTTPS → Login with a web browser. Then run `git push -u origin main` again. |
| Alternative (any computer) | Create a **Personal Access Token**: GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate (access only to `study-tasks-api`, permission **Contents: Read and write**). When Git asks for a password, paste the **token**. Treat it like a password. |

Success looks like:

```text
Enumerating objects: 9, done.
...
To https://github.com/YOUR-USERNAME/study-tasks-api.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

`-u` ("upstream") connects your local `main` to GitHub's `main`, so from now on you just type **`git push`** and **`git pull`**.

### Step 5 — Look at your code on GitHub

Refresh the repository page in the browser. You see your files, the number of **commits**, and your latest commit message.

- Click **`main.py`** — your code, with colours.
- Click the **commits** link (clock icon) — the same history as `git log`.
- Notice: **no** `tasks.db`, **no** `__pycache__` — `.gitignore` worked.

### Step 6 — Make a change on GitHub and `pull` it

Someone else (here: you, in the browser) changes the project:

1. On GitHub, if you made a `README.md` in Lesson 14, click it → the **pencil ✏ icon**. If not: **Add file → Create new file**, name it `README.md`.
2. Add a line: `Made during Day 3 of the Applied AI and API Integration course.`
3. **Commit changes…** → message `Update README from GitHub` → **Commit changes**.

GitHub now has a commit your laptop doesn't have. Get it:

```bash
git pull
```

```text
Updating 8c4d2e1..5a6b7c8
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)
```

Open `README.md` in VS Code — the new line is there. `git log --oneline` shows the new commit.

### Step 7 — Clone it like a teammate

Pretend you're a new teammate with a fresh laptop. Go to **`Day-03`** and clone into a different folder:

```bash
cd ..
```
```bash
git clone https://github.com/YOUR-USERNAME/study-tasks-api.git teammate_copy
```
```bash
cd teammate_copy
```

```bash
git log --oneline
```

The **full history** came with it. `git clone` already set up `origin` — no `remote add` needed.

Run the teammate's copy to prove it works from GitHub alone:

```bash
pytest -q
```

`5 passed`. (No `tasks.db` here — `.gitignore` kept it out, and the app creates a fresh one when it starts.)

### Step 8 — Teammate pushes, you pull

Still in **`teammate_copy`**, open `main.py` and change the `/version` endpoint to return `"1.1.0"`. Then:

```bash
git add main.py
```
```bash
git commit -m "Bump version to 1.1.0"
```
```bash
git push
```

Back to **your** folder:

```bash
cd ../my_fastapi
```
```bash
git pull
```

Your `main.py` now says `1.1.0`. This is how a team stays in sync: **pull before you start working, push when you've finished something.**

You can delete the `teammate_copy` folder now (it's only a practice copy; everything is on GitHub).

---

## Check

- [ ] My repository `study-tasks-api` exists on GitHub and shows my files and commits.
- [ ] `git remote -v` shows `origin` with my GitHub URL.
- [ ] `tasks.db`, `.env` and `__pycache__` are **not** on GitHub.
- [ ] I pulled a change made on GitHub.
- [ ] I cloned the repository into another folder and its tests passed.
- [ ] A change pushed from the clone arrived in `my_fastapi` with `git pull`.

---

## What just happened?

### The full workflow so far

```text
              edit           git add          git commit             git push
  (files) ─────────► modified ───────► staged ──────────► local repo ─────────► GitHub
                                                              ▲                      │
                                                              └────── git pull ──────┘
```

### `git pull` = `git fetch` + `git merge`

- `git fetch` downloads new commits from GitHub but **doesn't change your files** yet. Safe to run any time.
- `git merge` combines them into your current branch.
- `git pull` does both. If you and a teammate changed the **same lines**, Git asks you to resolve a **conflict** (Lesson 16).

### HTTPS vs SSH

You used an **HTTPS** URL (`https://github.com/...`). Many developers use **SSH** URLs (`git@github.com:...`) with an SSH key instead of a token. Both are fine. HTTPS + browser sign-in is the easiest to start with.

### `origin` and `main` are just names

`origin` = the default nickname for "the remote I cloned from / pushed to". `main` = the default branch name. `git push -u origin main` = "push my `main` branch to the remote called `origin`".

---

## Try it yourself

1. Push your DRF project too: `cd ../my_api`, `git init`, create a `.gitignore` (add `db.sqlite3`, `__pycache__/`, `.env`), commit, create a **new** GitHub repository `journal-api`, connect it and push. (Check `git status` first — `db.sqlite3` must **not** be listed!)
2. On GitHub, open your repository → **Settings** → find where you can change it between **public** and **private** (don't change it now unless you want to).
3. Run `git fetch` and then `git status` when GitHub has a new commit (make one on GitHub first). What does `git status` tell you?
4. Look at someone else's public project, e.g. https://github.com/fastapi/fastapi — find its README, its number of commits, and its **Contributors**.

---

## If it does not work

| Error | Fix |
|---|---|
| `remote: Support for password authentication was removed` | Don't type your GitHub password. Use the browser sign-in (Windows), `gh auth login`, or a **Personal Access Token** (Step 4). |
| `remote: Repository not found` | Wrong URL (check the username and repository name), or you are logged in as a different GitHub user. |
| `error: remote origin already exists` | You already added it. Fix the URL with `git remote set-url origin https://github.com/YOUR-USERNAME/study-tasks-api.git` |
| `! [rejected] main -> main (fetch first)` | GitHub has commits you don't have (e.g. you created the repository **with** a README). Run `git pull` first, then `git push`. If it says *refusing to merge unrelated histories*: `git pull origin main --allow-unrelated-histories`, then push. |
| `error: src refspec main does not match any` | You have no commits yet, or your branch is called `master`. Check `git branch`. Rename with `git branch -M main`. |
| `fatal: not a git repository` | You are in the wrong folder. `cd` into `my_fastapi`. |
| `Your local changes would be overwritten by merge` | Commit (or `git stash`) your own changes first, then `git pull`. |
| I pushed a secret by accident | **Revoke/rotate the secret immediately** (generate a new key/password). Deleting the file in a new commit is **not** enough — it's still in the history. |

---

**Next:** [16_BRANCHES_MERGING_PULL_REQUESTS.md](16_BRANCHES_MERGING_PULL_REQUESTS.md)
