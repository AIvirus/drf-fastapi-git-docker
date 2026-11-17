# Lesson 07 — Authentication, Permissions and Tokens

**Time:** 45 minutes  |  **You need:** Lesson 06 finished

---

## Goal

By the end of this lesson:

- only the **author** can change or delete an article (other users get **403**),
- only **staff** users can create or change categories,
- a new user can **register** through the API,
- a user can **log in with a token** and use it from Postman,
- you will know the difference between **401** and **403**.

---

## Understand

### Two questions, every request

| Question | Name | DRF piece | If the answer is "no" |
|---|---|---|---|
| **Who** are you? | **Authentication** | `authentication_classes` | **401 Unauthorized** — "I don't know who you are" |
| **What** may you do? | **Authorization** | `permission_classes` | **403 Forbidden** — "I know who you are, but no" |

(Yes, the name "401 Unauthorized" is confusing — it really means *unauthenticated*.)

### How does an API know who you are?

On Day 2 the browser had a **session cookie**. That works for browsers, but a mobile app or another server doesn't work well with cookies. APIs usually use a **token** instead:

```text
1. Log in once:   POST /api/auth/token/  {"username": "asha", "password": "..."}
                  ◄── {"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}

2. Every request: GET /api/auth/me/
                  Header →  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
                  ◄── {"username": "asha", ...}
```

A token is like a **cinema ticket**: you show your ID once at the counter (username + password), you get a ticket, and after that you just show the ticket.

### DRF authentication classes

| Class | How the client proves who it is | Good for |
|---|---|---|
| `SessionAuthentication` | Django session cookie (+ CSRF token) | The browsable API, websites on the same domain |
| `BasicAuthentication` | Username + password on **every** request | Quick tests only |
| `TokenAuthentication` | `Authorization: Token <key>` | Simple apps, scripts |
| JWT (`JWTAuthentication`) | `Authorization: Bearer <access token>` | Mobile/SPA apps, many servers — **Lesson 08** |

### DRF permission classes

| Class | Rule |
|---|---|
| `AllowAny` | Everyone, even logged-out |
| `IsAuthenticated` | Only logged-in users |
| `IsAuthenticatedOrReadOnly` | Everyone may read; logged-in users may write |
| `IsAdminUser` | Only users with `is_staff = True` |
| **your own class** | Any rule you like, e.g. "only the author" |

Two levels of permission checks:

- `has_permission(request, view)` — runs for **every** request ("may you use this endpoint at all?").
- `has_object_permission(request, view, obj)` — runs when **one object** is used: retrieve, update, delete ("may you touch *this* article?").

**Safe methods** = `GET`, `HEAD`, `OPTIONS`. They only *read*. DRF has a list: `permissions.SAFE_METHODS`.

---

## Do it now

### Part A — "Only the author can change it"

#### Step 1 — Write your own permission classes

Create **`journal/permissions.py`**:

```python
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Anyone may READ an article; only its author may CHANGE or DELETE it."""

    message = "You can only change your own articles."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Anyone may READ; only staff users may create, change or delete."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
```

#### Step 2 — Use them in the ViewSets

In **`journal/views.py`**:

1. Add the import at the top:
   ```python
   from rest_framework.decorators import action, api_view, permission_classes
   from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
   ```
   (Replace your old `from rest_framework.decorators import ...` line with the first line.)

2. Make `hello` open to everyone, on purpose:
   ```python
   @api_view(["GET"])
   @permission_classes([permissions.AllowAny])
   def hello(request):
       return Response({"message": "Hello from Django REST Framework!"})
   ```

3. Add a `permission_classes` line to each ViewSet:
   ```python
   class CategoryViewSet(viewsets.ModelViewSet):
       queryset = Category.objects.all()
       serializer_class = CategorySerializer
       permission_classes = [IsAdminOrReadOnly]                                   # ADD


   class ArticleViewSet(viewsets.ModelViewSet):
       serializer_class = ArticleSerializer
       permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]  # ADD
       ...
   ```

> **Important:** setting `permission_classes` on a view **replaces** the default from `settings.py` — it doesn't add to it. That's why `ArticleViewSet` lists `IsAuthenticatedOrReadOnly` again: without it, logged-out users could POST.

#### Step 3 — Test it with a second user

