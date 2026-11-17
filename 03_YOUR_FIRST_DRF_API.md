# Lesson 03 — Your First API with Django REST Framework

**Time:** 25 minutes  |  **You need:** Lesson 02 finished

---

## Goal

By the end of this lesson:

- you will have a new Django project called **`my_api`** with Django REST Framework installed,
- http://127.0.0.1:8000/api/hello/ will return **JSON**,
- you will have seen DRF's **browsable API** and called your own API from **Postman**.

---

## Understand

### What is Django REST Framework?

Plain Django *can* return JSON (`JsonResponse`), but you would have to write a lot by hand: turn models into dictionaries, read and validate JSON input, check tokens, return the right status codes, paginate…

**Django REST Framework (DRF)** is a popular add-on that does all that for you. It adds:

| DRF piece | Job | Lesson |
|---|---|---|
| `Response` + `@api_view` | Return JSON from a view | 03 |
| **Serializers** | Model ⇄ JSON, plus validation (like Django forms, but for JSON) | 04 |
| **API views / generic views / ViewSets** | Ready-made CRUD logic | 05, 06 |
| **Routers** | Write the URL patterns for you | 06 |
| **Authentication + permissions** | Who are you? What may you do? | 07, 08 |
| **Browsable API** | A free web page to try your API in the browser | 03 → |

It is used by companies such as Mozilla, Red Hat and many startups. If you know Django, DRF is the fastest way to build an API.

### Same Django, different output

```text
Day 2:  URL ─► view ─► render(template)  ─► HTML
Day 3:  URL ─► view ─► Response(data)    ─► JSON
```

Everything else — `manage.py`, apps, `settings.py`, `urls.py`, models, admin, migrations — works **exactly** like Day 2.

---

## Do it now

> Terminal check: `(.venv)` at the start, `Day-03>` at the end.

### Step 1 — Create the project folder and the project

```bash
mkdir my_api
```
```bash
cd my_api
```
```bash
django-admin startproject config .
```

> Don't forget the **dot** at the end. It means "create the project **here**", so `manage.py` sits directly in `my_api/`.

### Step 2 — Create the `journal` app

```bash
python manage.py startapp journal
```

### Step 3 — Tell Django about DRF and your app

Open **`config/settings.py`**. Find `INSTALLED_APPS` and add two lines at the end:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",               # ADD: Django REST Framework
    "journal",                      # ADD: our app
]
```

Save.

> Notice: the package you installed is called `djangorestframework`, but in Python its name is **`rest_framework`**.

### Step 4 — Write your first API view

Open **`journal/views.py`**. Delete everything and type:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello from Django REST Framework!"})
```

Save.

### Step 5 — Create the app's URL file

Create a new file **`journal/urls.py`**:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("hello/", views.hello, name="hello"),
]
```

### Step 6 — Connect it to the project

Open **`config/urls.py`**. Delete everything and type:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("journal.urls")),
    path("api-auth/", include("rest_framework.urls")),  # adds "Log in" to the browsable API
]
```

Save.

> **Why `api/` at the start?** It's a common habit: every API address starts with `/api/`. That keeps API URLs separate from normal web pages and the admin.

### Step 7 — Create the database tables and run the server

Django still needs its built-in tables (users, sessions…). Today we use **SQLite** — a database in one file (`db.sqlite3`) that needs no setup.

```bash
python manage.py migrate
```
```bash
python manage.py runserver
```

### Step 8 — Look at your API in the browser

Open **http://127.0.0.1:8000/api/hello/**

You see DRF's **browsable API**: a page with the title **Hello**, a grey **`GET /api/hello/`** box, and your data:

```text
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "Hello from Django REST Framework!"
}
```

Now open **http://127.0.0.1:8000/api/hello/?format=json** → you see only the raw JSON — exactly what a program receives.

### Step 9 — Call it from Postman

1. In Postman: **GET** `http://127.0.0.1:8000/api/hello/` → **Send**.
2. You get `{"message": "Hello from Django REST Framework!"}` and **200 OK**.
3. Click the **Headers** tab of the *response* → `Content-Type: application/json`.

