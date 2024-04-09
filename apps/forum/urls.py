from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.forum.views.post_views import QuestionViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")

app_name = "forum"

urlpatterns = [
    path("", include(router.urls)),
]
