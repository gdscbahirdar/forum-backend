from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.forum.models.qa_meta_models import Bookmark
from apps.forum.models.qa_models import Question
from apps.forum.serializers.post_serializers import BookmarkedPostSerializer

User = get_user_model()


class GetUserBookmarkList(ListAPIView):
    """
    API view to retrieve the list of bookmarked questions for a user.

    This view returns a list of questions that have been bookmarked by the authenticated user.
    The questions can be either directly bookmarked or have bookmarked answers.
    The questions are ordered by the creation date of the bookmarks.
    """

    serializer_class = BookmarkedPostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        bookmarked_post_ids = Bookmark.objects.filter(user=user).values_list("object_id", flat=True)
        questions = (
            Question.objects.filter(
                models.Q(post__pk__in=bookmarked_post_ids) | models.Q(answers__post__pk__in=bookmarked_post_ids),
            )
            .distinct()
            .order_by("-post__bookmarks__created_at")
        )
        return questions

    def get_serializer_context(self):
        context = super(GetUserBookmarkList, self).get_serializer_context()
        context.update({"request": self.request})
        return context
