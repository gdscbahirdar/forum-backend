from django.db import models

from apps.common.models import BaseModel


class Faculty(BaseModel):
    """
    Represents a faculty in the system.

    Attributes:
        name (str): The name of the faculty.
        description (str): A description of the faculty.
    """

    FACULTY_NAME_CHOICES = (("FACULTY OF COMPUTING", "Faculty of Computing"),)

    name = models.CharField(max_length=255, unique=True, choices=FACULTY_NAME_CHOICES)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Faculties"

    def __str__(self):
        return self.name


class Department(BaseModel):
    """
    Represents a department in a faculty.

    Attributes:
        name (str): The name of the department.
        description (str): A description of the department.
        faculty (Faculty): The faculty to which the department belongs.
    """

    DEPARTMENT_NAME_CHOICES = (
        ("COMPUTER SCIENCE", "Computer Science"),
        ("INFORMATION TECHNOLOGY", "Information Technology"),
        ("SOFTWARE ENGINEERING", "Software Engineering"),
        ("INFORMATION SYSTEMS", "Information Systems"),
        ("CYBER SECURITY", "Cyber Security"),
    )

    name = models.CharField(max_length=255, unique=True, choices=DEPARTMENT_NAME_CHOICES)
    description = models.TextField(blank=True)
    faculty = models.ForeignKey(Faculty, related_name="departments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.faculty}"
