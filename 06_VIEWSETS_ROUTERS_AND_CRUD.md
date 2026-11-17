# Lesson 06 — ViewSets, Routers and Complete CRUD

**Time:** 40 minutes  |  **You need:** Lesson 05 finished

---

## Goal

By the end of this lesson:

- **2 small classes** will give you **12 endpoints** (full CRUD for articles *and* categories),
- a **router** will write your URL patterns for you,
- `/api/` will show a clickable **API root**,
- your API will support **search**, **ordering**, **filtering**, **pagination**,
- drafts will be hidden from everyone except their author,
- you will add a custom endpoint: `/api/articles/mine/`.

---

## Understand

### What is a ViewSet?

In Lesson 05 you needed **two** views per resource (list + detail) and **two** URL lines. A **ViewSet** puts all the actions for one resource into **one class**:

| ViewSet action | HTTP method + URL |
|---|---|
| `list` | `GET /articles/` |
| `create` | `POST /articles/` |
| `retrieve` | `GET /articles/7/` |
| `update` | `PUT /articles/7/` |
| `partial_update` | `PATCH /articles/7/` |
| `destroy` | `DELETE /articles/7/` |

`ModelViewSet` = all six actions, ready-made.
`ReadOnlyModelViewSet` = only `list` + `retrieve`.

### What is a router?

A ViewSet doesn't know its URLs. A **router** looks at your ViewSet and **creates the URL patterns** automatically:

```python
router.register("articles", ArticleViewSet, basename="article")
# creates:  articles/        → name "article-list"
#           articles/<pk>/   → name "article-detail"
```

`DefaultRouter` also creates an **API root** page at `/api/` that links to all your resources.

### Views → generic views → ViewSets: which one?

```text
More control ◄──────────────────────────────────────────► Less code
@api_view    APIView     generic views      ViewSet + router
(Lesson 03)  (Lesson 05) (Lesson 05)        (this lesson)
```

Use ViewSets for normal model CRUD. Use `@api_view`/`APIView` for special endpoints (like `hello`, or `me` in Lesson 07).

---

## Do it now

### Step 1 — Replace the views with ViewSets

Replace **`journal/views.py`** with:

```python
from django.db.models import Q
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello from Django REST Framework!"})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    # ?search=django  and  ?ordering=-created_at
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "body"]
    ordering_fields = ["created_at", "title"]

    def get_queryset(self):
        """Everyone sees published articles. A logged-in user also sees their own drafts."""
        user = self.request.user
        queryset = Article.objects.select_related("author").prefetch_related("categories")
        if user.is_authenticated:
            queryset = queryset.filter(Q(is_published=True) | Q(author=user))
        else:
            queryset = queryset.filter(is_published=True)

        # ?category=2 shows only articles in category 2
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        return queryset

    def perform_create(self, serializer):
        # The author is ALWAYS the logged-in user, never something the client sends.
        serializer.save(author=self.request.user)

    # An extra endpoint: GET /api/articles/mine/
    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        articles = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
```

### Step 2 — Let the router write the URLs

Replace **`journal/urls.py`** with:

```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("categories", views.CategoryViewSet, basename="category")
router.register("articles", views.ArticleViewSet, basename="article")

urlpatterns = [
    path("hello/", views.hello, name="hello"),
    path("", include(router.urls)),
]
```

### Step 3 — Turn on pagination

