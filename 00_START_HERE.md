# START HERE — Day 3: REST APIs, FastAPI, GitHub and Docker

Welcome to Day 3! Yesterday you built a **website** that sends **HTML pages** to a browser.
Today you will build **APIs** that send **data (JSON)** to *any* program: a mobile app, a React website, another server, or an AI agent.

By the end of today **you will have built, by yourself**:

1. **Journal API** — a Django REST Framework API for articles and categories, with register, login tokens (Token + JWT), permissions and tests.
2. **Study Tasks API** — a FastAPI app with a database, validation and automatic Swagger documentation.
3. A **GitHub repository** for your FastAPI project, with branches, a pull request and a good README.
4. A **Docker image** of your FastAPI app, and a **Docker Compose** setup that runs it together with a PostgreSQL database.

You need **Day 2** (Django basics: models, views, URLs, admin, ORM). You do **not** need to know APIs, Git or Docker before you start.

---

## How every lesson works

Every lesson has the same parts, in the same order (just like Day 2):

| Part | What you do |
|---|---|
| **Goal** | Read what you will be able to do at the end. |
| **Understand** | Read a short, simple explanation. |
| **Do it now** | Type the commands and code **exactly** as shown. |
| **Check** | Compare your screen with what you *should* see. |
| **What just happened?** | Read what your code actually did. |
| **Try it yourself** | A small challenge, so you really learn it. |
| **If it does not work** | The most common mistakes and how to fix them. |

> **Golden rule:** Do not move to the next lesson until the **Check** of the current lesson works.

---

## Your learning path (do these in order)

### First half — APIs with Django REST Framework and FastAPI

| # | Lesson | What you build / do | Time |
|---|---|---|---|
| 01 | [What is a REST API?](01_WHAT_IS_A_REST_API.md) | Call a real API from the browser and from Python | 25 min |
| 02 | [Set up for Day 3](02_SET_UP_FOR_DAY_3.md) | `.venv`, packages, Postman, Git, Docker Desktop | 30 min |
| 03 | [Your first DRF API](03_YOUR_FIRST_DRF_API.md) | Install DRF, make `/api/hello/`, see the browsable API | 25 min |
| 04 | [Models and serializers](04_MODELS_AND_SERIALIZERS.md) | Turn database rows into JSON (and back) | 35 min |
| 05 | [API views: function, class, generic](05_API_VIEWS.md) | The same CRUD API written 3 ways | 45 min |
| 06 | [ViewSets, routers and full CRUD](06_VIEWSETS_ROUTERS_AND_CRUD.md) | 2 classes → 12 endpoints, search, pagination | 40 min |
| 07 | [Authentication, permissions and tokens](07_AUTHENTICATION_AND_PERMISSIONS.md) | Register, Token login, "only the author can edit" | 45 min |
| 08 | [JWT authentication](08_JWT_AUTHENTICATION.md) | Access + refresh tokens with SimpleJWT | 25 min |
| 09 | [Test your API with Postman (and Python)](09_TEST_YOUR_API_WITH_POSTMAN.md) | Collections, environments, test scripts, `APITestCase` | 40 min |
| 10 | [Your first FastAPI app](10_YOUR_FIRST_FASTAPI_APP.md) | Hello FastAPI + Swagger UI; Django vs FastAPI | 25 min |
| 11 | [Path & query parameters, Pydantic](11_PARAMETERS_AND_PYDANTIC.md) | Read the URL and validate JSON automatically | 35 min |
| 12 | [CRUD endpoints in FastAPI](12_FASTAPI_CRUD.md) | A full Tasks API (data in memory) | 35 min |
| 13 | [FastAPI with a database](13_FASTAPI_WITH_A_DATABASE.md) | Save tasks with SQLModel + SQLite, add tests | 40 min |

### Second half — Git, GitHub and Docker

