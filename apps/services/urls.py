from django.urls import path

from apps.services.views.ai_views import GenerateTextView

app_name = "services"

urlpatterns = [
    path("ai/generate_text/", GenerateTextView.as_view(), name="generate_text"),
]
