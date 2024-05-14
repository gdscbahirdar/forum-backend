from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.badges.models.badge_models import Badge, UserBadge


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

    def assign_badge(self, badge_name):
        badge = Badge.objects.filter(name=badge_name).first()
        if not badge:
            return None
        user_badge = UserBadge.objects.filter(user=self, badge=badge).first()
        return UserBadge.objects.create(user=self, user_badge=user_badge) if not user_badge else user_badge
