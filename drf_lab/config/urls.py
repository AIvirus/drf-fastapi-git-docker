from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("journal.urls")),               # Lessons 03-06
    path("api/auth/", include("accounts.urls")),         # Lessons 07-08
    path("api-auth/", include("rest_framework.urls")),   # "Log in" link in the browsable API
]
