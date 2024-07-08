from django.contrib.contenttypes.models import ContentType
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from apps.content_actions.constants import MODEL_MAPPING
from apps.content_actions.models.comment_models import Comment
from apps.content_actions.serializers.comment_serializers import CommentSerializer
from apps.forum.permissions import IsOwnerOrReadOnly


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
    filter_backends = (filters.OrderingFilter,)
    ordering = ("-created_at",)
    ordering_fields = ("created_at",)

    def get_permissions(self):
        if self.action in ("create",):
            return [IsAuthenticated()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()

    def get_queryset(self):
        """
        Adjust the queryset to filter comments based on `object_id` and `content_type` of a model.
        """
        object_id = self.kwargs.get("object_id")
        model_name = self.kwargs.get("model_name")

        model = MODEL_MAPPING.get(model_name)
        if not model:
            raise ValidationError("Invalid model type")

        try:
            instance = model.objects.get(id=object_id)
            content_type = ContentType.objects.get_for_model(model)
        except model.DoesNotExist:
            raise ValidationError("Invalid object_id")

        return super().get_queryset().filter(content_type=content_type, object_id=instance.id)
