from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.common.models import BaseModel


class ViewTracker(BaseModel):
    """
    Represents a view made by a user.

    Attributes:
        user (ForeignKey): The user who made the view.
        content_type (ForeignKey): The content type of the viewed object.
        object_id (UUIDField): The ID of the viewed object.
        content_object (GenericForeignKey): The viewed object.

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="views", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "content_type", "object_id"), name="view__1")]

    def __str__(self):
        return f"{self.user} viewed {self.content_type.model} -> {self.object_id}"
