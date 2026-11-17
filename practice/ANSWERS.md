# Answers — Day 3 Practice Workbook

Try the questions in [WORKBOOK.md](WORKBOOK.md) first. Your wording can be different — what matters is the meaning.

## Section A — REST APIs
1. An API is a fixed way for one program to ask another program for data or actions. Example: a food-delivery app asks the restaurant system's API "is dosa available?" and gets data back, without seeing the kitchen.
2. A website returns HTML for humans; an API returns data (usually JSON) for programs.
3. REpresentational State Transfer — a style for designing web APIs. Ideas: resources with URLs, HTTP methods as verbs, representations (JSON), stateless requests, meaningful status codes.
4. The HTTP **method** already is the verb. Nouns keep URLs simple and predictable: `GET /articles/`, `DELETE /articles/7/`.
5. Create = POST, list = GET (collection), read one = GET (item), replace = PUT, change part = PATCH, delete = DELETE.
6. 200 OK; 201 Created; 204 No Content (success, nothing to return); 400 Bad Request (invalid data, DRF); 401 not authenticated; 403 authenticated but not allowed; 404 not found; 405 method not allowed; 422 invalid data (FastAPI); 500 server bug.
7. JSON is a text format for data. `{"name": "Asha", "age": 21, "subjects": ["Python", "SQL"], "is_active": true}`
8. Each request carries everything the server needs (e.g. the token); the server doesn't remember previous requests.
9. Extra key=value data after `?` that filters or changes the result: `/books?author=5&limit=10`.
10. `GET /books/` → 200 · `POST /books/` → 201 · `PATCH /books/12/` → 200 · `DELETE /books/12/` → 204 · `GET /books/?author=5` → 200 (or the nested `GET /authors/5/books/`).
11. `Content-Type: application/json`.

## Section B — Django REST Framework basics
12. An add-on for Django to build APIs: serializers, API views, generic views, ViewSets, routers, authentication, permissions, pagination, the browsable API.
13. `HttpResponse` sends finished text/HTML. `Response` takes Python data and renders it as JSON (or the browsable HTML) depending on the request.
14. A web page DRF generates to explore and try your API. Content negotiation: the browser's `Accept` header prefers `text/html`; Postman accepts JSON.
15. It converts model objects → Python dicts → JSON (serialize), and JSON → validated data → model objects (deserialize).
16. With `Serializer` you write every field and `create()`/`update()` yourself; `ModelSerializer` generates them from the model.
17. `is_valid()` runs all checks and returns True/False; `errors` holds the problems; `validated_data` holds the clean data; `save()` creates or updates the object.
18. One field: a method `validate_<field>(self, value)`. Several fields: `validate(self, data)`. Raise `serializers.ValidationError`.
19. Shows the author's username in output but ignores it in input — the client can't pretend to be another author.
20. The field is accepted as input but never sent in output. Example: a password on a register serializer.
21. Ids `[1, 2]`; the `__str__` text `["Django", "APIs"]`; full objects `[{"id": 1, "name": "Django", ...}]`.
22. Turns a function into a DRF view that only accepts those methods (others → 405) and gives it DRF's request/response.
23. Functions branch with `if request.method == ...`; classes have one method per verb (`get`, `post`…). Classes can be extended and reused.
24. Ready-made views for common patterns: `ListCreateAPIView` (GET list, POST), `RetrieveUpdateDestroyAPIView` (GET, PUT, PATCH, DELETE), `RetrieveAPIView` (GET one), `CreateAPIView` (POST).
25. To add extra data when saving, e.g. `serializer.save(author=self.request.user)`.
26. One class with all actions for a resource: list, create, retrieve, update, partial_update, destroy.
27. It creates the URL patterns for a ViewSet automatically. `DefaultRouter` also adds an API root page.
28. Which rows exist for this request. If a draft isn't in another user's queryset, `get_object()` can't find it → 404 (they can't even learn it exists).
29. Returning results in pages (e.g. 10 at a time) instead of everything, so responses stay small and fast.
30. `detail=False` → an extra URL on the collection (`/articles/mine/`); `detail=True` → on one item (`/articles/7/publish/`).
31. The N+1 query problem: extra database queries for every row's related objects.
32. PUT replaces the whole object (all required fields must be sent); PATCH changes only the fields sent.

