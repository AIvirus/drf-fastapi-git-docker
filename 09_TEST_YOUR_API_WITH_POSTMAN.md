# Lesson 09 — Test Your API with Postman (and with Python)

**Time:** 40 minutes  |  **You need:** Lesson 08 finished

---

## Goal

By the end of this lesson you will:

- organise requests in a Postman **collection**,
- use **variables** like `{{baseUrl}}` and `{{access}}` instead of copy-pasting,
- write small **test scripts** in Postman that save the login token automatically and check status codes,
- **run a whole collection** with one click,
- write **automated API tests** in Django with `APITestCase`.

---

## Understand

### Manual testing vs automated testing

| | Postman by hand | Postman collection + scripts | Python `APITestCase` |
|---|---|---|---|
| How | Click Send, read the answer | Click **Run**, read ✔ / ✘ | `python manage.py test` |
| Speed | Slow | Fast | Fastest |
| Who uses it | Everyone exploring an API | Teams, QA testers, frontend developers | Backend developers, CI/CD (Day 6) |
| Database | Your real `db.sqlite3` | Your real `db.sqlite3` | A **temporary** test database |

You need both: Postman to **explore and share**, Python tests to **protect** your code every time it changes.

### Postman words

| Word | Meaning |
|---|---|
| **Collection** | A folder of saved requests — like a playlist for your API |
| **Variable** | A name like `{{baseUrl}}` that Postman replaces with a value |
| **Environment** | A set of variables, e.g. "Local" (`127.0.0.1:8000`) vs "Production" (`api.mysite.com`) |
| **Script** (Post-response / Tests) | Small JavaScript that runs **after** the response arrives: check it, save values |
| **Collection Runner** | Runs all requests in a collection, in order, and shows which tests passed |

---

## Do it now

> Run the server (`python manage.py runserver`) in one terminal for the whole lesson.

### Part A — Build your own collection

#### Step 1 — Create an environment with variables

1. Postman left sidebar → **Environments** → **+** (Create).
2. Name it **`Day3 Local`**.
3. Add these variables (type them in the **Initial value** *and* **Current value** columns):

   | Variable | Value |
   |---|---|
   | `baseUrl` | `http://127.0.0.1:8000` |
   | `username` | `asha` |
   | `password` | `Learning-APIs-2026` |
   | `access` | *(leave empty)* |

4. **Save** (Ctrl + S).
5. Top-right of Postman: choose **`Day3 Local`** from the environment drop-down (it says "No environment" now).

#### Step 2 — Create a collection

1. Left sidebar → **Collections** → **+** → name it **`My Journal API`**.
2. Click the collection → **Authorization** tab → Auth Type **Bearer Token** → Token: `{{access}}` → **Save**.

   Now **every** request in this collection sends the access token automatically (unless a request says otherwise).

#### Step 3 — A login request that saves the token by itself

