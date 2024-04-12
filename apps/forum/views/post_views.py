from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.forum.models.qa_models import Answer, Question
from apps.forum.permissions import IsOwnerOrReadOnly
from apps.forum.serializers.post_serializers import AnswerSerializer, QuestionDetailSerializer, QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = ("-created_at",)

    def get_serializer_class(self):
        if self.action in ("list", "create", "update", "partial_update", "destroy"):
            return QuestionSerializer
        elif self.action == "retrieve":
            return QuestionDetailSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (AllowAny,)

    def get_permissions(self):
        if self.action in ("create",):
            return [IsAuthenticated()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["question_slug"] = self.kwargs.get("question_slug")
        return context
