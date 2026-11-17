from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthApiTests(APITestCase):
    def test_register_hashes_password_and_hides_it(self):
        data = {"username": "asha", "email": "asha@example.com", "password": "Very-strong-pass-123"}
        response = self.client.post("/api/auth/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)  # never send the password back
        user = User.objects.get(username="asha")
        self.assertNotEqual(user.password, "Very-strong-pass-123")  # it is hashed
        self.assertTrue(user.check_password("Very-strong-pass-123"))

    def test_weak_password_is_rejected(self):
        data = {"username": "ravi", "password": "123"}
        response = self.client.post("/api/auth/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_login_then_me(self):
        User.objects.create_user(username="meera", password="Strong-password-12345")
        response = self.client.post(
            "/api/auth/token/",
            {"username": "meera", "password": "Strong-password-12345"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.data["username"], "meera")

    def test_jwt_login_then_me(self):
        User.objects.create_user(username="kiran", password="Strong-password-12345")
        response = self.client.post(
            "/api/auth/jwt/",
            {"username": "kiran", "password": "Strong-password-12345"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        access = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.data["username"], "kiran")

    def test_jwt_refresh_gives_new_access_token(self):
        User.objects.create_user(username="dev", password="Strong-password-12345")
        tokens = self.client.post(
            "/api/auth/jwt/",
            {"username": "dev", "password": "Strong-password-12345"},
            format="json",
        ).data
        response = self.client.post(
            "/api/auth/jwt/refresh/", {"refresh": tokens["refresh"]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_me_without_token_is_401(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
