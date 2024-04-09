from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.forum.models.qa_models import Question, Answer
from apps.forum.serializers.post_serializers import QuestionSerializer, AnswerSerializer, QuestionDetailSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action in ("list", "create", "update", "partial_update", "destroy"):
            return QuestionSerializer
        elif self.action == "retrieve":
            return QuestionDetailSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)
