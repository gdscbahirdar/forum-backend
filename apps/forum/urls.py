from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.forum.views.post_views import AnswerViewSet
from apps.forum.views.post_views import QuestionViewSet
from apps.forum.views.post_views import UserAnsweredQuestionsView
from apps.forum.views.tag_views import TagReadOnlyViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"questions/(?P<question_slug>[-\w]+)/answers", AnswerViewSet, basename="answer")
router.register(r"tags", TagReadOnlyViewSet, basename="tag")

app_name = "forum"

urlpatterns = [
    path("", include(router.urls)),
    path("questions/answered_by/<str:username>/", UserAnsweredQuestionsView.as_view(), name="user_answered_questions"),
]
