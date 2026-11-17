# Lesson 08 — JWT Authentication (Access + Refresh Tokens)

**Time:** 25 minutes  |  **You need:** Lesson 07 finished

---

## Goal

By the end of this lesson:

- users can log in and receive a **JWT access token** and a **refresh token**,
- you will send the access token as a **Bearer** token from Postman,
- you will look **inside** a JWT,
- you will see a token **expire** and get a new one with the refresh token.

---

## Understand

### The problem with simple tokens (Lesson 07)

| Simple DRF token | Problem |
|---|---|
| Stored in the database | Every request needs a database lookup |
| Never expires | A stolen token works forever |
| Only works with this one server's database | Hard to share login between several services |

### What is a JWT?

A **JWT** (JSON Web Token, say *"jot"*) is a token that **carries its own information** and is **signed** by the server.

It has three parts separated by dots:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 . eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjox... . 3kP9xQ2...
└──────────── HEADER ───────────────┘   └──────────────── PAYLOAD ────────────────┘   └ SIGNATURE ┘
 {"alg": "HS256", "typ": "JWT"}           {"token_type": "access",                     made with the
                                           "user_id": "3",                              server's SECRET_KEY
                                           "exp": 1794931841, ...}
```

- **Header** — which signing method is used.
- **Payload** — the "claims": who the user is (`user_id`) and when the token expires (`exp`).
- **Signature** — proves the server made this token and nobody changed it.

When a request arrives, the server **re-calculates the signature** with its `SECRET_KEY`. If it matches and `exp` is in the future → the user is authenticated. **No database lookup for the token.**

> ⚠ The payload is only **encoded** (base64), **not encrypted**. Anyone who has the token can read it. **Never put secrets** (passwords, card numbers) in a JWT.

### Access token + refresh token

| | Access token | Refresh token |
|---|---|---|
| Used for | Every API request (`Authorization: Bearer ...`) | Only to get a **new** access token |
| Lifetime (our settings) | **30 minutes** | **1 day** |
| If stolen | Works only until it expires (short!) | Must be kept extra safe |

```text
1. POST /api/auth/jwt/          {"username", "password"}   ──► {"access": "...", "refresh": "..."}
2. GET  /api/articles/mine/     Authorization: Bearer <access>  ──► 200
   ... 30 minutes later ...
