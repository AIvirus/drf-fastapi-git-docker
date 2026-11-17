# Lesson 05 — API Views: Function, Class and Generic

**Time:** 45 minutes  |  **You need:** Lesson 04 finished

---

## Goal

By the end of this lesson your API will do full **CRUD** on articles:

| Method | URL | Does |
|---|---|---|
| `GET` | `/api/articles/` | list articles |
| `POST` | `/api/articles/` | create an article |
| `GET` | `/api/articles/<id>/` | show one article |
| `PUT` / `PATCH` | `/api/articles/<id>/` | change an article |
| `DELETE` | `/api/articles/<id>/` | delete an article |

You will write it **three times**, each shorter than the last, so you understand what DRF does for you:

1. **Function-based views** with `@api_view` — everything by hand.
2. **Class-based views** with `APIView` — one method per HTTP verb.
3. **Generic views** — DRF writes the code; you just configure it.

---

## Understand

### The two URLs of a resource

```text
/api/articles/        ← the COLLECTION   → GET (list), POST (create)
/api/articles/7/      ← ONE ITEM         → GET (show), PUT, PATCH (change), DELETE
```

So we need **two views**: one for the collection, one for a single item.

### Before we start: who may write?

Creating an article needs an **author** — a logged-in user. Add this to the **bottom** of **`config/settings.py`**:

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}
```

It means: **anyone may read (GET); only logged-in users may write (POST, PUT, PATCH, DELETE)**. Lesson 07 explains permissions properly. For now you'll log in through the browsable API with your admin user.

---

## Do it now

### Version 1 — Function-based views (`@api_view`)

Open **`journal/views.py`**. Keep the `hello` view and add the new code, so the whole file is:

```python
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello from Django REST Framework!"})


@api_view(["GET", "POST"])
def article_list(request):
    if request.method == "GET":
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    # POST: create a new article from the JSON body
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)        # the author = the logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)     # 404 if it does not exist

    if request.method == "GET":
        return Response(ArticleSerializer(article).data)

    if request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT = send ALL fields. PATCH = send only the fields you want to change.
    partial = request.method == "PATCH"
    serializer = ArticleSerializer(article, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Update **`journal/urls.py`**:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("hello/", views.hello, name="hello"),
    path("articles/", views.article_list, name="article-list"),
    path("articles/<int:pk>/", views.article_detail, name="article-detail"),
]
```

Run the server and try it:

1. Open http://127.0.0.1:8000/api/articles/ → a JSON **list** of all your articles.
2. Open http://127.0.0.1:8000/api/articles/1/ → **one** article.
3. Open http://127.0.0.1:8000/api/articles/999/ → **404** `{"detail": "No Article matches the given query."}`
4. Scroll down on `/api/articles/`. There is **no form** to POST yet — because you are not logged in. Click **Log in** (top right), log in with your admin user, and come back.
5. Now there is a **Content** box at the bottom. Paste this and click **POST**:
   ```json
   {"title": "Posted through my API", "body": "This article was created with a POST request.", "categories": [1]}
   ```
   → **HTTP 201 Created**, and `"author": "admin"`.
6. Post `{"title": "Hi", "body": "x"}` → **HTTP 400 Bad Request** with your validation error from Lesson 04.
7. Open `/api/articles/<the new id>/`. At the bottom you have **PUT**, **PATCH** and **DELETE** buttons. Change the title with PATCH: `{"title": "Changed with PATCH"}`. Then **DELETE** it → **204 No Content**.

You just built a full CRUD API by hand. Now let's make it shorter.

---

### Version 2 — Class-based views (`APIView`)

Same logic, but each HTTP method gets its **own Python method** — no more `if request.method == ...`.

Replace **`journal/views.py`** with:

```python
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello from Django REST Framework!"})


