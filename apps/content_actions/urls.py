from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.content_actions.views.bookmark_views import BookmarkViewset
from apps.content_actions.views.comment_views import CommentViewSet
from apps.content_actions.views.vote_views import VoteViewSet

router = DefaultRouter()
router.register(r"(?P<model_name>\w+)/(?P<object_id>[0-9a-f-]+)/comments", CommentViewSet, basename="comment")

app_name = "content_actions"

urlpatterns = [
    path("", include(router.urls)),
    path("<str:model_name>/vote/", VoteViewSet.as_view({"post": "create"}), name="vote"),
    path(
        "<str:model_name>/bookmark/<uuid:object_id>/",
        BookmarkViewset.as_view(
            {
                "post": "create",
                "delete": "destroy",
            }
        ),
        name="bookmark",
    ),
]