> The server must keep running in the terminal while you use the browser or Postman. To type other commands, open a **second terminal** (the **+** icon in the terminal panel) and activate `.venv` there.

### Step 10 — Try a method that is not allowed

In Postman change **GET** to **POST** and **Send**:

```json
{
    "detail": "Method \"POST\" not allowed."
}
```

Status: **405 Method Not Allowed**. You only allowed `["GET"]` in `@api_view`.

---

## Check

- [ ] http://127.0.0.1:8000/api/hello/ shows the browsable API page with your message.
- [ ] `?format=json` shows only JSON.
- [ ] Postman GET → **200 OK**; Postman POST → **405 Method Not Allowed**.

---

## What just happened?

```text
1. Postman:          GET http://127.0.0.1:8000/api/hello/
2. config/urls.py:   "api/"   → include("journal.urls")
3. journal/urls.py:  "hello/" → views.hello
4. @api_view(["GET"]):  is the method allowed?  GET → yes. POST → 405.
5. hello() returns Response({...})   ← a Python dictionary
6. DRF turns the dictionary into JSON (or the HTML browsable page) and sends it.
```

### Why did the browser get HTML but Postman got JSON?

This is called **content negotiation**. Every request says which formats it accepts in the **`Accept`** header:

- A browser says: *"I prefer `text/html`."* → DRF sends the **browsable API** page (the JSON is inside it).
- Postman / programs say: *"anything / `application/json`."* → DRF sends **pure JSON**.
- `?format=json` forces JSON.

**`Response` vs Day 2's `HttpResponse`:**

| `HttpResponse("text")` (Day 2) | `Response({...})` (DRF) |
|---|---|
| You give it finished text/HTML | You give it **Python data** (dict, list) |
| Always the same output | DRF picks JSON or browsable HTML automatically |

**`@api_view(["GET"])`** turns a normal Django function into a DRF view: it allows only the listed methods, gives you DRF's improved `request` object, and catches errors to return them as JSON.

---

## Try it yourself

1. Add a second endpoint **`/api/about/`** that returns:
   ```json
   {"course": "Applied AI and API Integration", "day": 3, "topics": ["DRF", "FastAPI", "Git", "Docker"]}
   ```
   Check it in the browser and in Postman. Notice how the Python list became a JSON array.

2. Make `hello` say hello to a name from a **query parameter**: `/api/hello/?name=Asha` → `{"message": "Hello, Asha!"}`. Without `?name=` it should still say `Hello from Django REST Framework!`.

   Hint:
   ```python
   name = request.query_params.get("name")
   ```
   (`request.query_params` is DRF's nicer name for Day 2's `request.GET`.)

3. Allow `POST` too: `@api_view(["GET", "POST"])`. For POST, return whatever JSON was sent: `return Response({"you_sent": request.data})`. Test it in Postman with **Body → raw → JSON**. (`request.data` is the JSON body, already turned into a Python dict.)

---

## If it does not work

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'rest_framework'` | `.venv` not active, or packages not installed (Lesson 02, Step 4). |
| `TemplateDoesNotExist: rest_framework/api.html` | You forgot `"rest_framework"` in `INSTALLED_APPS` (Step 3). |
| 404 "Page not found" for `/api/hello/` | Check both URL files. The full address is `api/` + `hello/`. Did you save all files? |
| `AssertionError: .accepted_renderer not set on Response` | You forgot `@api_view([...])` above the function. |
| `django-admin` not recognized | Use `python -m django startproject config .` |
| Postman: "Could not send request" / `ECONNREFUSED` | The server is not running. Start it with `python manage.py runserver` and keep that terminal open. |
| Postman says "Cloud Agent" / can't reach localhost | In the web version of Postman, local addresses need the **Desktop Agent**. Use the **desktop app** instead. |

Compare with the answer key: [drf_lab/journal/views.py](drf_lab/journal/views.py) (look at the `hello` function) and [drf_lab/config/urls.py](drf_lab/config/urls.py).

---

**Next:** [04_MODELS_AND_SERIALIZERS.md](04_MODELS_AND_SERIALIZERS.md)
