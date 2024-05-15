from django.contrib.contenttypes.models import ContentType
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.forum.models.qa_meta_models import Bookmark
from apps.forum.models.qa_models import Post
from apps.forum.serializers.bookmark_serializers import BookmarkSerializer


class BookmarkViewset(viewsets.ModelViewSet):
    """
    Viewset for managing bookmarks.

    This viewset provides the following actions:
    - add_bookmark: Adds a bookmark for a specific object.
    - remove_bookmark: Removes a bookmark for a specific object.
    """

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)

    def add_bookmark(self, request, object_id):
        """
        Adds a bookmark for a specific object.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (int): The ID of the object to bookmark.

        Returns:
            Response: The HTTP response indicating the success of the operation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content_type = ContentType.objects.get_for_model(Post)
        bookmark = Bookmark.objects.create(user=self.request.user, content_type=content_type, object_id=object_id)
        bookmark.post.evaluate_bookmark_badges()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def remove_bookmark(self, request, object_id):
        """
        Removes a bookmark for a specific object.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (int): The ID of the object to remove the bookmark from.

        Returns:
            Response: The HTTP response indicating the success of the operation.
        """
        content_type = ContentType.objects.get_for_model(Post)
        instance = Bookmark.objects.filter(
            user=self.request.user, content_type=content_type, object_id=object_id
        ).first()
        if instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_serializer_context(self):
        """
        Returns the context for the serializer.

        Returns:
            dict: The context for the serializer.
        """
        context = super().get_serializer_context()
        context["object_id"] = self.kwargs.get("object_id")
        return context
