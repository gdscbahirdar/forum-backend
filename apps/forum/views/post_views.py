from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.forum.models.qa_models import Answer, Question
from apps.forum.permissions import IsOwnerOrReadOnly
from apps.forum.serializers.post_serializers import AnswerSerializer, QuestionDetailSerializer, QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on Question objects.

    Inherits from viewsets.ModelViewSet, which provides default implementations for
    the standard list, create, retrieve, update, and destroy actions.

    Attributes:
        queryset (QuerySet): The queryset of Question objects.
        permission_classes (tuple): The permission classes required for accessing the viewset.
        lookup_field (str): The field used for looking up individual Question objects.
        filter_backends (tuple): The filter backends used for filtering the queryset.
        filterset_fields (tuple): The fields used for filtering the queryset.
        search_fields (tuple): The fields used for searching the queryset.
        ordering (str): The default ordering for the queryset.
        ordering_fields (tuple): The fields used for ordering the queryset.
    """

    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("is_closed", "tags", "is_answered")
    search_fields = ("title",)
    ordering = ("-created_at",)
    ordering_fields = (
        "created_at",
        "post__vote_count",
        "view_count",
    )

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action being performed.

        Returns:
            Serializer: The serializer class to be used.
        """
        if self.action in ("list", "create", "update", "partial_update", "destroy"):
            return QuestionSerializer
        elif self.action == "retrieve":
            return QuestionDetailSerializer

    @action(detail=True, methods=["get"], url_path="others")
    def others(self, request, *args, **kwargs):
        """
        Retrieves related and popular questions for a specific question.

        Args:
            request (Request): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response containing the related and popular questions.
        """
        question = self.get_object()
        related_questions = (
            Question.objects.exclude(id=question.id).filter(tags__in=question.tags.all()).distinct()[:5]
        )
        popular_questions = Question.objects.exclude(id=question.id).order_by("-view_count")[:5]
        related_serializer = QuestionSerializer(related_questions, many=True)
        popular_serializer = QuestionSerializer(popular_questions, many=True)
        return Response({"related_questions": related_serializer.data, "popular_questions": popular_serializer.data})


class AnswerViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing answers to questions in the forum.

    This viewset provides the following actions:
    - list: Retrieve a list of all answers.
    - create: Create a new answer.
    - retrieve: Retrieve a specific answer.
    - update: Update an existing answer.
    - partial_update: Partially update an existing answer.
    - destroy: Delete an existing answer.

    Only authenticated users can create, update, and delete answers.
    """

    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ("-created_at",)
    ordering_fields = (
        "created_at",
        "post__vote_count",
    )

    def get_permissions(self):
        if self.action in ("create",):
            return [IsAuthenticated()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()

    def get_queryset(self):
        return super().get_queryset().filter(question__slug=self.kwargs.get("question_slug"))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["question_slug"] = self.kwargs.get("question_slug")
        return context
