from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.forum.models.qa_meta_models import Comment
from apps.resources.serializers.comment_serializers import CommentSerializer
from apps.resources.models.resource_models import Resource
from apps.resources.permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling comment operations.

    This viewset allows users to perform CRUD operations (Create, Retrieve, Update, Delete) on Comment objects.
    Only authenticated users are allowed to access this viewset.

    Attributes:
        queryset (QuerySet): The queryset of all Comment objects.
        permission_classes (tuple): The permission classes required to access this viewset.
        serializer_class (Serializer): The serializer class used for serializing and deserializing Comment objects.
    """

    queryset = Comment.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = [IsAuthenticated]
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return super().get_permissions()

    def get_queryset(self):
        """
        Adjust the queryset to filter comments based on `object_id` and `content_type` for the Resource model.
        """
        resource_id = self.kwargs.get("resource_id")
        if resource_id:
            resource_content_type = ContentType.objects.get_for_model(Resource)
            return super().get_queryset().filter(content_type=resource_content_type, object_id=resource_id)
        return super().get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["object_id"] = self.kwargs.get("resource_id")
        return context
