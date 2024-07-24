from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.admin_views import EntityViewSet, UploadStudents
from .views.faculty_view import FacultyViewSet

router = DefaultRouter()
router.register(r"faculty", FacultyViewSet, basename="faculty")
router.register(r"(?P<entity_type>[^/.]+)", EntityViewSet, basename="entity")

app_name = "entities"

urlpatterns = [
    path("upload_students/", UploadStudents.as_view(), name="upload_students"),
    path("", include(router.urls)),
]
