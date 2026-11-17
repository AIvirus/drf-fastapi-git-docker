from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("me/", views.me, name="me"),
    # Lesson 07: simple token -> {"token": "..."}
    path("token/", obtain_auth_token, name="token"),
    # Lesson 08: JWT          -> {"access": "...", "refresh": "..."}
    path("jwt/", TokenObtainPairView.as_view(), name="jwt_obtain"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
]
