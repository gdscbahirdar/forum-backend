from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.entities.models.faculty_models import Department, Faculty
from apps.entities.models.teacher_models import Teacher
from apps.entities.serializers.related_fields import DepartmentRelatedField, FacultyRelatedField
from apps.rbac.models.role_models import Role, UserRole
from apps.users.serializers.user_serializers import UserSerializer


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Teacher model.

    This serializer is used to serialize/deserialize Teacher objects.
    It includes the user information and other fields specific to the Teacher model.
    """

    user = UserSerializer()
    faculty = FacultyRelatedField(queryset=Faculty.objects.all())
    departments = DepartmentRelatedField(queryset=Department.objects.all(), many=True)

    class Meta:
        model = Teacher
        fields = [
            "pk",
            "user",
            "faculty",
            "departments",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request_user = CurrentUserDefault()

        if hasattr(request_user, "user_role") and request_user.user_role.role.name != "Super Admin":
            faculty = request_user.faculty_admin.faculty
            if attrs["faculty"] != faculty:
                raise serializers.ValidationError({"faculty": "You can only create teachers within your faculty."})

        return attrs

    def create(self, validated_data):
        """
        Create a new Teacher instance.

        Args:
            validated_data (dict): The validated data for creating the Teacher object.

        Returns:
            Teacher: The created Teacher object.
        """
        user_data = validated_data.pop("user")
        departments = validated_data.pop("departments")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        teacher.departments.set(departments)
        role = Role.objects.get(name="Teacher")
        UserRole.objects.create(user=user, role=role)
        return teacher
