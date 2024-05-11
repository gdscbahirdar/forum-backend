from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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

    REQUIRED_FIELDS = ["first_name", "middle_name", "last_name"]

    def __str__(self):
        return self.username
