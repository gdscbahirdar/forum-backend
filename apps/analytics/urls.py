from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.analytics.views.analytics_views import AnalyticsViewSet

router = DefaultRouter()
router.register(r"analytics", AnalyticsViewSet, basename="analytics")

app_name = "analytics"

urlpatterns = [
    path("", include(router.urls)),
]
