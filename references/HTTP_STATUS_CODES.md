# HTTP Status Codes — What They Mean for Your API

**Memory trick:** 1xx info · **2xx success** · 3xx go somewhere else · **4xx the client made a mistake** · **5xx the server made a mistake**.

## Success (2xx)

| Code | Name | When you'll see it today | Who sends it |
|---|---|---|---|
| **200** | OK | GET, PUT, PATCH worked | DRF, FastAPI (default) |
| **201** | Created | POST created something | DRF `create`, FastAPI `status_code=201` |
| **204** | No Content | DELETE worked; body is empty | DRF `destroy`, FastAPI `status_code=204` |

## Redirects (3xx)

| Code | Name | When |
|---|---|---|
| **301 / 308** | Moved Permanently | e.g. Django adding a missing final slash (`/api/articles` → `/api/articles/`) |
| **302** | Found | Day 2 login redirects (websites, not APIs) |

> APIs rarely redirect. If a POST to `/api/articles` (no slash) fails in Django, add the slash.

## Client errors (4xx) — "fix your request"

| Code | Name | Meaning | Typical cause today | Fix |
|---|---|---|---|---|
| **400** | Bad Request | Data is invalid (DRF) | Serializer validation failed | Read the error JSON; fix the data |
| **401** | Unauthorized | **Not authenticated** — "who are you?" | No token, wrong token, expired JWT | Log in / send `Authorization` header / refresh JWT |
| **403** | Forbidden | **Authenticated, but not allowed** | Editing someone else's article; non-staff creating a category | Correct user / role |
| **404** | Not Found | The resource doesn't exist (for you) | Wrong id; someone else's draft; wrong URL | Check id, URL, user |
| **405** | Method Not Allowed | URL exists, method doesn't | POST to `/api/hello/`; DELETE on a list URL | Use the allowed method / correct URL |
| **409** | Conflict | Clashes with current state | Duplicate title (Lesson 12 challenge) | Change the data |
| **415** | Unsupported Media Type | Server can't read this body format | Body sent as text instead of JSON | Set Body → raw → **JSON** (`Content-Type: application/json`) |
| **422** | Unprocessable Content | Data is invalid (FastAPI/Pydantic) | Wrong type, too short, out of range, missing field | Read `detail[].loc` and `msg` |
| **429** | Too Many Requests | Rate limit | Calling a public API too often (GitHub, Docker Hub) | Wait; authenticate |

### 401 vs 403 in one sentence

**401** = "I don't know who you are." **403** = "I know who you are, and the answer is no."

### 400 (DRF) vs 422 (FastAPI)

Both mean "your data is wrong". DRF uses 400 with `{"field": ["message"]}`; FastAPI uses 422 with `{"detail": [{"loc": [...], "msg": "..."}]}`.

## Server errors (5xx) — "the server has a problem"

| Code | Name | Meaning | What to do |
|---|---|---|---|
| **500** | Internal Server Error | A bug — an exception in your code | Read the terminal (uvicorn/runserver) or `docker logs` — the traceback is there |
| **502** | Bad Gateway | A proxy couldn't reach your app | App crashed / wrong port (Day 6) |
| **503** | Service Unavailable | Server overloaded or starting | Wait / check health |

> A **500 is always the server's fault.** Good APIs validate input so that bad data gives a **4xx**, never a 500.

## Reading a response in Postman

1. Look at the **status** (top right of the response).
2. Read the **body** — DRF/FastAPI explain the problem there.
3. Check **Headers** if needed (`Content-Type`, `WWW-Authenticate`, `Allow`).