3. GET  /api/articles/mine/     Authorization: Bearer <access>  ──► 401 "Token is expired"
4. POST /api/auth/jwt/refresh/  {"refresh": "..."}         ──► {"access": "<new access>"}
5. GET  /api/articles/mine/     Authorization: Bearer <new access> ──► 200
```

The user typed their password **once**. Apps do steps 3–5 automatically in the background.

---

## Do it now

`djangorestframework-simplejwt` is already installed (Lesson 02).

### Step 1 — Add JWT to the settings

In **`config/settings.py`**:

1. At the **top**, add:
   ```python
   from datetime import timedelta
   ```

2. Put JWT **first** in the authentication classes:
   ```python
   REST_FRAMEWORK = {
       "DEFAULT_AUTHENTICATION_CLASSES": [
           "rest_framework_simplejwt.authentication.JWTAuthentication",   # ADD (first)
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

3. At the **bottom**, add the token lifetimes:
   ```python
   SIMPLE_JWT = {
       "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
       "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
   }
   ```

### Step 2 — Add the JWT URLs

In **`accounts/urls.py`**:

```python
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("me/", views.me, name="me"),
    path("token/", obtain_auth_token, name="token"),
    path("jwt/", TokenObtainPairView.as_view(), name="jwt_obtain"),            # ADD
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),      # ADD
]
```

No `migrate` needed — JWTs are **not** stored in the database.

### Step 3 — Log in and get a JWT pair (Postman)

`POST http://127.0.0.1:8000/api/auth/jwt/`, Body → raw → JSON:

```json
{"username": "asha", "password": "Learning-APIs-2026"}
```

→ **200 OK**:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIs...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwi..."
}
```

Wrong password → **401** `{"detail": "No active account found with the given credentials"}`.

### Step 4 — Use the access token

`GET http://127.0.0.1:8000/api/auth/me/`

This time use Postman's **Authorization** tab (easier than typing the header):

1. **Authorization** tab → **Auth Type**: **Bearer Token**.
2. Paste the **access** token (not the refresh token) into **Token**.
3. **Send** → **200** with your user.

Click the **Headers** tab: Postman added `Authorization: Bearer eyJhbGci...` for you. (Remove any old `Authorization: Token ...` row from Lesson 07 first, or it will be confusing.)

Now create an article with the Bearer token — `POST /api/articles/` — it works just like the simple token.

### Step 5 — Look inside your token

Copy your **access** token and run this in a terminal (with `.venv` active). Replace `PASTE_TOKEN_HERE`:

```bash
python -c "import base64, json, sys; p = sys.argv[1].split('.')[1]; p += '=' * (-len(p) % 4); print(json.dumps(json.loads(base64.urlsafe_b64decode(p)), indent=2))" PASTE_TOKEN_HERE
```

```json
{
  "token_type": "access",
  "exp": 1794931841,
  "iat": 1794930041,
  "jti": "ebfb2bb5c8eb4d7abe3d91a2234ac221",
  "user_id": "3"
}
```

| Claim | Meaning |
|---|---|
| `token_type` | `access` or `refresh` |
| `exp` | **exp**ires at (seconds since 1 Jan 1970) |
| `iat` | **i**ssued **at** |
| `jti` | a unique id for this token |
| `user_id` | which user this token belongs to |

`exp - iat = 1800` seconds = **30 minutes**. Anyone can read this — but nobody can **change** it without breaking the signature.

> You may see websites like jwt.io that decode tokens. That's fine for practice tokens on your laptop, but **never paste a real production token into a website**.

### Step 6 — Watch a token expire

1. In `settings.py` change `"ACCESS_TOKEN_LIFETIME": timedelta(minutes=30)` to `timedelta(minutes=1)`. Save (the server restarts).
2. Get a new pair (Step 3). Use the access token on `/api/auth/me/` → **200**.
3. Wait **one minute**, send again → **401**:
   ```json
   {
       "detail": "Given token not valid for any token type",
       "code": "token_not_valid",
       "messages": [{"token_class": "AccessToken", "token_type": "access", "message": "Token is expired"}]
   }
   ```
4. Get a new access token **without the password**: `POST http://127.0.0.1:8000/api/auth/jwt/refresh/`, Authorization tab → **No Auth**, body:
   ```json
   {"refresh": "PASTE_YOUR_REFRESH_TOKEN"}
   ```
   → **200** `{"access": "eyJ..."}`
5. Use the new access token → **200** again.
6. **Change the lifetime back to 30 minutes.**

### Step 7 — Try to cheat

Take your access token and change **one letter** in the middle part (the payload). Send it → **401** `"Token is invalid"`. The signature no longer matches, so the server refuses it. That's why a JWT can't be faked without the `SECRET_KEY`.

---

## Check

- [ ] `POST /api/auth/jwt/` returns `access` and `refresh`.
- [ ] `Authorization: Bearer <access>` works on `/api/auth/me/` and for creating articles.
- [ ] I decoded my token and found `user_id` and `exp`.
- [ ] An expired access token → **401**; the refresh endpoint gave me a new one.
- [ ] A changed token → **401** "Token is invalid".
- [ ] `ACCESS_TOKEN_LIFETIME` is back to 30 minutes.

---

## What just happened?

### Simple Token vs JWT

| | DRF Token (Lesson 07) | JWT (this lesson) |
|---|---|---|
| Header | `Authorization: Token <key>` | `Authorization: Bearer <access>` |
| Stored in the database? | Yes | **No** (self-contained, signed) |
| Expires? | No | Yes (access: minutes, refresh: days) |
| "Log out" | Delete the token row | Wait for expiry, or use a **blacklist** (simplejwt has one) |
| Can other services check it? | Only with access to the database | Yes — anyone with the signing key |
| Good for | Scripts, small internal tools | Mobile apps, React/Vue apps, many services |

### Why keep three authentication classes?

DRF tries them **in order**. The first one that recognises the request wins:
- `Bearer ...` → **JWTAuthentication**
- `Token ...` → **TokenAuthentication**
- session cookie → **SessionAuthentication** (so the browsable API still works)

In a real project you'd usually pick **one** token style. We keep both today so you can compare.

### Why is `SECRET_KEY` now even more important?

JWTs are signed with your `SECRET_KEY`. If it leaks, **anyone can create a valid token for any user**. That's why it must come from `.env` on a real server (Day 2, Lesson 06), never from code on GitHub.

---

## Try it yourself

1. Use the **refresh** token as if it were an access token (Bearer) on `/api/auth/me/`. What does the error message say? Why is that a good thing?
2. Add your own information to the token. Create **`accounts/tokens.py`**:
   ```python
   from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
   from rest_framework_simplejwt.views import TokenObtainPairView


   class MyTokenSerializer(TokenObtainPairSerializer):
       @classmethod
       def get_token(cls, user):
           token = super().get_token(user)
           token["username"] = user.username   # extra claim
           return token


   class MyTokenView(TokenObtainPairView):
       serializer_class = MyTokenSerializer
   ```
   Use `MyTokenView.as_view()` instead of `TokenObtainPairView.as_view()` in `accounts/urls.py`. Decode a new token — is `username` inside?
3. Read about **refresh token rotation** and the **blacklist** app in the SimpleJWT docs: https://django-rest-framework-simplejwt.readthedocs.io/

---

## If it does not work

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'rest_framework_simplejwt'` | `pip install -r requirements.txt` with `.venv` active. |
| `"Authentication credentials were not provided."` | Postman: Authorization tab must be **Bearer Token**, and the token must be the **access** one. The header is `Bearer <token>` — **Bearer**, not `Token`. |
| `"Token is invalid"` | Not the whole token was copied (it is long!), or you used the refresh token, or you changed `SECRET_KEY` after creating it. Get a new pair. |
| `"Token is expired"` | Normal — use `/api/auth/jwt/refresh/` or log in again. |
| `NameError: name 'timedelta' is not defined` | Add `from datetime import timedelta` at the top of `settings.py`. |
| `InsecureKeyLengthWarning` in the terminal | Your `SECRET_KEY` is shorter than 32 characters. Generate a proper one (Day 2, Lesson 06). |
| Refresh endpoint → 401 `token_not_valid` | You sent the **access** token instead of the refresh token, or the refresh token itself has expired (1 day). Send the **refresh** token in the **body**; if it expired, log in again (Step 3). |

Compare with: [drf_lab/config/settings.py](drf_lab/config/settings.py), [drf_lab/accounts/urls.py](drf_lab/accounts/urls.py).

---

**Next:** [09_TEST_YOUR_API_WITH_POSTMAN.md](09_TEST_YOUR_API_WITH_POSTMAN.md)
