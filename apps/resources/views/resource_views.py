from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.resources.models.resource_models import Resource
from apps.resources.serializers.resource_serializers import ResourceSerializer
from apps.resources.permissions import IsOwnerOrSuperUser, IsOwner
from apps.forum.models.qa_meta_models import ViewTracker


class ResourceViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing resources.

    This viewset provides CRUD operations (Create, Retrieve, Update, Delete) for the Resource model.
    It also includes filtering, searching, and ordering capabilities.
    """

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = (
        "uploader",
        "categories",
        "tags",
    )
    search_fields = ("title",)
    ordering_fields = ("created_at",)

    def get_permissions(self):
        if self.action in ("update", "partial_update"):
            self.permission_classes = [IsAuthenticated, IsOwner]
        if self.action in ("destroy",):
            self.permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        resource = self.get_object()

        content_type = ContentType.objects.get_for_model(Resource)
        if not ViewTracker.objects.filter(
            user=request.user, content_type=content_type, object_id=resource.pk
        ).exists():
            ViewTracker.objects.create(user=request.user, content_type=content_type, object_id=resource.pk)
            resource.view_count = F("view_count") + 1
            resource.save(update_fields=["view_count"])

        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

    def perform_update(self, serializer):
        serializer.save(uploader=self.request.user)
