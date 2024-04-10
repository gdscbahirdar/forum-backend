from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.forum.views.post_views import AnswerViewSet
from apps.forum.views.post_views import QuestionViewSet
from apps.forum.views.vote_views import VoteViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")

app_name = "forum"

urlpatterns = [
    path("", include(router.urls)),
    path("questions/<slug:question_slug>/answers/add/", AnswerViewSet.as_view({"post": "create"}), name="add_answer"),
    path("questions/<slug:question_slug>/vote/", VoteViewSet.as_view({"post": "create"}), name="vote_question"),
]
