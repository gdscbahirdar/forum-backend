from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.entities.models.teacher_models import Teacher
from apps.rbac.models.role_models import Role, UserRole
from apps.users.serializers.user_serializers import UserSerializer


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Teacher model.

    This serializer is used to serialize/deserialize Teacher objects.
    It includes the user information and other fields specific to the Teacher model.
    """

    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ["user", "faculty", "departments", "first_name", "middle_name", "last_name"]

    def validate(self, attrs):
        request_user = CurrentUserDefault()

        if hasattr(request_user, "user_role") and request_user.user_role.role.name != "Super Admin":
            faculty_admin = request_user.faculty_admin.faculty
            if attrs["faculty"] != faculty_admin:
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
        validated_data["first_name"] = user_data.get("first_name")
        validated_data["middle_name"] = user_data.get("middle_name")
        validated_data["last_name"] = user_data.get("last_name")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        teacher.departments.set(departments)
        role = Role.objects.get(name="Teacher")
        UserRole.objects.create(user=user, role=role)
        return teacher
