# Lesson 04 — Models and Serializers (Rows ⇄ JSON)

**Time:** 35 minutes  |  **You need:** Lesson 03 finished

---

## Goal

By the end of this lesson you will:

- create the **Category** and **Article** models (the same idea as Day 2),
- add some data with the **admin**,
- write **serializers** that turn database rows into JSON,
- use a serializer to **validate** incoming JSON and **save** it,
- add your own validation rules.

---

## Understand

### The problem a serializer solves

Your database gives you **Python objects** (`Article` instances). An API must send **JSON text**. And when a client sends JSON, you must **check** it before saving.

```text
           SERIALIZE (output)                         DESERIALIZE (input)
Article object ─► Python dict ─► JSON text     JSON text ─► Python dict ─► validate ─► Article object
                ▲ serializer.data                                         ▲ serializer.is_valid()
                                                                                    serializer.save()
```

A **serializer** does both directions. If you remember **Django forms** from Day 2, a serializer is the same idea for JSON:

| Day 2 form | Day 3 serializer |
|---|---|
| `ArticleForm(request.POST)` | `ArticleSerializer(data=request.data)` |
| `form.is_valid()` | `serializer.is_valid()` |
| `form.errors` | `serializer.errors` |
| `form.cleaned_data` | `serializer.validated_data` |
| `form.save()` | `serializer.save()` |
| `ModelForm` (fields from the model) | **`ModelSerializer`** (fields from the model) |
| `clean_title()` | `validate_title()` |

### `Serializer` vs `ModelSerializer`

You *could* list every field by hand:

```python
class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=60)
    description = serializers.CharField(max_length=160, required=False, allow_blank=True)
    # ...and write create() and update() yourself
```

A **`ModelSerializer`** reads your model and does all that for you — fields, types, max lengths, `unique` checks, `create()` and `update()`:

```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
```

You will almost always use `ModelSerializer`.

---

## Do it now

> Stop the server (**Ctrl + C**) when you need the terminal. Terminal must end with `my_api>`.

### Step 1 — The models

Open **`journal/models.py`** and replace everything with:

```python
from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    title = models.CharField(max_length=160)
    body = models.TextField()
    categories = models.ManyToManyField(Category, blank=True, related_name="articles")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
```

These are the Day 2 models, a little simpler. Remember: **One-to-Many** (one author → many articles) and **Many-to-Many** (articles ⇄ categories).

### Step 2 — Register them in the admin

**`journal/admin.py`**:

```python
from django.contrib import admin

from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "is_published", "created_at"]
    list_filter = ["is_published", "categories"]
    search_fields = ["title", "body"]
```

### Step 3 — Create the tables and an admin user

```bash
python manage.py makemigrations journal
```
```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```