1. In the admin (http://127.0.0.1:8000/admin/), add a user **`ravi`** with a password. Do **not** tick "Staff status".
2. Log out of the browsable API and log in as **ravi** (http://127.0.0.1:8000/api-auth/login/).
3. Open the admin's article `/api/articles/1/` and try **PATCH** `{"title": "Ravi was here"}`:
   ```json
   {"detail": "You can only change your own articles."}
   ```
   **HTTP 403 Forbidden.** Your custom message!
4. As ravi, POST a new article to `/api/articles/` → **201**. Ravi *can* edit **this** one.
5. As ravi, POST `{"name": "Hacking"}` to `/api/categories/` → **403**. Only staff can.

---

### Part B — Tokens and a register endpoint

#### Step 4 — Turn on Token authentication

In **`config/settings.py`**:

1. Add `"rest_framework.authtoken",` to `INSTALLED_APPS` (right after `"rest_framework",`).
2. Change `REST_FRAMEWORK` to:
   ```python
   REST_FRAMEWORK = {
       "DEFAULT_AUTHENTICATION_CLASSES": [
           "rest_framework.authentication.TokenAuthentication",
           "rest_framework.authentication.SessionAuthentication",
       ],
       "DEFAULT_PERMISSION_CLASSES": [
           "rest_framework.permissions.IsAuthenticatedOrReadOnly",
       ],
       "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
       "PAGE_SIZE": 10,
   }
   ```

`authtoken` has its own table for tokens, so:

```bash
python manage.py migrate
```

#### Step 5 — Create an `accounts` app for register and "who am I?"

```bash
python manage.py startapp accounts
```

Add `"accounts",` to `INSTALLED_APPS` (after `"journal",`).

Create **`accounts/serializers.py`**:

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # write_only: accepted in requests, NEVER sent back in responses.
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        # create_user() hashes the password. Never save a plain-text password!
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]
```

Replace **`accounts/views.py`**:

```python
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/  -> create a new user account."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    """GET /api/auth/me/  -> who am I? (needs a token)"""
    return Response(UserSerializer(request.user).data)
```

Create **`accounts/urls.py`**:

```python
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("me/", views.me, name="me"),
    path("token/", obtain_auth_token, name="token"),   # username + password -> token
]
```

And add one line to **`config/urls.py`**:

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("journal.urls")),
    path("api/auth/", include("accounts.urls")),        # ADD
    path("api-auth/", include("rest_framework.urls")),
]
```

#### Step 6 — The whole flow in Postman

Run the server. In Postman:

**1. Register** — `POST http://127.0.0.1:8000/api/auth/register/`, Body → raw → JSON:
```json
{"username": "asha", "email": "asha@example.com", "password": "Learning-APIs-2026"}
```
→ **201 Created**: `{"id": 3, "username": "asha", "email": "asha@example.com"}` — **no password** in the answer.

Try a weak password like `"123"` → **400** with Django's password rules (too short, too common, entirely numeric).

**2. Get a token** — `POST http://127.0.0.1:8000/api/auth/token/`:
```json
{"username": "asha", "password": "Learning-APIs-2026"}
```
→ **200**: `{"token": "a1b2c3..."}` — **copy the token**.

**3. Who am I, without the token?** — `GET http://127.0.0.1:8000/api/auth/me/`
→ **401 Unauthorized**: `{"detail": "Authentication credentials were not provided."}`

**4. Who am I, with the token?**
- Open the **Headers** tab of the request.
- Add a row: Key = `Authorization`, Value = `Token a1b2c3...` (the word **Token**, one space, your token).
- **Send** → **200**: `{"id": 3, "username": "asha", "email": "asha@example.com", "is_staff": false}`

**5. Create an article as asha** — `POST http://127.0.0.1:8000/api/articles/` with the same `Authorization` header and body:
```json
{"title": "Written with a token", "body": "Postman sent this with my API token.", "is_published": true}
```
→ **201**, `"author": "asha"`.

**6. Try to change the admin's article as asha** — `PATCH http://127.0.0.1:8000/api/articles/1/`, same header, body `{"title": "Hacked"}` → **403**.

**7. Same PATCH without the header** → **401**.

---

## Check

- [ ] Another user gets **403** when changing an article that isn't theirs.
- [ ] A normal user gets **403** when creating a category; staff can.
- [ ] `POST /api/auth/register/` → **201**, and the password is **not** in the response.
- [ ] `POST /api/auth/token/` gives a token.
- [ ] `GET /api/auth/me/` → **401** without the token, **200** with it.
- [ ] I can explain the difference between 401 and 403.

---

## What just happened?

### The order DRF checks things

```text
Request arrives
  │
  ├─ 1. AUTHENTICATION  — try each class in DEFAULT_AUTHENTICATION_CLASSES:
  │       TokenAuthentication: is there "Authorization: Token ..."? → find the user
  │       SessionAuthentication: is there a session cookie? → find the user
  │       nothing found → request.user = AnonymousUser
  │
  ├─ 2. has_permission()  — for every permission class, e.g. IsAuthenticatedOrReadOnly
  │       fails → 401 (not logged in) or 403 (logged in but not allowed)
  │
  ├─ 3. get_object()  → uses get_queryset() → 404 if not found
  │
  ├─ 4. has_object_permission() — e.g. IsAuthorOrReadOnly → 403 if not the author
  │
  └─ 5. the action runs (list / create / update / ...)
```

### Where are the tokens?

Open the admin → **Auth Token → Tokens**. Each user has **one** token, stored in the database. That's simple, but:

- The token **never expires** — if someone steals it, it works forever (until you delete it in the admin).
- Every request needs a **database lookup** to find the token.

JWT (next lesson) fixes both.

### Why was the register password safe?

- `write_only=True` → accepted in input, never in output.
- `validators=[validate_password]` → the same password rules as Django's admin.
- `create_user()` → **hashes** the password (you saw this on Day 2). Never use `User.objects.create(password=...)` — that would store it in plain text and login would not work.

### Why does the browsable API still work?

`SessionAuthentication` is still in the list. The browser sends its session cookie. DRF also checks the **CSRF** token for session logins (the browsable API handles it for you). Token requests don't need CSRF because a malicious website can't add your `Authorization` header.

### 401 or 403 when not logged in?

DRF answers **401** only if the **first** authentication class can tell the client *how* to log in (it sends a `WWW-Authenticate: Token` header). `TokenAuthentication` can; `SessionAuthentication` can't. That's why in Lesson 05 (session only) a logged-out POST got **403**, and now it gets **401**.

---

## Try it yourself

1. In the `ArticleViewSet` from Lesson 06's bonus, your `publish` action (if you made it) — check that ravi **cannot** publish the admin's article. (`self.get_object()` runs `has_object_permission` for you.)
2. Make an **admin-only** endpoint `GET /api/auth/users/` that lists all users with `UserSerializer`. Use `generics.ListAPIView` and `permission_classes = [permissions.IsAdminUser]`. Test with asha's token (**403**) and the admin's token (**200**).
3. "Log out" a token: in the admin, delete asha's token. Send `GET /api/auth/me/` with the old token → `{"detail": "Invalid token."}` **401**. Get a new token with step 2.
4. Change `IsAuthorOrReadOnly` so that **staff users** may also edit any article.

---

## If it does not work

| Error | Fix |
|---|---|
| `no such table: authtoken_token` | Add `"rest_framework.authtoken"` to `INSTALLED_APPS`, then `python manage.py migrate`. |
| `{"detail": "Authentication credentials were not provided."}` with the header | Check the header **name** `Authorization` and the value format `Token <key>` — the word `Token`, **one space**, the key. No quotes. |
| `{"detail": "Invalid token."}` | You copied the token with a missing character, or the token was deleted. Get a new one. |
| `{"non_field_errors": ["Unable to log in with provided credentials."]}` | Wrong username or password in `/api/auth/token/`. |
| Register: `{"username": ["A user with that username already exists."]}` | Choose another username. |
| Ravi **can** edit the admin's article | `permission_classes` is missing on `ArticleViewSet`, or the class name is misspelled. Restart the server. |
| Logged-out users can POST articles now | You set `permission_classes = [IsAuthorOrReadOnly]` **alone**. Add `permissions.IsAuthenticatedOrReadOnly` too. |
| `CSRF Failed: CSRF token missing` in Postman | Postman is sending a **session cookie** (you logged in through the browser part of Postman). Use the token header, or delete the cookies in Postman (**Cookies** link under **Send**). |

Compare with: [drf_lab/journal/permissions.py](drf_lab/journal/permissions.py), [drf_lab/accounts/](drf_lab/accounts/), [drf_lab/config/settings.py](drf_lab/config/settings.py).

---

**Next:** [08_JWT_AUTHENTICATION.md](08_JWT_AUTHENTICATION.md)
