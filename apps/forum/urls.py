from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.forum.views.bookmark_views import BookmarkViewset
from apps.forum.views.post_views import AnswerViewSet, QuestionViewSet
from apps.forum.views.tag_views import TagReadOnlyViewSet
from apps.forum.views.vote_views import VoteViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"questions/(?P<question_slug>[-\w]+)/answers", AnswerViewSet, basename="answer")
router.register(r"tags", TagReadOnlyViewSet, basename="tag")

app_name = "forum"

urlpatterns = [
    path("", include(router.urls)),
    path("vote/", VoteViewSet.as_view({"post": "create"}), name="vote"),
    path(
        "bookmark/<uuid:object_id>/",
        BookmarkViewset.as_view({"post": "add_bookmark", "delete": "remove_bookmark"}),
        name="bookmark",
    ),
]
