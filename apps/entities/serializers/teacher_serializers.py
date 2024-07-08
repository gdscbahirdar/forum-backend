from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.entities.models.faculty_models import Department
from apps.entities.models.faculty_models import Faculty
from apps.entities.models.teacher_models import Teacher
from apps.entities.serializers.related_fields import DepartmentRelatedField
from apps.entities.serializers.related_fields import FacultyRelatedField

User = get_user_model()


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.
    """

    faculty = FacultyRelatedField(queryset=Faculty.objects.all())
    departments = DepartmentRelatedField(queryset=Department.objects.all(), many=True)

    class Meta:
        model = Teacher
        fields = (
            "pk",
            "faculty",
            "departments",
            "created_at",
            "updated_at",
        )
