from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.admin_views import EntityViewSet
from .views.faculty_view import FacultyViewSet

router = DefaultRouter()
router.register(r"faculty", FacultyViewSet, basename="faculty")
router.register(r"(?P<entity_type>[^/.]+)", EntityViewSet, basename="entity")

app_name = "entities"

urlpatterns = [
    path("", include(router.urls)),
]
