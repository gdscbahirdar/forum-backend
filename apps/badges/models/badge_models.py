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

    name = models.CharField(max_length=100, unique=True, help_text="Name of the badge")
    description = models.TextField(help_text="Description of the badge")
    level = models.IntegerField(choices=BadgeLevel.choices, help_text="Level of the badge")

    def __str__(self) -> str:
        return f"{self.name} - {self.level}"


class UserBadge(BaseModel):
    """
    A model to link users with the badges they have earned.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="users")

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "badge"), name="userbadge__1")]

    def __str__(self) -> str:
        return f"{self.user} - {self.badge}"


class DailyUserReputation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_reputations")
    date = models.DateField(auto_now_add=True)
    reputation = models.IntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "date"), name="dailyuserreputation__1")]

    def __str__(self):
        return f"{self.user} - {self.date} - {self.reputation} points"
