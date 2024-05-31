from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Bookmark(BaseModel):
    """
    Represents a bookmark made by a user on a forum post. This can be on either a question or an answer.

    Attributes:
        user (ForeignKey): The user who made the bookmark.
        content_type (ForeignKey): The content type of the bookmarked object.
        object_id (UUIDField): The ID of the bookmarked object.
        content_object (GenericForeignKey): The bookmarked object.

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="bookmarks", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "content_type", "object_id"), name="bookmark__1")]

    def __str__(self):
        return f"{self.user} bookmarked on {self.content_type.model}"