In **`config/settings.py`**, add two lines to your `REST_FRAMEWORK` setting:

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
```

### Step 4 — Explore your API

Run the server and open **http://127.0.0.1:8000/api/** — the **API Root**:

```json
{
    "categories": "http://127.0.0.1:8000/api/categories/",
    "articles": "http://127.0.0.1:8000/api/articles/"
}
```

Click the links. Then try every one of these (log in through the browsable API first for the POST/PATCH/DELETE ones):

| Try this | You should see |
|---|---|
| `GET /api/articles/` | `{"count": ..., "next": null, "previous": null, "results": [...]}` — now **paginated** |
| `GET /api/articles/` while **logged out** | no draft |
| `GET /api/articles/` while logged in as the author | the draft is there |
| `GET /api/articles/?search=REST` | only articles with "REST" in title or body |
| `GET /api/articles/?ordering=title` | sorted A→Z (`-title` = Z→A) |
| `GET /api/articles/?category=1` | only articles in category 1 |
| `GET /api/articles/mine/` | only your articles (logged out → 403) |
| `POST /api/categories/` `{"name": "FastAPI"}` | **201** — a new category |
| `PATCH /api/categories/3/` `{"description": "Fast Python APIs"}` | **200** |
| `DELETE /api/categories/3/` | **204** |

> The browsable API also shows a **Filters** button (top right of a list) for search and ordering.

### Step 5 — See all the URLs the router made

Open http://127.0.0.1:8000/api/banana/ (a URL that doesn't exist). The yellow 404 page lists every URL pattern, including the ones the router created:

```text
api/ hello/ [name='hello']
api/ ^categories/$ [name='category-list']
api/ ^categories/(?P<pk>[^/.]+)/$ [name='category-detail']
api/ ^articles/$ [name='article-list']
api/ ^articles/mine/$ [name='article-mine']
api/ ^articles/(?P<pk>[^/.]+)/$ [name='article-detail']
api/ ^$ [name='api-root']
...
```

(Each one also has a `.json` format version.)

---

## Check

- [ ] `/api/` shows the API Root with 2 links.
- [ ] The article list is paginated (`count`, `next`, `previous`, `results`).
- [ ] Logged out you **don't** see drafts; logged in as the author you **do**.
- [ ] `?search=`, `?ordering=` and `?category=` work.
- [ ] `/api/articles/mine/` works when logged in.
- [ ] You can do all of CRUD on categories.

---

## What just happened?

### 12 endpoints from 2 classes

| URL | GET | POST | PUT | PATCH | DELETE |
|---|---|---|---|---|---|
| `/api/articles/` | list | create | | | |
| `/api/articles/<id>/` | retrieve | | update | partial_update | destroy |
| `/api/categories/` | list | create | | | |
| `/api/categories/<id>/` | retrieve | | update | partial_update | destroy |

Plus your extra `mine` action.

### `get_queryset()` — security through the queryset

`get_queryset()` decides **which rows exist** for this request. It is used for the list **and** for retrieve/update/delete. So if a draft is not in the queryset, `GET /api/articles/<draft id>/` returns **404** for other users — they can't even find out that it exists. (Same idea as Day 2's "other users get 404".)

### `Q` objects

`Q(is_published=True) | Q(author=user)` means **OR** in a database query: "published **or** mine". Without `Q`, `filter(a=1, b=2)` always means **AND**.

### `select_related` / `prefetch_related`

You met the **N+1 problem** on Day 2. The serializer shows `author.username` and `categories` for every article. Without these two, Django would run **extra queries for every article**. `select_related("author")` fetches authors in the same query (ForeignKey); `prefetch_related("categories")` fetches all categories in one extra query (Many-to-Many).

### Pagination

10,000 articles in one response would be slow and huge. With `PAGE_SIZE: 10` the client gets 10 at a time, and `next` is the URL of the next page (`?page=2`).

### `@action`

`@action(detail=False)` → an extra URL on the **collection**: `/api/articles/mine/`.
`@action(detail=True)` → an extra URL on **one item**: `/api/articles/7/publish/`.

---

## Try it yourself

1. Add a `publish` action (detail=True, method POST) that sets `is_published = True` on an article and returns it:
   ```python
   @action(detail=True, methods=["post"])
   def publish(self, request, pk=None):
       article = self.get_object()
       article.is_published = True
       article.save()
       return Response(self.get_serializer(article).data)
   ```
   Call `POST /api/articles/<id>/publish/`. (Lesson 07 will make sure only the author can do this.)
2. Change `PAGE_SIZE` to `2` and follow the `next` links through your articles.
3. Make categories **read-only** by using `viewsets.ReadOnlyModelViewSet` for `CategoryViewSet`. Which endpoints disappear from the 404 URL list? Change it back afterwards.
4. Add `?author=admin` filtering to `get_queryset()`. Hint: `queryset.filter(author__username=...)`.

---

## If it does not work

| Error | Fix |
|---|---|
| `AssertionError: basename argument not specified` | ViewSets with `get_queryset()` and no `queryset` attribute need `basename="article"` in `router.register(...)`. |
| `/api/` shows 404 | You forgot `path("", include(router.urls))`, or the main `config/urls.py` doesn't include `journal.urls` under `api/`. |
| The list isn't paginated | `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE` must be **inside** `REST_FRAMEWORK = {...}`. |
| `?search=` does nothing | `filter_backends` and `search_fields` must be on the ViewSet; check spelling. |
| `NameError: name 'Q' is not defined` | `from django.db.models import Q` |
| `/api/articles/mine/` → 404 | `@action` must be **inside** the class (indented), and the method name must be `mine`. |
| `UnorderedObjectListWarning` | Your model needs `ordering` in `class Meta` (we have it). |

Compare with: [drf_lab/journal/views.py](drf_lab/journal/views.py), [drf_lab/journal/urls.py](drf_lab/journal/urls.py).

---

**Next:** [07_AUTHENTICATION_AND_PERMISSIONS.md](07_AUTHENTICATION_AND_PERMISSIONS.md)
