from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Article, Category

User = get_user_model()


class ArticleApiTests(APITestCase):
    def setUp(self):
        # ARRANGE: runs before EVERY test, in a temporary test database
        self.author = User.objects.create_user(username="author", password="Strong-password-12345")
        self.other = User.objects.create_user(username="other", password="Other-password-12345")
        self.category = Category.objects.create(name="Django")
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
            is_published=False,
        )

    def test_hello_endpoint(self):
        response = self.client.get("/api/hello/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Hello from Django REST Framework!")

    def test_anyone_can_list_published_articles(self):
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data["results"]]
        self.assertIn("A published article", titles)
        self.assertNotIn("A private draft", titles)

    def test_author_sees_own_draft(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.get(f"/api/articles/{self.draft.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_gets_404_for_draft(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.get(f"/api/articles/{self.draft.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_user_cannot_create(self):
        response = self.client.post("/api/articles/", {"title": "Hello", "body": "x"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logged_in_user_can_create_and_is_the_author(self):
        self.client.force_authenticate(user=self.other)
        data = {
            "title": "My new API article",
            "body": "Written through the REST API.",
            "categories": [self.category.id],
            "author": "author",  # a trick: try to pretend to be someone else
        }
        response = self.client.post("/api/articles/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], "other")  # the trick did not work
        self.assertEqual(response.data["categories"], [self.category.id])

    def test_short_title_is_rejected(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.post("/api/articles/", {"title": "Hi", "body": "x"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_published_article_needs_long_body(self):
        self.client.force_authenticate(user=self.author)
        data = {"title": "Too short to publish", "body": "short", "is_published": True}
        response = self.client.post("/api/articles/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("body", response.data)

    def test_author_can_update(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.patch(
            f"/api/articles/{self.published.id}/", {"title": "Updated title"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.published.refresh_from_db()
        self.assertEqual(self.published.title, "Updated title")

    def test_other_user_cannot_update(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(
            f"/api/articles/{self.published.id}/", {"title": "Hacked title"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_delete(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.delete(f"/api/articles/{self.published.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Article.objects.filter(id=self.published.id).exists())

    def test_search(self):
        response = self.client.get("/api/articles/?search=published")
        self.assertEqual(response.data["count"], 1)

    def test_mine_needs_login(self):
        response = self.client.get("/api/articles/mine/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryApiTests(APITestCase):
    def test_normal_user_cannot_create_category(self):
        user = User.objects.create_user(username="normal", password="Strong-password-12345")
        self.client.force_authenticate(user=user)
        response = self.client.post("/api/categories/", {"name": "Python"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_can_create_category(self):
        staff = User.objects.create_user(
            username="staff", password="Strong-password-12345", is_staff=True
        )
        self.client.force_authenticate(user=staff)
        response = self.client.post("/api/categories/", {"name": "Python"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
