# `drf_lab` — The Finished Journal API (Answer Key for Lessons 03–09)

This folder is the **finished** Django REST Framework project — what you build yourself in Lessons 03–09 inside `my_api/`.

Use it to:

- **compare** — if a file in your `my_api` doesn't work, open the same file here (e.g. `my_api/journal/views.py` ↔ `drf_lab/journal/views.py`);
- **preview** — run it to see what you are going to build.

> Learning tip: don't copy this whole folder. You learn by typing the code in the lessons.

---

## Run it (about 5 minutes)

You need **Lesson 02 done** (`.venv` created, packages installed). No database account needed — it uses **SQLite**.

```bash
cd drf_lab
```
```bash
python manage.py makemigrations journal
```
```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```
```bash
python manage.py runserver
```

> Migration files are not included on purpose — `makemigrations` creates them from the models.

Optional: copy `.env.example` to `.env` to set your own `DJANGO_SECRET_KEY`, or a `DATABASE_URL` for PostgreSQL (e.g. your Neon database from Day 2).

## Endpoints

| Method | URL | Who | What |
|---|---|---|---|
| GET | `/api/` | anyone | API root (links) |
| GET | `/api/hello/` | anyone | Hello message |
| GET | `/api/articles/` | anyone | Published articles (+ your own drafts when logged in). `?search=`, `?ordering=`, `?category=`, `?page=` |
| POST | `/api/articles/` | logged in | Create (you become the author) |
| GET | `/api/articles/<id>/` | anyone* | One article (*drafts: only the author) |
| PUT / PATCH / DELETE | `/api/articles/<id>/` | the author | Change / delete |
| GET | `/api/articles/mine/` | logged in | Only my articles |
| GET | `/api/categories/` and `/api/categories/<id>/` | anyone | Read categories |
| POST / PUT / PATCH / DELETE | `/api/categories/...` | staff | Manage categories |
| POST | `/api/auth/register/` | anyone | Create an account |
| POST | `/api/auth/token/` | anyone | Username + password → simple token |
| POST | `/api/auth/jwt/` | anyone | Username + password → JWT `access` + `refresh` |
| POST | `/api/auth/jwt/refresh/` | anyone | `refresh` → new `access` |
| GET | `/api/auth/me/` | logged in | Who am I? |
| — | `/admin/` | staff | Django admin |
| — | `/api-auth/login/` | — | Log in to the browsable API |

Headers:
- simple token: `Authorization: Token <token>`
- JWT: `Authorization: Bearer <access>`

Try everything at once with the Postman collection: [../postman/Day03_Journal_API.postman_collection.json](../postman/Day03_Journal_API.postman_collection.json) (Lesson 09, Part B).

## Run the tests

```bash
python manage.py test
```

`Ran 21 tests ... OK`

---

## Which lesson built which file?

| File | Lesson |
|---|---|
| `config/settings.py` — `INSTALLED_APPS` (`rest_framework`) | 03 |
| `config/settings.py` — `REST_FRAMEWORK` permissions, pagination | 05, 06 |
| `config/settings.py` — authentication classes, `authtoken` | 07 |
| `config/settings.py` — `SIMPLE_JWT` | 08 |
| `config/urls.py` | 03, 07 |
| `journal/models.py`, `journal/admin.py` | 04 |
| `journal/serializers.py` | 04 |
| `journal/views.py` — `hello` | 03 |
| `journal/views.py` — `CategoryViewSet`, `ArticleViewSet` | 05 → 06 (+ permissions in 07) |
| `journal/urls.py` — router | 06 |
| `journal/permissions.py` | 07 |
| `accounts/serializers.py`, `accounts/views.py` | 07 |
| `accounts/urls.py` | 07, 08 |
| `journal/tests.py`, `accounts/tests.py` | 09 |

## Differences from what you typed

- `settings.py` reads optional values from `.env` (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DATABASE_URL`) with safe defaults for your laptop. Your `my_api` keeps the key that `startproject` generated — both are fine for learning, but **never** deploy with a key that is written in the code.

## Safety

Never commit `.env`. This setup (`DEBUG=True`, SQLite, fallback secret key) is for learning on your own computer, not for a real server.