## Section C — Authentication and permissions
33. Authentication = who are you? Authorization = what may you do?
34. 401 = not authenticated (no/invalid credentials). 403 = authenticated, but not allowed.
35. Session (browser, browsable API), Basic (username+password each request, testing), Token (`Token <key>`, simple apps/scripts), JWT (`Bearer <access>`, mobile/SPA/many services).
36. AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, custom classes (e.g. IsAuthorOrReadOnly).
37. `has_permission` runs for every request to the view; `has_object_permission` runs when a single object is used (retrieve/update/delete).
38. GET, HEAD, OPTIONS — methods that only read.
39. `permission_classes` replaces the default. Without `IsAuthenticatedOrReadOnly`, anonymous users could POST, because `IsAuthorOrReadOnly` only checks objects.
40. Header `Authorization: Token <key>`. Header `Authorization: Bearer <access token>`.
41. `create_user()` hashes the password; `create()` would store it in plain text and login would fail.
42. Header (algorithm), payload (claims: user_id, exp…), signature.
43. Not secret — it's only base64-encoded, anyone can read it. It can't be changed without breaking the signature, which needs the server's `SECRET_KEY`.
44. Access: short-lived, sent with every request. Refresh: longer-lived, only used to get a new access token.
45. Simple tokens need a database lookup on every request and never expire.
46. JWTs are signed with it. If it leaks, anyone can forge valid tokens for any user.

