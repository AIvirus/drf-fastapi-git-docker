# Lesson 01 — What Is a REST API?

**Time:** 25 minutes  |  **You need:** a browser (Day 2 finished)

---

## Goal

By the end of this lesson you will:

- explain what an **API** is, using a restaurant example,
- explain what makes an API **REST**,
- read **JSON**,
- match **HTTP methods** to **CRUD** actions,
- call a **real public API** from your browser and read its status code.

---

## Understand

### Website vs API

On Day 2 your Django views returned **HTML** — a page made for **humans** to look at.

An **API** (Application Programming Interface) returns **data** — made for **programs** to use.

| | Website (Day 2) | API (today) |
|---|---|---|
| Who reads the answer? | A person, in a browser | A program: mobile app, React site, another server, an AI agent |
| What is sent back? | HTML (headings, buttons, colours) | **JSON** (just the data) |
| Example answer | `<h1>Learn Django</h1><p>by asha</p>` | `{"title": "Learn Django", "author": "asha"}` |

### The restaurant example

```text
 YOU (client)          WAITER (API)                 KITCHEN (server + database)
 "One dosa, please" ─► takes the order in a  ─────►  cooks it
                       fixed format
 gets the dosa     ◄── brings back the plate ◄─────  puts it on a plate
```

- You never walk into the kitchen. You only talk to the **waiter**, using the **menu** (the list of things you are allowed to ask for).
- The API is the waiter. The **menu** is the **API documentation**.
- Any customer can use the same waiter: the Android app, the iPhone app and the website all call **the same API**.

### Why APIs are so important today

- **One backend, many frontends.** Write your business rules once; web, mobile and partner apps all use them.
- **Teams work separately.** The frontend team and the backend team only need to agree on the API.
- **Companies connect.** Payments (Razorpay, Stripe), maps, weather, login with Google — all are APIs.
- **AI uses APIs.** When you call an AI model you call an API, and AI agents use *your* APIs as "tools". This is the heart of this course: *Applied AI and **API Integration***.

### What makes an API "REST"?

**REST** (REpresentational State Transfer) is a **style** — a set of good habits — for designing web APIs. The main ideas:

| REST idea | Simple meaning | Example |
|---|---|---|
| **Resources** | Everything is a "thing" with an address (URL). Use **nouns**, not verbs. | `/api/articles/`, `/api/articles/7/` |
| **HTTP methods are the verbs** | The method says *what to do* with the resource. | `GET /api/articles/7/` = read article 7 |
| **Representations** | The server sends a *representation* of the resource, usually JSON. | `{"id": 7, "title": "..."}` |
| **Stateless** | Every request carries everything needed (e.g. its login token). The server does not "remember" the previous request. | Each request sends `Authorization: Bearer ...` |
| **Status codes** | The number in the answer tells you what happened. | `201 Created`, `404 Not Found` |

Bad (not REST): `GET /getAllArticles`, `POST /deleteArticle?id=7`
Good (REST): `GET /api/articles/`, `DELETE /api/articles/7/`

### HTTP methods = CRUD

You learned CRUD on Day 2 (Create, Read, Update, Delete). In a REST API each CRUD action has its own method:

| CRUD | HTTP method | URL | Meaning | Success code |
|---|---|---|---|---|
| **C**reate | `POST` | `/api/articles/` | Add a new article | `201 Created` |
| **R**ead (all) | `GET` | `/api/articles/` | List articles | `200 OK` |
| **R**ead (one) | `GET` | `/api/articles/7/` | Show article 7 | `200 OK` |
| **U**pdate (all fields) | `PUT` | `/api/articles/7/` | Replace article 7 completely | `200 OK` |
| **U**pdate (some fields) | `PATCH` | `/api/articles/7/` | Change only some fields of article 7 | `200 OK` |
| **D**elete | `DELETE` | `/api/articles/7/` | Remove article 7 | `204 No Content` |

Notice the pattern: **two URLs** per resource — the **collection** (`/articles/`) and **one item** (`/articles/7/`).

### JSON in 1 minute

**JSON** (JavaScript Object Notation) looks almost exactly like a Python dictionary:

```json
{
  "id": 7,
  "title": "Learn REST",
  "is_published": true,
  "categories": [1, 3],
  "author": null
}
```

