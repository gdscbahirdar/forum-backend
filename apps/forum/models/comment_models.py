from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Comment(BaseModel):
    """
    Represents a comment made by a user on a forum post. This can be on either a question or an answer.

    Attributes:
        user (User): The user who made the comment.
        text (str): The body of the comment.
        content_type (ContentType): The type of the object (Question or Answer) this comment is associated with.
        object_id (UUIDField): The ID of the object this comment is associated with.
        content_object (GenericForeignKey): The generic link to either a Question or an Answer.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(_("Comment body"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Comment by {self.user}"
