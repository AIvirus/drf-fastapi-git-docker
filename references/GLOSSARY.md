# Glossary — Simple Meanings of Every New Word (Day 3)

Words are in A→Z order. The number in brackets is the lesson where you meet it first. Day 2 words (model, migration, ORM, view…) are in Day 2's glossary.

| Word | Simple meaning |
|---|---|
| **Access token** | A short-lived JWT sent with every request: `Authorization: Bearer ...`. (08) |
| **`@action`** | DRF decorator that adds an extra endpoint to a ViewSet, e.g. `/articles/mine/`. (06) |
| **API** | Application Programming Interface — a fixed way for programs to ask another program for data or actions. (01) |
| **API root** | The page at `/api/` made by `DefaultRouter`, listing all resources. (06) |
| **`@api_view`** | DRF decorator that turns a function into an API view and lists allowed methods. (03) |
| **`APIView`** | DRF base class for class-based API views: one method per HTTP verb. (05) |
| **`APITestCase`** | DRF test class with an API client and a temporary database. (09) |
| **Authentication** | Finding out **who** is calling (session, token, JWT). (07) |
| **Authorization** | Deciding what the caller is **allowed** to do (permissions). (07) |
| **Bearer token** | A token sent as `Authorization: Bearer <token>` — "whoever bears (holds) it". (08) |
| **Branch** | A separate line of work in Git; `main` is the official one. (16) |
| **Browsable API** | DRF's web page for exploring and trying your API in the browser. (03) |
| **Build context** | The folder (the `.` in `docker build .`) whose files Docker can `COPY`. (18) |
| **Claim** | A piece of information inside a JWT payload, e.g. `user_id`, `exp`. (08) |
| **Clone** | Download a whole Git repository (with history) the first time. (15) |
| **Collection (Postman)** | A saved, shareable group of requests. (09) |
| **Collection (REST)** | The URL for a list of resources, e.g. `/api/articles/`. (01) |
| **Commit** | A saved snapshot of your project in Git, with a message, author and date. (14) |
| **Container** | A running (or stopped) instance of an image — an isolated box with your app and its dependencies. (17) |
| **Containerization** | Packing an app with everything it needs so it runs the same everywhere. (17) |
| **Content negotiation** | Choosing the response format (JSON/HTML) from the request's `Accept` header. (03) |
| **CRUD** | Create, Read, Update, Delete. (01) |
| **Daemon / Docker Engine** | The background program that builds images and runs containers. (17) |
| **Dependency (FastAPI)** | A function FastAPI calls for you and passes into an endpoint via `Depends(...)`, e.g. a database session. (13) |
| **Deserialize** | Turn JSON into validated Python data / objects. (04) |
| **Docker Compose** | Tool to run several containers together from one `compose.yaml`. (19) |
| **Docker Hub** | Online registry (library) of Docker images. (17) |
| **Dockerfile** | A text recipe for building a Docker image. (18) |
| **`.dockerignore`** | List of files Docker must not copy into an image. (18) |
| **Endpoint** | One URL + method of an API, e.g. `POST /tasks`. (01) |
| **Environment (Postman)** | A named set of variables, e.g. Local vs Production. (09) |
| **Environment variable** | A setting given to a program from outside its code, e.g. `DATABASE_URL`. (18) |
| **FastAPI** | Modern, fast Python framework for building APIs with type hints. (10) |
| **Fast-forward** | A merge where Git just moves the branch label forward (no merge commit). (16) |
| **Fetch** | Download new commits from a remote without merging them. (15) |
| **Fork** | Your own copy of someone else's GitHub repository. (16) |
| **Generic view** | A DRF class with ready-made CRUD logic, e.g. `ListCreateAPIView`. (05) |
| **Git** | Version control program that records the history of your files. (14) |
| **GitHub** | Website that hosts Git repositories and adds pull requests, issues, reviews. (15) |
| **`.gitignore`** | List of files Git must not track (secrets, caches, local databases). (14) |
| **HEAD** | Git's pointer to "where you are now" (usually the latest commit of your branch). (14) |
| **Header (HTTP)** | Extra information sent with a request/response, e.g. `Authorization`, `Content-Type`. (01) |
| **Healthcheck** | A command/endpoint used to test if a service is ready and alive. (19) |
| **`HTTPException`** | FastAPI exception you `raise` to return an error status, e.g. 404. (12) |
| **Image** | A read-only template for containers: files, settings and a start command. (17) |
| **JSON** | JavaScript Object Notation — the text format APIs use for data. (01) |
| **JWT** | JSON Web Token — a signed token that carries its own information (header.payload.signature). (08) |
| **Layer (Docker)** | One step of an image; unchanged layers are reused from cache. (18) |
| **Merge** | Bring the commits of one branch into another. (16) |
| **Merge conflict** | Both branches changed the same lines; a human must choose. (16) |
| **`ModelSerializer`** | DRF serializer that builds its fields from a Django model. (04) |
| **`ModelViewSet`** | DRF ViewSet with all six CRUD actions. (06) |
| **OpenAPI** | Standard JSON/YAML description of a REST API; FastAPI generates it at `/openapi.json`. (10) |
| **`origin`** | Default name of the remote repository (e.g. on GitHub). (15) |
| **Pagination** | Returning results in pages (`?page=2`). (06) |
| **Path parameter** | A value inside the URL path, e.g. `7` in `/tasks/7`. (11) |
| **Payload (JWT)** | The middle part of a JWT with the claims. Readable by anyone — not secret. (08) |
| **Permission class** | DRF class that decides if a request is allowed, e.g. `IsAuthenticated`. (07) |
| **Port mapping** | `-p HOST:CONTAINER` — forward a port on your computer into a container. (17) |
| **Postman** | Desktop app for sending and testing API requests. (02) |
| **Pull** | Download new commits from a remote and merge them. (15) |
| **Pull request (PR)** | A GitHub request to review and merge a branch. (16) |
| **Push** | Upload your commits to a remote. (15) |
| **Pydantic** | Python library that validates data using type hints; FastAPI uses it. (11) |
| **Query parameter** | `key=value` data after `?` in a URL, e.g. `?done=true`. (01, 11) |
| **README** | The front-page document of a repository (`README.md`). (16) |
| **Refresh token** | A longer-lived JWT used only to get a new access token. (08) |
| **Registry** | A server that stores images (Docker Hub). (17) |
| **Remote** | Another copy of the repository, e.g. on GitHub. (15) |
| **Repository (repo)** | A project tracked by Git, including its full history (`.git` folder). (14) |
| **Request body** | Data sent with POST/PUT/PATCH, usually JSON. (11) |
| **Resource** | A "thing" an API exposes with its own URL, e.g. an article. (01) |
| **`response_model`** | FastAPI setting that filters and documents what an endpoint returns. (11) |
| **REST** | A style for designing web APIs: resources, HTTP methods, representations, stateless, status codes. (01) |
| **Router (DRF)** | Creates URL patterns for ViewSets automatically. (06) |
| **Safe methods** | GET, HEAD, OPTIONS — requests that only read. (07) |
| **Serializer** | DRF class that converts objects ⇄ JSON and validates input. (04) |
| **Service (Compose)** | One container definition in `compose.yaml`, e.g. `api`, `db`. Its name is also its hostname. (19) |
| **Session (SQLModel)** | One conversation with the database: `add`, `commit`, `refresh`. (13) |
| **Signature (JWT)** | Proves the token was made by the server and not changed. (08) |
| **SQLModel** | Library where one class is both a Pydantic model and a database table. (13) |
| **Staging area** | Git's "box" of changes for the next commit (`git add`). (14) |
| **Stateless** | Each request carries everything needed; the server doesn't remember the last one. (01) |
| **Status code** | The number in a response that says what happened, e.g. 201, 404. (01) |
| **Swagger UI** | Interactive API documentation page (`/docs` in FastAPI). (10) |
| **Tag (Docker)** | The version part of an image name: `python:3.13-slim`. (17) |
| **Token** | A string a client sends to prove who it is, instead of a password. (07) |
| **Type hint** | Python annotation like `count: int`; FastAPI uses it to read and validate data. (11) |
| **Uvicorn** | The ASGI server that runs a FastAPI app. (10) |
| **Version control** | Recording every version of your files so you can go back and collaborate. (14) |
| **ViewSet** | One DRF class for all actions of a resource (list, create, retrieve…). (06) |
| **Virtual machine (VM)** | A whole simulated computer with its own operating system. (17) |
| **Volume** | Docker storage that lives outside a container's life — keeps data. (18, 19) |
| **Working directory** | Your project's files as you see and edit them. (14) |
| **YAML** | A settings file format where indentation shows structure (`compose.yaml`). (19) |
