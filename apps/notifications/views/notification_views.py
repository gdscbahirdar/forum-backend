from django.contrib.auth import get_user_model
from django_filters import rest_framework as django_filters
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsOwnerOrSuperUser
from apps.notifications.models.notification_models import Notification, Subscription
from apps.notifications.serializers.notification_serializers import (
    NotificationReadOnlySerializer,
    SubscriptionSerializer,
)

User = get_user_model()


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing subscriptions.
    """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrSuperUser)
    filter_backends = (filters.OrderingFilter,)
    ordering = ("-created_at",)
    ordering_fields = ("created_at",)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only viewset for handling notifications.

    This viewset provides read-only operations for the Notification model.
    It filters the notifications based on the authenticated user and supports
    filtering, searching, and ordering.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationReadOnlySerializer
    permission_classes = (IsAuthenticated, IsOwnerOrSuperUser)
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("is_read",)
    search_fields = ("message",)
    ordering = ("-created_at",)
    ordering_fields = ("created_at",)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="unread_count")
    def unread_count(self, request):
        unread_count = self.get_queryset().filter(is_read=False).count()
        return Response({"unread_count": unread_count}, status=status.HTTP_200_OK)


class NotificationActionView(APIView):
    """
    View for performing actions on notifications.

    Supported actions:
    - mark_read: Marks selected notifications as read.
    - mark_unread: Marks selected notifications as unread.
    - delete_read: Deletes selected notifications that are marked as read.
    - delete_unread: Deletes selected notifications that are marked as unread.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrSuperUser)

    def post(self, request, action, *args, **kwargs):
        ids = request.data.get("ids", [])

        filters = {"user": request.user}
        if ids:
            filters["id__in"] = ids

        if action == "mark_as_read":
            Notification.objects.filter(**filters, is_read=False).update(is_read=True)

        elif action == "mark_as_unread":
            Notification.objects.filter(**filters, is_read=True).update(is_read=False)

        elif action == "delete_read":
            Notification.objects.filter(**filters, is_read=True).delete()

        elif action == "delete_unread":
            Notification.objects.filter(**filters, is_read=False).delete()

        elif action == "delete_any":
            Notification.objects.filter(**filters).delete()

        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