Choose a username (e.g. `admin`), skip the email if you like, and a password you will remember. (The password is invisible while you type — that's normal.)

### Step 4 — Add some data in the admin

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/admin/ and log in. Add:

- **2 categories:** `Django` and `APIs`
- **3 articles** (author = your admin user):
  1. "What is a REST API?" — any body text of at least 20 characters — both categories — **Published ✔**
  2. "Serializers explained" — any body — `Django` — **Published ✔**
  3. "My secret draft" — any body — **Published ✘** (a draft)

### Step 5 — Write the serializers

Create a new file **`journal/serializers.py`**:

```python
from rest_framework import serializers

from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ArticleSerializer(serializers.ModelSerializer):
    # Show the author's username, and never let the client choose the author.
    author = serializers.ReadOnlyField(source="author.username")
    # Clients send category ids, e.g. "categories": [1, 3]
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "body",
            "author",
            "categories",
            "is_published",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
```

Save.

### Step 6 — Serialize: database → JSON (in the shell)

Stop the server (**Ctrl + C**) and open the Django shell:

```bash
python manage.py shell
```

Type these lines one by one (the `>>>` is the prompt — don't type it):

```python
>>> from journal.models import Article, Category
>>> from journal.serializers import ArticleSerializer, CategorySerializer
>>> article = Article.objects.get(title="What is a REST API?")
>>> serializer = ArticleSerializer(article)
>>> serializer.data
```

You see a **Python dictionary**:

```python
{'id': 1, 'title': 'What is a REST API?', 'body': '...', 'author': 'admin', 'categories': [2, 1], 'is_published': True, 'created_at': '2026-11-17T21:07:14.834273+05:30', 'updated_at': '...'}
```

Now turn it into real JSON text:

```python
>>> from rest_framework.renderers import JSONRenderer
>>> JSONRenderer().render(serializer.data)
b'{"id":1,"title":"What is a REST API?",...,"is_published":true,...}'
```

See `True` → `true`. That is exactly what your API will send.

**Many objects** at once → `many=True`:

```python
>>> CategorySerializer(Category.objects.all(), many=True).data
[{'id': 2, 'name': 'APIs', 'description': ''}, {'id': 1, 'name': 'Django', 'description': ''}]
```

### Step 7 — Deserialize: JSON → validate → database

Pretend a client sent this JSON:

```python
>>> data = {"title": "Created from the shell", "body": "Serializers can save too.", "categories": [1]}
>>> serializer = ArticleSerializer(data=data)
>>> serializer.is_valid()
True
>>> serializer.validated_data
{'title': 'Created from the shell', 'body': 'Serializers can save too.', 'categories': [<Category: Django>]}
```

Save it. The author is read-only, so **we** give it:

```python
>>> from django.contrib.auth.models import User
>>> admin_user = User.objects.get(username="admin")
>>> new_article = serializer.save(author=admin_user)
>>> new_article.id, new_article.title
(4, 'Created from the shell')
```

Now send **bad** data:

```python
>>> bad = ArticleSerializer(data={"body": "no title here", "categories": [99]})
>>> bad.is_valid()
False
>>> bad.errors
{'title': [ErrorDetail(string='This field is required.', code='required')], 'categories': [ErrorDetail(string='Invalid pk "99" - object does not exist.', code='does_not_exist')]}
```

The serializer found **both** problems. Your API will send these errors back to the client with status **400**.

Leave the shell with `exit()`.

### Step 8 — Add your own validation rules

Add these two methods **inside** `ArticleSerializer` (below `class Meta`, same indentation as `class Meta`):

```python
    # Validation for ONE field -> a method called validate_<field_name>
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value.strip()

    # Validation that needs SEVERAL fields -> validate()
    def validate(self, data):
        # On an update, a field that was not sent keeps its old value (self.instance).
        body = data.get("body", getattr(self.instance, "body", ""))
        is_published = data.get("is_published", getattr(self.instance, "is_published", False))
        if is_published and len(body) < 20:
            raise serializers.ValidationError(
                {"body": "A published article needs a body of at least 20 characters."}
            )
        return data
```

Test it in the shell (`python manage.py shell`):

```python
>>> from journal.serializers import ArticleSerializer
>>> s = ArticleSerializer(data={"title": "Hi", "body": "x"})
>>> s.is_valid(), s.errors
(False, {'title': [ErrorDetail(string='Title must be at least 5 characters long.', code='invalid')]})
>>> s = ArticleSerializer(data={"title": "Publish me", "body": "short", "is_published": True})
>>> s.is_valid(), s.errors
(False, {'body': [ErrorDetail(string='A published article needs a body of at least 20 characters.', code='invalid')]})
```

`exit()` when done.

---

## Check

- [ ] The admin shows 2 categories and at least 3 articles (one is a draft).
- [ ] `ArticleSerializer(article).data` returns a dictionary with `author` = your username.
- [ ] `is_valid()` is `True` for good data and `False` (with clear `errors`) for bad data.
- [ ] A title of `"Hi"` is rejected by your own rule.

---

## What just happened?

| Code | Meaning |
|---|---|
| `ArticleSerializer(article)` | "Prepare this object for **output**." |
| `.data` | The ready-to-send dictionary. |
| `ArticleSerializer(data=...)` | "Here is **input**; check it." |
| `.is_valid()` | Runs every check: types, required fields, `max_length`, `unique`, existing category ids, **and** your `validate_...` methods. |
| `.save(author=...)` | Calls `create()` → `Article.objects.create(...)` and sets the categories. Extra keyword arguments (like `author`) are added to the saved object. |
| `ReadOnlyField(source="author.username")` | Output only. Follows the ForeignKey to the user and shows `username`. A client **cannot** set it. |
| `PrimaryKeyRelatedField(many=True, ...)` | Shows the related categories as a list of ids, and accepts a list of ids as input (and checks they exist). |
| `read_only_fields` | Sent in the output, ignored in the input. |

### Why must the client never choose the author?

If `author` were writable, anyone could send `{"author": 5, "title": "..."}` and post **as someone else**. The rule: **the server decides who the author is — from the login, never from the JSON.** You'll do that in the view in Lesson 05.

### Other ways to show a relationship

| Field | JSON output for categories |
|---|---|
| `PrimaryKeyRelatedField(many=True)` (ours) | `[2, 1]` |
| `StringRelatedField(many=True)` (read-only) | `["APIs", "Django"]` |
| `CategorySerializer(many=True, read_only=True)` (nested) | `[{"id": 2, "name": "APIs", ...}, ...]` |
| `SlugRelatedField(many=True, slug_field="name", queryset=...)` | `["APIs", "Django"]` (writable too) |

---

## Try it yourself

1. In the shell, print `repr(CategorySerializer())`. DRF shows the fields it **generated** from your model, including `max_length=60` and a `UniqueValidator`. Then try to create a category called `Django` again with the serializer — what error do you get?
2. Add a field `body_length` that is **calculated**, not stored:
   ```python
   body_length = serializers.SerializerMethodField()

   def get_body_length(self, obj):
       return len(obj.body)
   ```
   Add `"body_length"` to `fields`, then check `ArticleSerializer(article).data` again.
3. Add a rule to `validate_title`: the title may not contain the word `"spam"` (in any upper/lower case).

---

## If it does not work

| Error | Fix |
|---|---|
| `ImproperlyConfigured: Field name 'x' is not valid for model 'Article'` | A name in `fields` is misspelled or doesn't exist on the model. |
| `AssertionError: Relational field must provide a queryset argument` | `PrimaryKeyRelatedField` needs `queryset=Category.objects.all()` (or `read_only=True`). |
| `IntegrityError: NOT NULL constraint failed: journal_article.author_id` | You called `serializer.save()` without `author=...`. |
| `AssertionError: You must call .is_valid() before calling .save()` | Call `is_valid()` first, and only save if it returned `True`. |
| `no such table: journal_article` | You didn't run `makemigrations journal` and `migrate`. |
| Changes in `serializers.py` not seen in the shell | The shell loads files once. `exit()` and open it again. |

Compare with: [drf_lab/journal/models.py](drf_lab/journal/models.py), [drf_lab/journal/serializers.py](drf_lab/journal/serializers.py).

---

**Next:** [05_API_VIEWS.md](05_API_VIEWS.md)
