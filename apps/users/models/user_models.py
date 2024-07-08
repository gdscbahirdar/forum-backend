from datetime import date
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.badges.models.badge_models import Badge, DailyUserReputation, UserBadge


def avatar_directory_path(instance, filename):
    return f"avatars/user_{instance.id}/{filename}"


class User(AbstractUser):
    GENDER_CHOICES = (("M", "M"), ("F", "F"))

    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_first_time_login = models.BooleanField(
        default=True, help_text="If true, user will be redirected to change password after login."
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    bio = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=avatar_directory_path)
    phone_number = PhoneNumberField(blank=True)
    reputation = models.IntegerField(
        default=1, help_text="Reputation points earned by the user through various activities. Default is one."
    )

    REQUIRED_FIELDS = ["first_name", "middle_name", "last_name"]

    def __str__(self):
        return self.username

    @property
    def get_fullname(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def add_reputation(self, points: int) -> int:
        daily_reputation, _ = DailyUserReputation.objects.get_or_create(user=self, date=date.today())
        if daily_reputation.reputation + points > 200:
            points = 200 - daily_reputation.reputation
        self.reputation += points
        self.save(update_fields=["reputation"])

        # Add points to daily reputation
        daily_reputation.reputation += points
        daily_reputation.save(update_fields=["reputation"])
        return self.reputation

    def subtract_reputation(self, points: int) -> int:
        new_reputation = max(1, self.reputation - points)
        self.reputation = new_reputation
        self.save(update_fields=["reputation"])

        # Subtract points from daily reputation
        daily_reputation, _ = DailyUserReputation.objects.get_or_create(user=self, date=date.today())
        new_daily_reputation = max(0, daily_reputation.reputation - points)
        daily_reputation.reputation = new_daily_reputation
        daily_reputation.save(update_fields=["reputation"])
        return self.reputation

    def assign_badge(self, badge_name: str) -> Optional[UserBadge]:
        badge = Badge.objects.filter(name=badge_name).first()
        if not badge:
            return None

        if user_badge := UserBadge.objects.filter(user=self, badge=badge).first():
            return user_badge

        return UserBadge.objects.create(user=self, badge=badge)
