from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.entities.models.faculty_models import Department, Faculty


class Student(BaseModel):
    """
    Represents a student in the system.

    Attributes:
        user (User): The user associated with the student.
        faculty (Faculty): The faculty the student belongs to.
        department (Department): The department the student belongs to.
        first_name (str): The first name of the student.
        middle_name (str): The middle name of the student.
        last_name (str): The last name of the student.
        year_in_school (int): The year the student is in.
        admission_date (date): The date of admission for the student.
        graduation_date (date): The expected graduation date for the student.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="student", on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, related_name="students", on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name="students", on_delete=models.CASCADE)
    year_in_school = models.PositiveSmallIntegerField()
    admission_date = models.DateField()
    graduation_date = models.DateField()

    def __str__(self):
        return f"Student: {self.user}, Department: {self.department}"
