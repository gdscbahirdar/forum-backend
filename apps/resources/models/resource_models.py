from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.forum.models.qa_meta_models import Tag
from apps.common.models import BaseModel
from apps.content_actions.models.bookmark_models import Bookmark
from apps.content_actions.models.comment_models import Comment
from apps.content_actions.models.vote_models import Vote
from apps.content_actions.models.view_models import ViewTracker
from apps.resources.constants import ResourceConstants


def resource_directory_path(instance, filename):
    return f"resources/user_{instance.resource.user.id}/{filename}"


class ResourceCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Resource Categories"

    def __str__(self):
        return self.name


class Resource(BaseModel):
    """
    Represents a resource in the system.

    Attributes:
        title (str): The title of the resource.
        description (str): The description of the resource.
        user (User): The user who uploaded the resource.
        categories (QuerySet): The categories associated with the resource.
        tags (QuerySet): The tags associated with the resource.
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources")
    categories = models.ManyToManyField(ResourceCategory, blank=True, related_name="resources")
    tags = models.ManyToManyField(Tag, blank=True, related_name="resources")
    comments = GenericRelation(Comment)
    vote_count = models.IntegerField(default=0)
    votes = GenericRelation(Vote, related_query_name="resource")
    bookmarks = GenericRelation(Bookmark, related_query_name="resource")
    view_count = models.PositiveIntegerField(default=0)
    views = GenericRelation(ViewTracker, related_query_name="resource")
    score = models.IntegerField(default=0, help_text="The score of the post. upvotes - downvotes.")

    def __str__(self):
        return self.title

    def update_score(self):
        upvotes = self.votes.filter(vote_type=Vote.UPVOTE).count()
        downvotes = self.votes.filter(vote_type=Vote.DOWNVOTE).count()
        self.score = upvotes - downvotes
        self.save(update_fields=["score"])

    def evaluate_score_badges(self):
        if self.score >= 100:
            self.user.assign_badge("Great Resource")
        elif self.score >= 25:
            self.user.assign_badge("Good Resource")
        elif self.score >= 10:
            self.user.assign_badge("Nice Resource")


class ResourceFile(BaseModel):
    """
    Represents a file associated with a resource.

    Attributes:
        resource (Resource): The resource that this file belongs to.
        file (FileField): The file field that stores the uploaded file.
    """

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=resource_directory_path)
    file_name = models.CharField(blank=True, null=True)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    file_size = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding and self.file:
            self.file_type = ResourceConstants.FILE_TYPE_MAPPING[self.file.file.content_type]
            self.file_size = self.file.size
            self.file_name = self.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.resource.title} - File"
