from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.forum.models.qa_meta_models import Tag
from apps.forum.serializers.post_serializers import QuestionSerializer
from apps.forum.serializers.tag_serializers import TagSerializer


class TagReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only viewset for handling Tag objects.

    This viewset provides the following actions:
    - list: Retrieve a list of all tags.
    - retrieve: Retrieve a specific tag by name.
    - questions: Retrieve all questions associated with a specific tag.

    Only authenticated users can access these actions.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "name"
    lookup_value_regex = "[^/]+"
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name",)
    ordering = ("-created_at",)
    ordering_fields = ("created_at",)

    @action(detail=True, methods=["get"], url_path="questions")
    def questions(self, request, *args, **kwargs):
        tag = self.get_object()
        questions = tag.questions.order_by("-created_at")

        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = QuestionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
