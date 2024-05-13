import uuid

from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    """
    Base model for most models in the project.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


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
