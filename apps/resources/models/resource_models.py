from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.forum.models.qa_meta_models import Tag
from apps.common.models import BaseModel
from apps.forum.models.qa_meta_models import Comment, Vote, Bookmark, ViewTracker


def resource_directory_path(instance, filename):
    return f"resources/user_{instance.resource.uploader.id}/{filename}"


class ResourceCategory(BaseModel):
    name = models.CharField(max_length=100)
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
        uploader (User): The user who uploaded the resource.
        categories (QuerySet): The categories associated with the resource.
        tags (QuerySet): The tags associated with the resource.
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources")
    categories = models.ManyToManyField(ResourceCategory, blank=True, related_name="resources")
    tags = models.ManyToManyField(Tag, blank=True, related_name="resources")
    comments = GenericRelation(Comment)
    votes = GenericRelation(Vote, related_query_name="resource")
    bookmarks = GenericRelation(Bookmark, related_query_name="resource")
    view_count = models.PositiveIntegerField(default=0)
    views = GenericRelation(ViewTracker, related_query_name="resource")

    def __str__(self):
        return self.title


class ResourceFile(BaseModel):
    """
    Represents a file associated with a resource.

    Attributes:
        resource (Resource): The resource that this file belongs to.
        file (FileField): The file field that stores the uploaded file.
    """

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=resource_directory_path)

    def __str__(self):
        return f"{self.resource.title} - File"
