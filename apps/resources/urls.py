from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.resources.views.resource_views import ResourceViewSet

router = DefaultRouter()
router.register(r"resources", ResourceViewSet, basename="resource")

app_name = "resources"

urlpatterns = [
    path("", include(router.urls)),
]
