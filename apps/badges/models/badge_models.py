from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Badge(BaseModel):
    """
    Represents a badge in the system.
    """

    class BadgeLevel(models.IntegerChoices):
        GOLD = 1
        SILVER = 2
        BRONZE = 3

    name = models.CharField(max_length=100, help_text="Name of the badge")
    description = models.TextField(help_text="Description of the badge")
    points = models.IntegerField(help_text="Points required to achieve the badge")
    level = models.IntegerField(choices=BadgeLevel, help_text="Level of the badge")


class UserBadge(BaseModel):
    """
    A model to link users with the badges they have earned.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="users")
