from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("rest_framework.urls", namespace="rest_framework")),  # DRF Browsable API
    path("api/users/", include("apps.users.urls")),
]
