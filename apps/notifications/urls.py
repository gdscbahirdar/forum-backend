from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.notifications.views.notification_views import NotificationActionView
from apps.notifications.views.notification_views import NotificationReadOnlyViewSet
from apps.notifications.views.notification_views import SubscriptionViewSet

app_name = "notifications"

router = DefaultRouter()

router.register(r"notifications", NotificationReadOnlyViewSet)
router.register(r"subscriptions", SubscriptionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("notification_actions/<str:action>/", NotificationActionView.as_view(), name="notification_actions"),
]
