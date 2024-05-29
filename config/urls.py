from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("rest_framework.urls", namespace="rest_framework")),  # DRF Browsable API
    path("api/users/", include("apps.users.urls")),
    path("api/entities/", include("apps.entities.urls", namespace="entities")),
    path("api/forum/", include("apps.forum.urls", namespace="forum")),
    path("api/", include("apps.resources.urls", namespace="resources")),
    path("api/", include("apps.common.urls", namespace="common")),
    path("api/", include("apps.badges.urls", namespace="badges")),
    path("api/", include("apps.services.urls", namespace="services")),
]

# Media Assets
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Schema URLs
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
