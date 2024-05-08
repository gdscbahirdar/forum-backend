from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Tag(BaseModel):
    """
    Represents a tag for categorizing forum posts.

    Attributes:
        name (str): The name of the tag.
        description (str): A description of the tag.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="votes", on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=8, choices=VOTE_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "content_type", "object_id"), name="vote__1")]

    def __str__(self):
        return f"{self.user} voted {self.vote_type} on {self.content_type.model}"


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
    vote_count = models.IntegerField(default=0)
    votes = GenericRelation(Vote, related_query_name="comment")

    def __str__(self):
        return f"Comment by {self.user}"


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
