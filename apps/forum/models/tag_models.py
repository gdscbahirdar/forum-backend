from django.db import models

from apps.common.models import BaseModel


class Tag(BaseModel):
    """
    Represents a tag for categorizing forum posts.

    Attributes:
        name (str): The name of the tag.
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
