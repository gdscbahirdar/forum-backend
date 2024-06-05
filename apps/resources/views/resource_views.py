from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsOwnerOrSuperUser
from apps.content_actions.models.view_models import ViewTracker
from apps.resources.models.resource_models import Resource, ResourceCategory
from apps.resources.serializers.resource_serializers import ResourceCategorySerializer, ResourceSerializer


class ResourceFilter(django_filters.FilterSet):
    categories = django_filters.CharFilter(method="filter_by_categories")
    tags = django_filters.CharFilter(method="filter_by_tags")

    class Meta:
        model = Resource
        fields = ["user", "categories", "tags"]

    def filter_by_categories(self, queryset, name, value):
        if value:
            category_names = value.split(",")
            return queryset.filter(categories__name__in=category_names).distinct()
        return queryset

    def filter_by_tags(self, queryset, name, value):
        if value:
            tag_names = value.split(",")
            return queryset.filter(tags__name__in=tag_names).distinct()
        return queryset


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
    filterset_class = ResourceFilter
    search_fields = ("title",)
    ordering = ("-created_at",)
    ordering_fields = ("created_at", "view_count")

    def get_permissions(self):
        if self.action in ("update", "partial_update"):
            self.permission_classes = [IsAuthenticated, IsOwnerOrSuperUser]
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
