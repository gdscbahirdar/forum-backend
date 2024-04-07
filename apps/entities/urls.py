from django.urls import path

from apps.entities.views.faculty_admin_views import CreateEntityAPIView

app_name = "entities"

urlpatterns = [
    path("create_entity/<str:entity_type>/", CreateEntityAPIView.as_view(), name="create_entity"),
]
