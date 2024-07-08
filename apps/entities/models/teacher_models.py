from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.entities.models.faculty_models import Department, Faculty


class Teacher(BaseModel):
    """
    Represents a teacher in the system.

    Attributes:
        user (User): The user associated with the teacher.
        faculty (Faculty): The faculty to which the teacher belongs.
        departments (QuerySet): The departments associated with the teacher.
        first_name (str): The first name of the teacher.
        middle_name (str): The middle name of the teacher.
        last_name (str): The last name of the teacher.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="teacher", on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, related_name="teachers", on_delete=models.CASCADE)
    departments = models.ManyToManyField(Department)

    def __str__(self):
        return f"Teacher: {self.user}, Faculty: {self.faculty}"
