from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.feedback.views.feedback_views import FeedbackReplyViewSet
from apps.feedback.views.feedback_views import FeedbackViewSet

app_name = "feedback"

router = DefaultRouter()
router.register(r"feedback", FeedbackViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "feedback/<uuid:feedback_id>/replies/",
        FeedbackReplyViewSet.as_view({"get": "list", "post": "create"}),
        name="feedback-reply-list",
    ),
    path(
        "feedback/<uuid:feedback_id>/replies/<uuid:pk>/",
        FeedbackReplyViewSet.as_view({"get": "retrieve", "put": "update", "patch": "update", "delete": "destroy"}),
        name="feedback-reply-detail",
    ),
]
