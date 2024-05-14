from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django_filters import rest_framework as django_filters
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.forum.models.qa_meta_models import ViewTracker
from apps.forum.models.qa_models import Answer, Question
from apps.forum.permissions import IsOwnerOrReadOnly
from apps.forum.serializers.post_serializers import (
    AcceptAnswerSerializer,
    AnswerSerializer,
    QuestionDetailSerializer,
    QuestionSerializer,
)


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
        if self.action == "retrieve":
            return QuestionDetailSerializer
        return QuestionSerializer

    def retrieve(self, request, *args, **kwargs):
        question = self.get_object()

        content_type = ContentType.objects.get_for_model(Question)
        if not ViewTracker.objects.filter(
            user=request.user, content_type=content_type, object_id=question.pk
        ).exists():
            ViewTracker.objects.create(user=request.user, content_type=content_type, object_id=question.pk)
            question.view_count = F("view_count") + 1
            question.save(update_fields=["view_count"])

        return super().retrieve(request, *args, **kwargs)

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

    @action(detail=True, methods=["post"], url_path="accept_answer")
    def accept_answer(self, request, *args, **kwargs):
        serializer = AcceptAnswerSerializer(data=request.data)
        if serializer.is_valid():
            question = self.get_object()

            if request.user != question.post.user:
                return Response(
                    {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN
                )

            answer_id = serializer.validated_data["answer_id"]
            if not answer_id:
                return Response({"error": "Answer ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                answer = Answer.objects.get(id=answer_id, question=question)
            except Answer.DoesNotExist:
                return Response(
                    {"error": "No valid answer found for the provided ID."}, status=status.HTTP_404_NOT_FOUND
                )

            if question.accepted_answer and question.accepted_answer.id == answer.id:
                question.accepted_answer.is_accepted = False
                question.accepted_answer.save()
                question.is_answered = False
                question.accepted_answer = None
                question.save()
                return Response({"message": "Answer unaccepted successfully."}, status=status.HTTP_200_OK)

            if question.accepted_answer and question.accepted_answer.id != answer.id:
                question.accepted_answer.is_accepted = False
                question.accepted_answer.save()

            question.accepted_answer = answer
            question.is_answered = True
            question.save()

            answer.is_accepted = True
            answer.save()

            return Response({"message": "Answer accepted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def perform_destroy(self, instance):
        instance.question.answer_count = F("answer_count") - 1
        instance.question.save(update_fields=["answer_count"])
        return instance.delete()
