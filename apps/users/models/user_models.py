from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_first_time_login = models.BooleanField(
        default=True, help_text="If true, user will be redirected to change password after login."
    )

    REQUIRED_FIELDS = ["first_name", "middle_name", "last_name"]

    def __str__(self):
        return self.username
