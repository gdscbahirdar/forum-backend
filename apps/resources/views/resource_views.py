from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from apps.resources.models.resource_models import Resource, ResourceCategory
from apps.resources.serializers.resource_serializers import ResourceSerializer, ResourceCategorySerializer
from apps.resources.permissions import IsOwnerOrSuperUser, IsOwner
from apps.content_actions.models.view_models import ViewTracker


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
    filterset_fields = ("user", "categories", "tags")
    search_fields = ("title",)
    ordering = ("-created_at",)
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
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="myUploads")
    def my_uploads(self, request):
        queryset = Resource.objects.filter(user=request.user).order_by("-created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ResourceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ResourceSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="categories")
    def categories(self, request):
        search_query = request.query_params.get("search", None)
        if search_query:
            categories = ResourceCategory.objects.filter(name__icontains=search_query)
        else:
            categories = ResourceCategory.objects.all()

        page = self.paginate_queryset(categories)
        if page is not None:
            serializer = ResourceCategorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ResourceCategorySerializer(categories, many=True)
        return Response(serializer.data)
