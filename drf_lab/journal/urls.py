from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Lesson 06: the router writes the URL patterns for our ViewSets.
router = DefaultRouter()
router.register("categories", views.CategoryViewSet, basename="category")
router.register("articles", views.ArticleViewSet, basename="article")

urlpatterns = [
    path("hello/", views.hello, name="hello"),
    path("", include(router.urls)),
]
