from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.entities.models.faculty_models import Faculty


class SuperAdmin(BaseModel):
    """
    Represents a super admin in the system.

    Attributes:
        user (User): The user associated with the super admin.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="super_admin", on_delete=models.CASCADE)


class FacultyAdmin(BaseModel):
    """
    Represents a faculty admin.

    Attributes:
        user (User): The user associated with the faculty admin.
        faculty (Faculty): The faculty where the user is admin of.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="faculty_admin", on_delete=models.CASCADE)
    faculty = models.OneToOneField(Faculty, related_name="faculty_admin", on_delete=models.CASCADE)
