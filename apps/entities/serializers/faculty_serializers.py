from rest_framework import serializers

from apps.entities.models.admin_models import FacultyAdmin
from apps.entities.models.faculty_models import Faculty
from apps.entities.serializers.related_fields import FacultyRelatedField
from apps.rbac.models.role_models import Role, UserRole
from apps.users.serializers.user_serializers import UserSerializer
from apps.entities.serializers.related_fields import DepartmentRelatedField


class FacultyAdminSerializer(serializers.ModelSerializer):
    """
    Serializer for the FacultyAdmin model.

    This serializer is used to serialize/deserialize FacultyAdmin objects.
    It includes the user information and the faculty where the faculty admin is assigned to.
    """

    user = UserSerializer()
    faculty = FacultyRelatedField(queryset=Faculty.objects.all())

    class Meta:
        model = FacultyAdmin
        fields = [
            "pk",
            "user",
            "faculty",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        faculty = attrs.get("faculty")
        if hasattr(faculty, "faculty_admin"):
            raise serializers.ValidationError({"faculty": "A faculty admin already exists for this faculty."})

        return attrs

    def create(self, validated_data):
        """
        Create a new FacultyAdmin instance.

        Args:
            validated_data (dict): The validated data for creating the FacultyAdmin object.

        Returns:
            FacultyAdmin: The created FacultyAdmin object.
        """
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        faculty_admin = FacultyAdmin.objects.create(user=user, **validated_data)
        role = Role.objects.get(name="Faculty Admin")
        UserRole.objects.create(user=faculty_admin.user, role=role)
        return faculty_admin


class FacultySerializer(serializers.ModelSerializer):
    """
    Serializer for the Faculty model.

    This serializer is used to serialize/deserialize Faculty objects.
    It includes the departments related to the faculty.
    """

    departments = DepartmentRelatedField(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = [
            "pk",
            "name",
            "departments",
            "created_at",
            "updated_at",
        ]
