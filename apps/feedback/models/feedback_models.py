from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Feedback(BaseModel):
    """
    Feedback model.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL, related_name="feedback"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"Feedback by {self.user} - {self.title}"


class FeedbackReply(BaseModel):
    """
    Feedback reply model.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL, related_name="feedback_replies"
    )
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="replies")
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Feedback replies"

    def __str__(self):
        return f"{self.user} replied to {self.feedback.title}"
