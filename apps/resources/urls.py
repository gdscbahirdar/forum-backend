from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.resources.views.resource_views import ResourceViewSet
from apps.forum.views.vote_views import VoteViewSet
from apps.resources.views.comment_views import CommentViewSet

router = DefaultRouter()
router.register(r"resources", ResourceViewSet)
router.register(r"resources/(?P<resource_id>[-\w]+)/comments", CommentViewSet, basename="comment")

app_name = "resources"

urlpatterns = [
    path("", include(router.urls)),
    path("<str:model_name>/vote/", VoteViewSet.as_view({"post": "create"}), name="vote"),
]
