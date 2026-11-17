# Lesson 20 — Final Checklist and What's Next

**Time:** 15 minutes  |  **You need:** Lessons 01–19 finished

---

## Goal

Check that you really understand everything from today, and see how it connects to the next days.

---

## Part 1 — "I can DO it" checklist

**Django REST Framework (`my_api`)**
- [ ] I can start the API and open the browsable API at `/api/`.
- [ ] Articles and categories have full CRUD through a **router** and **ViewSets**.
- [ ] Logged-out users see only published articles; authors also see their own drafts.
- [ ] `?search=`, `?ordering=`, `?category=` and pagination work.
- [ ] Another user gets **403** when editing my article; a normal user gets **403** creating a category.
- [ ] I can register, get a **Token** and a **JWT** pair, and call `/api/auth/me/` with each.
- [ ] I can refresh an expired JWT access token.
- [ ] My Postman collection logs in by itself and runs with all tests passing.
- [ ] `python manage.py test` → **OK**.

**FastAPI (`my_fastapi`)**
- [ ] I can run the app with `uvicorn main:app --reload` and use `/docs`.
- [ ] I can read **path** and **query** parameters and a **JSON body** (Pydantic model).
- [ ] Bad input gets **422** with clear messages; a missing task gets **404**.
- [ ] Tasks are saved in a database with **SQLModel** and survive a restart.
- [ ] `pytest -v` → all passed.

**Git and GitHub**
- [ ] `my_fastapi` is a Git repository with a good `.gitignore` (no `.env`, no `*.db`).
- [ ] I can do the cycle: `git status` → `git add` → `git commit` → `git push`.
- [ ] My project is on GitHub with a **README**.
- [ ] I created a feature branch, opened a **pull request** and merged it.
- [ ] I resolved a merge conflict.

**Docker**
- [ ] I can build an image from my **Dockerfile** and run it with port mapping.
- [ ] I can pass settings with `-e` / `--env-file`.
- [ ] I used a **volume** to keep data.
- [ ] `docker compose up --build` runs my API + PostgreSQL.
- [ ] `Dockerfile`, `.dockerignore` and `compose.yaml` are on GitHub.

---

## Part 2 — "I can EXPLAIN it" checklist

Explain each one **out loud** (or to a friend) in one or two sentences. If you can't, re-read the lesson in brackets.

1. What is an API? What makes it REST? *(01)*
2. Which HTTP method and status code for create / read / update / delete? *(01)*
3. 400 vs 401 vs 403 vs 404 vs 422. *(01, 07, 11)*
4. What does a serializer do — in both directions? *(04)*
5. `@api_view` vs `APIView` vs generic views vs ViewSets — when to use which? *(05, 06)*
6. What does a router do? *(06)*
7. Why must the server — never the client — set the article's author? *(04, 06)*
8. Authentication vs authorization. *(07)*
9. `has_permission` vs `has_object_permission`. *(07)*
10. Simple Token vs JWT. Access vs refresh token. *(07, 08)*
11. Why is a JWT safe from changes but **not** secret? *(08)*
12. Django + DRF vs FastAPI — when would you pick each? *(10)*
13. Path parameter vs query parameter vs request body. *(11)*
14. What is Pydantic and what happens when validation fails? *(11)*
15. PUT vs PATCH, and what `exclude_unset=True` is for. *(12)*
16. What is a dependency (`Depends`) and why is it useful for tests? *(13)*
17. Working directory → staging area → repository. *(14)*
18. Git vs GitHub. `push` vs `pull` vs `clone`. *(14, 15)*
19. What is a branch? What is a pull request and why do teams use them? *(16)*
20. Virtual machine vs container. Image vs container. *(17)*
21. What does each line of your Dockerfile do? Why copy `requirements.txt` first? *(18)*
22. What does `-p 8000:8000` mean? Why `--host 0.0.0.0`? *(17, 18)*
23. Why read settings from environment variables? *(18, 19)*
24. Why does the API use `db` as the hostname in Compose? *(19)*
25. What is a volume, and what does `docker compose down -v` do? *(18, 19)*

More practice questions → [practice/WORKBOOK.md](practice/WORKBOOK.md) (answers in [practice/ANSWERS.md](practice/ANSWERS.md) — try first, then check!)

---

## Part 3 — Bonus challenges (pick any)

1. **Comments API (DRF):** add a `Comment` model (`article`, `author`, `text`, `created_at`) with a ViewSet at `/api/comments/`. Anyone reads; logged-in users comment; only the comment's author can edit/delete. Write tests.
2. **Nested route (DRF):** `GET /api/articles/<id>/comments/` using an `@action(detail=True)`.
3. **Users and tasks (FastAPI):** add an `owner` field to tasks and a fake login: a header `X-User: asha` read with `Header()`; each user only sees their own tasks.
4. **Call your FastAPI from Python:** write `client.py` that uses `httpx` to create 5 tasks and print the stats — your first **API integration** script.
5. **One Compose file, two APIs:** run `my_api` (DRF), `my_fastapi` and one PostgreSQL (with two databases) in a single `compose.yaml`.
6. **CI preview:** add `.github/workflows/tests.yml` that runs `pytest` on every push (search "GitHub Actions Python"). Day 6 covers this properly.

For each challenge: **branch → code → test → commit → push → pull request → merge**.

---

## Part 4 — How today connects to the next days

| Day | What you'll do | What you'll reuse from today |
|---|---|---|
| **Day 4** | **Blog Discovery & Recommendation** project | DRF serializers, ViewSets, routers, permissions, JWT, Postman; Git branches and PRs for teamwork |
| **Day 5** | **AI WarRoom** project | FastAPI + Pydantic for AI services, calling APIs with `httpx`, OpenAPI docs that AI agents can read, Docker Compose for multi-service setups |
| **Day 6** | Linux, servers, CI/CD, monitoring | Dockerfiles and images, environment variables, GitHub Actions running your tests, deploying containers |

If you can **build an endpoint, validate its input, protect it, test it, commit it and put it in a container**, you're ready for the projects.

---

## Keep these handy

| File | Use it when… |
|---|---|
| [references/COMMANDS_CHEAT_SHEET.md](references/COMMANDS_CHEAT_SHEET.md) | You forgot a command (DRF, FastAPI, Git, Docker) |
| [references/COMMON_ERRORS.md](references/COMMON_ERRORS.md) | Something is red and you don't know why |
| [references/HTTP_STATUS_CODES.md](references/HTTP_STATUS_CODES.md) | You got a status code and want to know what it means |
| [references/DJANGO_VS_FASTAPI.md](references/DJANGO_VS_FASTAPI.md) | You must choose a framework |
| [references/GLOSSARY.md](references/GLOSSARY.md) | You don't know a word |
| [references/PROFESSIONAL_HABITS.md](references/PROFESSIONAL_HABITS.md) | You want to work like a real software team |
| [drf_lab/](drf_lab/README.md), [fastapi_lab/](fastapi_lab/README.md) | You want to compare with the finished versions |

**Congratulations — you built two REST APIs, put your code on GitHub with a real team workflow, and shipped it in containers!** 🎉
