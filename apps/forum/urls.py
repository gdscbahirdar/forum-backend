from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.forum.views.post_views import AnswerViewSet, QuestionViewSet
from apps.forum.views.tag_views import TagReadOnlyViewSet
from apps.forum.views.vote_views import VoteViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"tags", TagReadOnlyViewSet, basename="tag")

app_name = "forum"

urlpatterns = [
    path("", include(router.urls)),
    path("questions/<slug:question_slug>/answers/add/", AnswerViewSet.as_view({"post": "create"}), name="add_answer"),
    path("questions/<slug:question_slug>/vote/", VoteViewSet.as_view({"post": "create"}), name="vote_question"),
]
