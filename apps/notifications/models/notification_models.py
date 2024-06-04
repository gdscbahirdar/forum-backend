from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.common.models import BaseModel


class Notification(BaseModel):
    """
    Represents a notification for a user.
    """

    class Level(models.TextChoices):
        INFO = "info"
        SUCCESS = "success"
        WARNING = "warning"
        ERROR = "error"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    level = models.CharField(choices=Level.choices, max_length=10, default=Level.INFO)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    target_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="notify_target", blank=True, null=True
    )
    target_object_id = models.UUIDField(blank=True, null=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    def __str__(self):
        return f"Notification for {self.user}: {self.title}"

    def mark_as_read(self):
        """
        Marks the notification as read.
        """
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        """
        Marks the notification as unread.
        """
        self.is_read = False
        self.save()


class Subscription(BaseModel):
    """
    Represents a subscription made by a user to a target object.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    target_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="subscribe_target", blank=True, null=True
    )
    target_object_id = models.UUIDField(blank=True, null=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    def __str__(self):
        return f"Subscription by {self.user} to {self.target}"
