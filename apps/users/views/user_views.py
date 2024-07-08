from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.content_actions.constants import MODEL_MAPPING
from apps.content_actions.models.bookmark_models import Bookmark
from apps.forum.models.qa_models import Question
from apps.forum.serializers.post_serializers import BookmarkedPostSerializer
from apps.resources.models.resource_models import Resource
from apps.resources.serializers.resource_serializers import BookmarkedResourceSerializer
from apps.users.serializers.user_serializers import PublicUserProfileSerializer

User = get_user_model()


class GetUserBookmarkList(ListAPIView):
    """
    API view to retrieve the list of bookmarked questions for a user.

    This view returns a list of questions that have been bookmarked by the authenticated user.
    The questions can be either directly bookmarked or have bookmarked answers.
    The questions are ordered by the creation date of the bookmarks.
    """

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        bookmark_type = self.kwargs["bookmark_type"]

        if bookmark_type not in MODEL_MAPPING:
            raise ValidationError("Invalid bookmark type")

        model = MODEL_MAPPING[bookmark_type]
        content_type = ContentType.objects.get_for_model(model)

        bookmarked_object_ids = Bookmark.objects.filter(user=user, content_type=content_type).values_list(
            "object_id", flat=True
        )

        if bookmark_type == "post":
            queryset = (
                Question.objects.filter(
                    models.Q(post__pk__in=bookmarked_object_ids)
                    | models.Q(answers__post__pk__in=bookmarked_object_ids)
                )
                .distinct()
                .order_by("-post__bookmarks__created_at")
            )

        elif bookmark_type == "resource":
            queryset = (
                Resource.objects.filter(pk__in=bookmarked_object_ids).distinct().order_by("-bookmarks__created_at")
            )

        return queryset

    def get_serializer_context(self):
        context = super(GetUserBookmarkList, self).get_serializer_context()
        context.update({"request": self.request})
        context["bookmark_type"] = self.kwargs["bookmark_type"]
        return context

    def get_serializer_class(self):
        bookmark_type = self.kwargs["bookmark_type"]

        if bookmark_type == "post":
            return BookmarkedPostSerializer
        elif bookmark_type == "resource":
            return BookmarkedResourceSerializer


class UserListView(generics.ListAPIView):
    """
    API view for retrieving a list of users.

    This view returns a paginated list of all users in the system,
    ordered by their date of joining. Only authenticated users can access this view.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = PublicUserProfileSerializer
    permission_classes = (IsAuthenticated,)


class UserProfileView(APIView):
    """
    API view to retrieve a user's profile information.

    Requires authentication.

    Methods:
        - get(request, username): Retrieves the profile information of the user with the given username.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        serializer = PublicUserProfileSerializer(user)
        return Response(serializer.data)