1. In the collection, **Add request** → name it **`Login (JWT)`**.
2. Method **POST**, URL: `{{baseUrl}}/api/auth/jwt/`
3. **Authorization** tab → **No Auth** (you can't send a token before you have one).
4. **Body** → raw → JSON:
   ```json
   {"username": "{{username}}", "password": "{{password}}"}
   ```
5. Open the **Scripts** tab → **Post-response** (in older Postman versions this is the **Tests** tab) and type:
   ```javascript
   pm.test("Status is 200", () => pm.response.to.have.status(200));

   const data = pm.response.json();
   pm.environment.set("access", data.access);
   pm.environment.set("refresh", data.refresh);
   ```
6. **Save** and **Send**.
7. Look at the bottom panel → **Test Results**: ✔ *Status is 200*.
8. Click the **eye icon** 👁 next to the environment drop-down: `access` now has a value!

#### Step 4 — Requests that use the saved token

Add these requests to the collection. For each one, keep **Authorization → Inherit auth from parent** (that's the Bearer `{{access}}` from Step 2), and add the test script shown.

**`Who am I`** — `GET {{baseUrl}}/api/auth/me/`
```javascript
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("It is me", () => {
    pm.expect(pm.response.json().username).to.eql(pm.environment.get("username"));
});
```

**`Create article`** — `POST {{baseUrl}}/api/articles/`, Body raw JSON:
```json
{"title": "Created by my collection", "body": "Postman created this article automatically.", "is_published": true}
```
Script — it **saves the new article's id**:
```javascript
pm.test("Status is 201", () => pm.response.to.have.status(201));
pm.environment.set("articleId", pm.response.json().id);
```

**`Get article`** — `GET {{baseUrl}}/api/articles/{{articleId}}/`
```javascript
pm.test("Status is 200", () => pm.response.to.have.status(200));
```

**`Update article`** — `PATCH {{baseUrl}}/api/articles/{{articleId}}/`, Body: `{"title": "Updated by my collection"}`
```javascript
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Title changed", () => pm.expect(pm.response.json().title).to.eql("Updated by my collection"));
```

**`Delete article`** — `DELETE {{baseUrl}}/api/articles/{{articleId}}/`
```javascript
pm.test("Status is 204", () => pm.response.to.have.status(204));
```

#### Step 5 — Run the whole collection

1. Hover over **My Journal API** → click **⋯** → **Run collection** (or the **Run** button on the collection page).
2. Keep the order: Login → Who am I → Create → Get → Update → Delete.
3. Click **Run My Journal API**.

You see every request with green **PASS** labels. In about one second Postman logged in, created, read, changed and deleted an article, and checked every answer.

> **Why is this powerful?** Change your Django code, click **Run** again, and you know in seconds whether you broke something. You can also **export** the collection (⋯ → Export) and send it to a teammate or a frontend developer — it documents how to use your API.

---

### Part B — Import the ready-made collection

This course includes a bigger collection with 17 requests and tests.

1. Postman → **Import** (top left) → choose the file **`Day-03/postman/Day03_Journal_API.postman_collection.json`**.
2. A collection **"Day 3 - Journal API (DRF)"** appears. It uses its own **collection variables** (click the collection → **Variables** tab): `baseUrl`, `username` = `postman_user`, `password`, …
3. Select **No environment** at the top right (so your `Day3 Local` values don't override them).
4. **Run** the collection. Expected: **all tests pass**. The `02 Register` request creates `postman_user` the first time; on later runs it gets **400 "already exists"**, which the test also accepts.

Open a few requests and read their **Scripts → Post-response** code — it's the same idea you wrote yourself.

---

### Part C — Automated tests in Python with `APITestCase`

Postman tests need a running server and use your real database. Django tests run without a server, in a **temporary database** that is deleted afterwards — so they can run anywhere, any time (for example on GitHub, Day 6).

#### Step 6 — Write the tests

Replace **`journal/tests.py`** with:

```python
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Article

User = get_user_model()


class ArticleApiTests(APITestCase):
    def setUp(self):
        # ARRANGE: runs before EVERY test, in a temporary test database
        self.author = User.objects.create_user(username="author", password="Strong-password-12345")
        self.other = User.objects.create_user(username="other", password="Other-password-12345")
        self.published = Article.objects.create(
            author=self.author,
            title="A published article",
            body="This body is long enough to be published.",
            is_published=True,
        )
        self.draft = Article.objects.create(
            author=self.author,
            title="A private draft",
            body="Only the author can see this draft.",
        )

    def test_anyone_can_list_published_articles(self):
        response = self.client.get("/api/articles/")                        # ACT
        self.assertEqual(response.status_code, status.HTTP_200_OK)           # ASSERT
        titles = [item["title"] for item in response.data["results"]]
        self.assertIn("A published article", titles)
        self.assertNotIn("A private draft", titles)

    def test_other_user_gets_404_for_draft(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.get(f"/api/articles/{self.draft.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_user_cannot_create(self):
        data = {"title": "Hello there", "body": "x"}
        response = self.client.post("/api/articles/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logged_in_user_creates_and_is_the_author(self):
        self.client.force_authenticate(user=self.other)
        data = {"title": "My new API article", "body": "Written through the API.", "author": "author"}
        response = self.client.post("/api/articles/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], "other")   # sending "author" did not work

    def test_short_title_is_rejected(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.post("/api/articles/", {"title": "Hi", "body": "x"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_other_user_cannot_update(self):
        self.client.force_authenticate(user=self.other)
        url = f"/api/articles/{self.published.id}/"
        response = self.client.patch(url, {"title": "Hacked title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_delete(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.delete(f"/api/articles/{self.published.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Article.objects.filter(id=self.published.id).exists())
```

And **`accounts/tests.py`** — test a real JWT login (no shortcut):

```python
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthApiTests(APITestCase):
    def test_register_hides_and_hashes_password(self):
        data = {"username": "asha", "password": "Very-strong-pass-123"}
        response = self.client.post("/api/auth/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        self.assertTrue(User.objects.get(username="asha").check_password("Very-strong-pass-123"))

    def test_jwt_login_then_me(self):
        User.objects.create_user(username="kiran", password="Strong-password-12345")
        response = self.client.post(
            "/api/auth/jwt/",
            {"username": "kiran", "password": "Strong-password-12345"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.data["username"], "kiran")

    def test_me_without_token_is_401(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

#### Step 7 — Run them

Stop the server (**Ctrl + C**) or use a second terminal:

```bash
python manage.py test
```

```text
Found 10 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 4.2s

OK
Destroying test database for alias 'default'...
```

#### Step 8 — Prove the tests protect you

In **`journal/permissions.py`**, break `IsAuthorOrReadOnly` on purpose: change `return obj.author == request.user` to `return True`. Run the tests:

```text
FAIL: test_other_user_cannot_update (journal.tests.ArticleApiTests...)
AssertionError: 200 != 403
```

A test caught the security bug. **Change it back** and run the tests again → **OK**.

---

## Check

- [ ] My `Login (JWT)` request saves `access` into the environment by itself.
- [ ] Running **My Journal API** shows all tests **PASS**.
- [ ] The imported collection runs with all tests passing.
- [ ] `python manage.py test` → **OK**.
- [ ] I saw a test **fail** when I broke the permission, and pass again after fixing it.

---

## What just happened?

### Postman script cheat sheet

| Code | Does |
|---|---|
| `pm.response.to.have.status(201)` | Check the status code |
| `pm.response.json()` | The response body as a JavaScript object |
| `pm.expect(x).to.eql(y)` | Check that x equals y |
| `pm.environment.set("name", value)` | Save a value into the **environment** |
| `pm.collectionVariables.set("name", value)` | Save a value into the **collection's** variables |
| `pm.environment.get("name")` | Read a value |

Variables are resolved in this order (closest wins): **local → environment → collection → global**. That's why Part B said to choose *No environment* — otherwise your `username` from `Day3 Local` would win.

### `APITestCase` cheat sheet

| Code | Does |
|---|---|
| `self.client.get(url)` | Send a GET (like Postman, but no server needed) |
| `self.client.post(url, data, format="json")` | Send JSON. **Don't forget `format="json"`**. |
| `self.client.force_authenticate(user=u)` | Skip login — "pretend this user is logged in" |
| `self.client.credentials(HTTP_AUTHORIZATION="Bearer ...")` | Add a real header to every next request |
| `response.status_code`, `response.data` | The status and the (already decoded) data |

`force_authenticate` is a shortcut for tests about **permissions**. To test the **login itself**, send real requests, like `test_jwt_login_then_me`.

---

## Try it yourself

1. Add a Postman request **`Create without token`** with **Authorization → No Auth**, and a test that expects **401**.
2. Create a second environment **`Day3 Other User`** with ravi's username and password. Switch to it and run your collection. Everything still passes — why is ravi allowed to update and delete here? (Hint: who created the article in this run?) Then add a request that PATCHes article **1** (the admin's) and expects **403**.
3. Add Python tests for categories:
   - a normal user gets **403** on `POST /api/categories/`,
   - a staff user (`create_user(..., is_staff=True)`) gets **201**.
4. Compare your tests with [drf_lab/journal/tests.py](drf_lab/journal/tests.py) — it has 15 tests. Copy one you don't have and make it pass.

---

## If it does not work

| Problem | Fix |
|---|---|
| Postman: `{{baseUrl}}` shows red / "Could not send request" | No environment selected (top right), or the variable name is misspelled. Variable names are case-sensitive. |
| Script error: `JSONError: No data, empty input` | The response has no body (e.g. 204, or the server is down). Check the status first. |
| Login works but next requests are **401** | The token was saved in a different place than you read it (environment vs collection variable), or the request's Authorization isn't **Inherit auth from parent**. |
| Imported collection: Register fails with `400` the first time | The username `postman_user` already exists in your database — that's fine; the test accepts 400. If Login then fails, change the `password` variable to the one you used. |
| `python manage.py test`: `Ran 0 tests` | The test methods must start with **`test_`** and the file must be called **`tests.py`**. |
| A list like `"categories": [1, 2]` arrives wrong in a test | You forgot `format="json"` in `self.client.post(...)`. Without it the data is sent as a form, not JSON. |
| A test expects 401 but gets 403 | `TokenAuthentication`/`JWTAuthentication` is not the **first** item in `DEFAULT_AUTHENTICATION_CLASSES` (see Lesson 07, "401 or 403?"). |

---

**🎉 Part A of Day 3 is done!** You built a complete, secure, tested REST API with Django REST Framework.

Want to compare? Run the finished one: [drf_lab/README.md](drf_lab/README.md).

**Next:** [10_YOUR_FIRST_FASTAPI_APP.md](10_YOUR_FIRST_FASTAPI_APP.md)
