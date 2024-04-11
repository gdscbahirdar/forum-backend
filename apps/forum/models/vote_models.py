from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.common.models import BaseModel


class Vote(BaseModel):
    """
    Represents a vote made by a user on a specific content(i.e. Question, Answer, Comment, etc.)

    Fields:
        user (ForeignKey): Foreign key to the user who made the vote.
        vote_type (CharField): Type of vote (upvote or downvote).
        content_type (ForeignKey): Foreign key to the content type.
        object_id (UUIDField): UUID of the content object.
        content_object (GenericForeignKey): Generic foreign key to the content object.
    """

    UPVOTE = "upvote"
    DOWNVOTE = "downvote"
    VOTE_CHOICES = [
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=8, choices=VOTE_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = ("user", "content_type", "object_id")

    def __str__(self):
        return f"{self.user} voted {self.vote_type} on {self.content_type.model}"
