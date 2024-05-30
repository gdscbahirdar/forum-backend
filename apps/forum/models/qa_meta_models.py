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
