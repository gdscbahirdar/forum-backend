from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.content_actions.models.bookmark_models import Bookmark
from apps.content_actions.serializers.bookmark_serializers import BookmarkSerializer


class BookmarkViewset(viewsets.ModelViewSet):
    """
    Viewset for managing bookmarks.

    This viewset provides the following actions:
    - create: Adds a bookmark for a specific object.
    - destroy: Removes a bookmark for a specific object.
    """

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        Creates a bookmark for a specific object.
        """
        serializer = self.get_serializer(data=request.data, context={"request": request, "view": self})
        serializer.is_valid(raise_exception=True)

        bookmark = Bookmark.objects.create(
            user=request.user,
            content_type=serializer.validated_data["content_type"],
            object_id=serializer.validated_data["object_id"],
        )

        instance = bookmark.content_type.get_object_for_this_type(id=bookmark.object_id)
        if hasattr(instance, "evaluate_bookmark_badges"):
            instance.evaluate_bookmark_badges()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
        Removes a bookmark for a specific object.
        """
        serializer = self.get_serializer(data=request.data, context={"request": request, "view": self})
        serializer.is_valid(raise_exception=True)

        instance = Bookmark.objects.filter(
            user=request.user,
            content_type=serializer.validated_data["content_type"],
            object_id=serializer.validated_data["object_id"],
        ).first()

        if instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND)