## Section D — Testing APIs
47. Collection = saved group of requests. Environment = named set of variables (e.g. Local vs Production). Variable = `{{name}}` replaced by a value.
48. After the response arrives, it reads the `access` token from the JSON and saves it in the environment variable `access`.
49. To check the whole API in seconds after every change, in the right order, with pass/fail results.
50. A temporary test database created for the tests and deleted afterwards — the real data is never touched, tests can run anywhere.
51. `force_authenticate` skips login (good for permission tests). `credentials` adds a real header (good for testing tokens/login).
52. Otherwise the data is sent as a form, not JSON (lists and nested data don't arrive as intended).
53. Arrange (prepare data), Act (do the request), Assert (check the result).

## Section E — FastAPI
54. A modern Python framework only for APIs. Advantages: automatic validation from type hints, automatic docs (Swagger/ReDoc), very fast, async support, little code.
55. Django + DRF: you need an admin and user accounts; big business app with many models. FastAPI: a small microservice; serving an AI/ML model; very high concurrency.
56. The server program that receives HTTP requests and passes them to the FastAPI app. `main` = file `main.py`, `app` = the variable, `--reload` = restart on file changes (development only).
57. Swagger UI (interactive docs), ReDoc (read-only docs), the raw OpenAPI description.
58. A standard JSON/YAML description of an API. Tools and AI agents can read it to know which endpoints exist and how to call them.
59. Name in the path → path parameter. Simple type not in the path → query parameter. Pydantic model → JSON body.
60. Give it a default, e.g. `q: str | None = None`.
61. A validation library using type hints. FastAPI returns 422 with a list of all errors; your function isn't called.
62. Text at least 3 characters; number ≥ 1 and ≤ 5.
63. It filters/converts the output to that model. Example: `UserPublic` removes the password from a returned user.
64. `raise HTTPException(status_code=404, detail="Task not found")`.
65. The client must not send `id`/`created_at` (server decides); updates need all-optional fields; responses always include `id`.
66. It returns only the fields the client actually sent; otherwise PATCH would overwrite other fields with `None`.
67. FastAPI matches routes in order; `/tasks/{task_id}` would catch `stats` and fail with 422 (not an integer).
68. A library combining Pydantic and SQLAlchemy: one class is both a validation model and a database table. `table=True` = create a database table for this class.
69. `add` prepares the object to be saved, `commit` writes it to the database, `refresh` reads it back (e.g. to get the new id).
70. Dependency injection: FastAPI calls `get_session()` for each request and closes the session afterwards. In tests you can override it with a test database.
71. No — it only creates missing tables, it doesn't change existing ones. Real projects use Alembic migrations.
72. Normal `def`. FastAPI runs it in a thread pool. `async def` only helps if everything inside is async; slow normal code inside `async def` blocks the server.

## Section F — Git
73. A system that records every version of your files. Solves: lost/overwritten work, not knowing who changed what and why, hard teamwork.
74. Git = the version-control program on your computer. GitHub = a website that hosts Git repositories and adds collaboration (PRs, issues).
75. Working directory = your files as you edit them; staging area = changes chosen for the next commit; repository (`.git`) = all saved commits.
76. `init` creates a repository; `status` shows what changed/staged; `add` stages changes; `commit` saves a snapshot; `log` shows history; `diff` shows line-by-line changes.
77. To choose exactly which changes go into a commit, so each commit is one logical change.
78. A snapshot of the project with an id (hash), author, date, message and a link to the previous commit.
79. "Add search to GET /tasks", "Fix 500 error when title is empty", "Remove unused imports in models.py" — they start with a verb, say what (and why), are short and specific.
80. A list of files Git must ignore. `.env` (secrets), `.venv/` (big, re-creatable), `__pycache__/` (generated), `*.db` (local data).
81. No — it stays in the history. Revoke/rotate the secret immediately (make a new key/password).
82. `git restore <file>`. `git restore --staged <file>`.

## Section G — GitHub and collaboration
83. A remote is another copy of the repository (e.g. on GitHub). `origin` is the default name for it.
84. push = upload my commits; pull = download and merge new commits; clone = download a whole repository the first time.
85. fetch downloads new commits but doesn't change your files; pull = fetch + merge.
86. The local repository already had commits; an empty GitHub repository avoids an "unrelated histories" conflict on the first push.
87. A separate line of work. Teams use branches to build features without breaking `main`, work in parallel, and review before merging.
88. Fast-forward: `main` hasn't changed, so its label just moves forward. Merge commit: both branches changed, so a new commit joins them.
89. Both branches changed the same lines; Git can't decide. Between `<<<<<<<` and `=======` is your current version; between `=======` and `>>>>>>>` is the incoming version.
90. A request to merge a branch, with discussion. Teams can read a description, see the diff, comment on lines, approve/request changes, see automatic checks, merge.
91. What changed, why, and how to test it (plus linked issues, screenshots if UI).
92. Collaborators push branches to your repository directly. Forks are copies in someone else's account; they open PRs from there (open source).
93. Rules on a branch (e.g. `main`): no direct pushes, PR required, approvals/checks required.
94. Title and description, features, tech stack, setup/run instructions, endpoints/usage, tests, (Docker), author/license.

## Section H — Docker
95. "It works on my machine" — Docker packs the app with its exact runtime and dependencies so it runs the same everywhere.
96. A VM contains a whole OS, a container shares the host kernel; containers are MBs vs GBs; start in seconds vs minutes; you can run many more containers.
97. An image is a read-only template (recipe); a container is a running/stopped instance of it (the cake). One image → many containers.
98. A public registry of images. A tag is the version/variant after the colon, e.g. `python:3.13-slim` (default `latest`).
99. `-d` background; `-it` interactive terminal; `--rm` delete when stopped; `-p 8080:80` host port 8080 → container port 80; `-e` set an environment variable; `--name` choose a name; `-v` mount a volume.
100. A container has its own private network; without mapping, your laptop can't reach the port inside.
101. Running containers only vs all containers including stopped ones.
102. Runs a command inside a running container.
103. A recipe for building an image. FROM = base image; WORKDIR = working folder; COPY = copy files in; RUN = run a command at build time; EXPOSE = document the port; CMD = the command when a container starts.
104. RUN happens once, while building the image. CMD runs every time a container starts.
105. Layer caching: the slow `pip install` layer is reused when only the code changes.
106. Keeps files out of the image: `.venv/` (size), `.env` (secrets), `*.db` / `__pycache__` / `.git` (local junk).
107. `127.0.0.1` only accepts connections from inside the container itself; `0.0.0.0` accepts the forwarded connections from the host.
108. Read settings from environment variables and pass them at run time with `-e` / `--env-file` / Compose `environment:`.
109. It's deleted with the container. Use a volume (`-v name:/path`).
110. A tool to define and run multi-container apps from one YAML file with one command.
111. Compose creates a network where each service's name is its hostname. Inside the api container, `localhost` is the api container itself.
112. `healthcheck` tells Docker how to test if the database is ready; `depends_on` with `service_healthy` makes the api start only after that.
113. `down` removes containers and the network but keeps volumes (data). `down -v` also deletes the volumes (data gone).
114. Containers run the image they were created from; `--build` rebuilds the image with your new code.
