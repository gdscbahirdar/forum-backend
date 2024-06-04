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

subscription_list = SubscriptionViewSet.as_view({"get": "list", "post": "create"})
subscription_detail = SubscriptionViewSet.as_view({"get": "retrieve", "delete": "destroy"})

urlpatterns = [
    path("", include(router.urls)),
    path("subscriptions/", subscription_list, name="subscription_list"),
    path("subscriptions/<uuid:pk>/", subscription_detail, name="subscription_detail"),
    path("notification_actions/<str:action>/", NotificationActionView.as_view(), name="notification_actions"),
]
