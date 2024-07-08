from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsOwnerOrSuperUser
from apps.feedback.models.feedback_models import Feedback, FeedbackReply
from apps.feedback.serializers.feedback_serializers import FeedbackReplySerializer, FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing feedback.

    This viewset provides CRUD operations for the Feedback model.
    """

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = ("-created_at",)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsOwnerOrSuperUser,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FeedbackReplyViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing feedback replies.

    This viewset provides CRUD operations for feedback replies.
    """

    serializer_class = FeedbackReplySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ("-created_at",)

    def get_queryset(self):
        queryset = FeedbackReply.objects.all()
        feedback_id = self.kwargs.get("feedback_id")
        if feedback_id is not None:
            queryset = queryset.filter(feedback_id=feedback_id)

        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsOwnerOrSuperUser,)
        return super().get_permissions()

    def perform_create(self, serializer):
        feedback_id = self.kwargs.get("feedback_id")
        serializer.save(user=self.request.user, feedback_id=feedback_id)
