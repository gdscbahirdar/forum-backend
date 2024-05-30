from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.resources.views.resource_views import ResourceViewSet

router = DefaultRouter()
router.register(r"resources", ResourceViewSet)

app_name = "resources"

urlpatterns = [
    path("", include(router.urls)),
]
