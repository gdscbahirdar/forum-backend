from rest_framework import serializers

from apps.entities.models.admin_models import FacultyAdmin
from apps.entities.models.faculty_models import Faculty
from apps.entities.serializers.related_fields import DepartmentRelatedField
from apps.entities.serializers.related_fields import FacultyRelatedField


class FacultySerializer(serializers.ModelSerializer):
    """
    Serializer for the Faculty model.
    """

    departments = DepartmentRelatedField(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = (
            "pk",
            "name",
            "departments",
            "created_at",
            "updated_at",
        )


class FacultyAdminSerializer(serializers.ModelSerializer):
    """
    Serializer for the FacultyAdmin model.
    """

    faculty = FacultyRelatedField(queryset=Faculty.objects.all())

    class Meta:
        model = FacultyAdmin
        fields = (
            "pk",
            "faculty",
            "created_at",
            "updated_at",
        )
