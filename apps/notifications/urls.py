from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.notifications.views.notification_views import (
    NotificationActionView,
    NotificationReadOnlyViewSet,
    SubscriptionViewSet,
)

app_name = "notifications"

router = DefaultRouter()

router.register(r"notifications", NotificationReadOnlyViewSet)
router.register(r"subscriptions", SubscriptionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("notification_actions/<str:action>/", NotificationActionView.as_view(), name="notification_actions"),
]