| # | Lesson | What you build / do | Time |
|---|---|---|---|
| 14 | [Git basics: your local repository](14_GIT_BASICS.md) | `init`, `status`, `add`, `commit`, `log` | 40 min |
| 15 | [GitHub: push, pull, clone](15_GITHUB_PUSH_PULL_CLONE.md) | Put your project on GitHub | 35 min |
| 16 | [Branches, merging and pull requests](16_BRANCHES_MERGING_PULL_REQUESTS.md) | Feature branch → pull request → merge, write a README | 45 min |
| 17 | [Docker basics](17_DOCKER_BASICS.md) | Images, containers, Docker Hub, port mapping | 35 min |
| 18 | [Dockerfile: containerize your FastAPI app](18_DOCKERFILE_BUILD_AND_RUN.md) | Write a Dockerfile, build, run, env variables | 40 min |
| 19 | [Docker Compose: API + PostgreSQL](19_DOCKER_COMPOSE.md) | Two containers with one command | 35 min |
| 20 | [Final checklist and what's next](20_FINAL_CHECKLIST_AND_WHATS_NEXT.md) | Check everything you learned | 15 min |

Total: about 10–11 hours. It is completely fine to split it over two days (for example Lessons 01–13 on day one, 14–20 on day two).

---

## What is in this folder?

```text
Day-03/
├── 00_START_HERE.md          ← you are here
├── 01_ ... 20_ lessons       ← read and do these in order
├── requirements.txt          ← Python packages for today (Lesson 02)
├── my_api/                   ← YOU create this in Lesson 03 (your DRF project)
├── my_fastapi/               ← YOU create this in Lesson 10 (your FastAPI project → Git → Docker)
├── drf_lab/                  ← FINISHED DRF project (answer key for Lessons 03–09)
├── fastapi_lab/              ← FINISHED FastAPI project + Dockerfile + compose (answer key for 10–19)
├── postman/                  ← a ready-made Postman collection (Lesson 09)
├── practice/                 ← revision questions + answers
└── references/               ← cheat sheet, common errors, glossary, Django vs FastAPI…
```

### Your folders vs the answer keys — important!

| You build… | Compare with… | Lessons |
|---|---|---|
| `my_api/` | `drf_lab/` | 03 – 09 |
| `my_fastapi/` | `fastapi_lab/` | 10 – 19 |

- Example: your `my_api/journal/serializers.py` ↔ the answer `drf_lab/journal/serializers.py`.
- Do **not** copy whole folders. You learn by typing, running and fixing.
- Want to see the finished projects first? Follow [drf_lab/README.md](drf_lab/README.md) and [fastapi_lab/README.md](fastapi_lab/README.md) after Lesson 02.

---

## What you need before Lesson 01

- A laptop with **Windows 10/11, macOS, or Linux**, and about **10 GB free disk space** (Docker needs space).
- **Python 3.11, 3.12, 3.13 or 3.14** and **VS Code** (you installed both on Day 2).
- **Internet connection.**
- Free accounts you will create today: **Postman** (optional — you can use it without an account), **GitHub** (Lesson 15), **Docker Hub** (optional, Lesson 18).
- Lesson 02 installs **Postman**, **Git** and **Docker Desktop**. Docker Desktop is the biggest download — you can start it downloading now.

> **Good news:** today you do **not** need a Neon database. Your DRF project uses **SQLite** (a database in a single file, built into Python). In Lesson 19 Docker gives you a real PostgreSQL in one command.

---

## When you are stuck

1. Read the **If it does not work** part at the bottom of the lesson.
2. Read [references/COMMON_ERRORS.md](references/COMMON_ERRORS.md).
3. Compare your file with the same file in `drf_lab/` or `fastapi_lab/`.
4. Read the **last line** of the red error message first — it usually tells you exactly what is wrong.
5. An API error? Look at the **status code** first: [references/HTTP_STATUS_CODES.md](references/HTTP_STATUS_CODES.md).
6. Do not know a word? Look in [references/GLOSSARY.md](references/GLOSSARY.md).

Ready? Open **[01_WHAT_IS_A_REST_API.md](01_WHAT_IS_A_REST_API.md)**