class ArticleList(APIView):
    def get(self, request):
        articles = Article.objects.all()
        return Response(ArticleSerializer(articles, many=True).data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   # sends 400 + errors automatically
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetail(APIView):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        return Response(ArticleSerializer(article).data)

    def put(self, request, pk):
        return self.update(request, pk, partial=False)

    def patch(self, request, pk):
        return self.update(request, pk, partial=True)

    def update(self, request, pk, partial):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

Update the two article lines in **`journal/urls.py`** (class views need `.as_view()`):

```python
    path("articles/", views.ArticleList.as_view(), name="article-list"),
    path("articles/<int:pk>/", views.ArticleDetail.as_view(), name="article-detail"),
```

Test again in the browser: list, detail, POST, PATCH, DELETE. Everything works **exactly** the same.

> `is_valid(raise_exception=True)` — if the data is invalid, DRF stops here and returns **400** with the errors. That saves the `if ... else` you wrote in Version 1.

---

### Version 3 — Generic views

Look at Version 2: almost every API has this **same** code — get objects, serialize, validate, save, 404, 204… DRF already wrote it for you in **generic views**. You only say **which data** and **which serializer**.

Replace the two classes in **`journal/views.py`** so the file is:

```python
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello from Django REST Framework!"})


class ArticleList(generics.ListCreateAPIView):          # GET (list) + POST
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):  # GET + PUT + PATCH + DELETE
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
```

The URLs stay the same. Test everything once more. Same API — **about 15 lines instead of 45**.

---

## Check

- [ ] `GET /api/articles/` lists articles; `GET /api/articles/1/` shows one; `/api/articles/999/` → **404**.
- [ ] Logged in, POST creates an article → **201**, and the author is you.
- [ ] Bad data → **400** with your error message.
- [ ] PATCH changes one field → **200**; DELETE → **204**.
- [ ] Logged **out** (click your name → Log out), the POST form disappears. (A POST from Postman without login → **403** — try it.)
- [ ] Your final `views.py` uses the generic views (Version 3).

---

## What just happened?

### Three ways, same result

| | Function (`@api_view`) | Class (`APIView`) | Generic (`ListCreateAPIView`…) |
|---|---|---|---|
| Lines for CRUD | ~45 | ~40 | ~15 |
| How methods are chosen | `if request.method == "POST"` | `def post(self, request)` | already written by DRF |
| Best for | small special endpoints (`hello`, `me`) | special logic that is not plain CRUD | **normal CRUD on a model** |

### The generic views you can choose from

| Class | Methods |
|---|---|
| `ListAPIView` | GET list |
| `CreateAPIView` | POST |
| `ListCreateAPIView` | GET list + POST |
| `RetrieveAPIView` | GET one |
| `RetrieveUpdateAPIView` | GET one + PUT + PATCH |
| `RetrieveDestroyAPIView` | GET one + DELETE |
| `RetrieveUpdateDestroyAPIView` | GET one + PUT + PATCH + DELETE |

### Hooks: where to put your own logic in generic views

| Method you can override | When it runs | Typical use |
|---|---|---|
| `get_queryset()` | Every request | Show only *some* rows (e.g. only published) |
| `perform_create(serializer)` | On POST, after validation | `serializer.save(author=self.request.user)` |
| `perform_update(serializer)` | On PUT/PATCH | Save who changed it |
| `perform_destroy(instance)` | On DELETE | "Soft delete" instead of real delete |

### PUT vs PATCH

- **PUT** = replace: you must send **all required fields** (`title`, `body`). Missing ones → 400.
- **PATCH** = partial: send **only** what changes, e.g. `{"is_published": true}`. That's `partial=True` in the serializer.

### Two problems we still have (fixed next lessons)

1. **Drafts are visible to everyone** in the list. → Lesson 06 (`get_queryset`).
2. **Any logged-in user can edit or delete anyone's article!** → Lesson 07 (object permissions). Try it: create a second user in the admin, log in as them, and PATCH the admin's article. It works — that's a security bug.

---

## Try it yourself

1. Add two **category** endpoints using generic views: `GET/POST /api/categories/` and `GET/PUT/PATCH/DELETE /api/categories/<id>/`. You need `CategorySerializer` and two new classes + two URL lines.
2. Make `ArticleList` show **only published** articles by changing `queryset` to `Article.objects.filter(is_published=True)`. Open the list — your draft is gone. (Lesson 06 does this better: authors still see their own drafts.)
3. In Postman: send `GET http://127.0.0.1:8000/api/articles/` and look at the response. Then send a `POST` with a JSON body **without logging in** — what status code and message do you get?

---

## If it does not work

| Error | Fix |
|---|---|
| `NOT NULL constraint failed: journal_article.author_id` | You are not logged in, or `perform_create` is missing. Check `REST_FRAMEWORK` in settings (anonymous users must not POST). |
| `ValueError: Cannot assign "<AnonymousUser>": "Article.author" must be a "User" instance` | Same reason: you POSTed while logged out and the permission setting is missing. Add the `REST_FRAMEWORK` setting from **Understand**. |
| No form at the bottom of the browsable API | You are not logged in → click **Log in** (top right). If there is no Log in link, you forgot `path("api-auth/", ...)` in `config/urls.py`. |
| `AttributeError: 'function' object has no attribute 'as_view'` | `as_view()` is only for **classes**. For function views write `views.article_list` (no `.as_view()`). |
| `TypeError: ArticleList.get() got an unexpected keyword argument 'pk'` | The URL with `<int:pk>` must point to `ArticleDetail`, not `ArticleList`. |
| `AssertionError: 'ArticleList' should either include a serializer_class attribute...` | A generic view needs both `queryset` and `serializer_class`. |
| JSON parse error | Your JSON is invalid. Use **double quotes**, no trailing commas, `true`/`false` lowercase. |

---

**Next:** [06_VIEWSETS_ROUTERS_AND_CRUD.md](06_VIEWSETS_ROUTERS_AND_CRUD.md)
