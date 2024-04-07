from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.faculty_admin_views import EntityViewSet

router = DefaultRouter()
router.register(r"(?P<entity_type>[^/.]+)", EntityViewSet, basename="entity")

app_name = "entities"

urlpatterns = [
    path("", include(router.urls)),
]