| JSON | Python |
|---|---|
| `{ }` object | `dict` |
| `[ ]` array | `list` |
| `"text"` (always **double** quotes) | `str` |
| `7`, `3.5` | `int`, `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

### Status codes you will see today

| Code | Name | When |
|---|---|---|
| `200` | OK | Read or update worked |
| `201` | Created | A new item was created (after `POST`) |
| `204` | No Content | Delete worked (nothing to send back) |
| `400` | Bad Request | Your data is wrong (DRF) — e.g. title too short |
| `401` | Unauthorized | "Who are you?" — no login token, or a wrong one |
| `403` | Forbidden | "I know who you are, but you are not allowed" |
| `404` | Not Found | That item does not exist (or you may not see it) |
| `405` | Method Not Allowed | e.g. `DELETE` on a URL that does not allow it |
| `422` | Unprocessable Content | Your data is wrong (FastAPI) |
| `500` | Internal Server Error | A bug in the server code |

Easy memory trick: **2xx** = success, **4xx** = *you* (the client) made a mistake, **5xx** = *the server* made a mistake.

More: [references/HTTP_STATUS_CODES.md](references/HTTP_STATUS_CODES.md)

---

## Do it now

You will call real public practice APIs with only your browser.

### Step 1 — Read one item

Open this address in Chrome or Edge:

**https://jsonplaceholder.typicode.com/posts/1**

You see JSON, not a web page:

```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident ...",
  "body": "quia et suscipit ..."
}
```

> Tip: Chrome and Edge have a **"Pretty-print"** checkbox at the top. Tick it to see the JSON nicely indented.

### Step 2 — Read the whole collection

Open **https://jsonplaceholder.typicode.com/posts**

Now you get a JSON **array** `[ ... ]` with 100 posts. Same resource name, no id → the **collection**.

### Step 3 — Filter with a query parameter

Open **https://jsonplaceholder.typicode.com/posts?userId=2**

Only the posts of user 2. The part after `?` is a **query parameter**. It filters or changes the list — it does not choose a different resource.

### Step 4 — Look at the request and response in DevTools

1. Press **F12** → open the **Network** tab.
2. Reload the page (**F5**).
3. Click the request named `posts?userId=2`.
4. Look at **Headers**:
   - **Request Method:** `GET`
   - **Status Code:** `200 OK`
   - **Response Headers → content-type:** `application/json; charset=utf-8`

That `content-type` header is how a program knows "this answer is JSON".

### Step 5 — Ask for something that does not exist

Open **https://jsonplaceholder.typicode.com/posts/99999**

You get `{}` and in the Network tab: **Status Code `404 Not Found`**.

### Step 6 — A real company API

Open **https://api.github.com/users/octocat**

This is GitHub's real REST API — the same one many tools use. Find these keys in the JSON: `login`, `public_repos`, `created_at`.

---

## Check

- [ ] I saw one post as JSON (Step 1) and a list of posts (Step 2).
- [ ] I saw the method **GET**, status **200** and content-type **application/json** in DevTools.
- [ ] I saw a **404** for a post that does not exist.
- [ ] I can say which HTTP method creates, reads, updates and deletes.

---

## What just happened?

```text
Browser ── GET /posts/1 ─────────────────────► jsonplaceholder server
                                                  │ finds post 1 in its database
Browser ◄── 200 OK + content-type: application/json + {"id": 1, ...}
```

- A browser can only easily send **GET** requests from the address bar. To send `POST`, `PUT`, `PATCH` and `DELETE` with a JSON body, you need a tool → **Postman** (installed in Lesson 02) or code.
- `/posts` is the collection; `/posts/1` is one item — exactly the REST pattern you will build in Lessons 05–06.
- `?userId=2` is a query parameter — you will read query parameters in Django (Lesson 06) and FastAPI (Lesson 11).

### Where do APIs fit with what you know?

```text
                 ┌── Day 2 Django view ──► HTML page  ──► human in a browser
Database ◄─► Django
                 └── Day 3 DRF view   ──► JSON data  ──► React app / mobile app / AI agent / Postman
```

Same models, same database, same ORM. Only the **output format** changes. That is why DRF feels familiar.

---

## Try it yourself

1. Open https://jsonplaceholder.typicode.com/users/3 — what is this user's `email` and their company `name`? (Hint: JSON objects can contain other objects.)
2. Open https://jsonplaceholder.typicode.com/posts/1/comments — this is a **nested resource**: "the comments **of** post 1". How many comments are there?
3. Write down the REST URL **and** method for each of these (for a library app with books):
   - list all books
   - add a new book
   - change only the price of book 12
   - remove book 12
   - show only books by author 5
4. Which status code would you expect for each of the 5 actions above when they work?

Answers are in [practice/ANSWERS.md](practice/ANSWERS.md) (Section A).

---

## If it does not work

| Problem | Fix |
|---|---|
| The JSON is one long ugly line | Tick **Pretty-print** at the top, or install a JSON viewer extension. Firefox formats JSON automatically. |
| I don't see any request in the Network tab | The Network tab must be open **before** you reload. Press **F5** again. |
| The page doesn't load | Check your internet. Some office/school networks block sites — try a mobile hotspot. |
| `api.github.com` says "rate limit exceeded" | GitHub allows 60 requests per hour without login. Wait a while — it is not a problem with your computer. |

---

**Next:** [02_SET_UP_FOR_DAY_3.md](02_SET_UP_FOR_DAY_3.md)
