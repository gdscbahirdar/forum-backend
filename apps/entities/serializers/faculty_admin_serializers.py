from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.entities.models.admin_models import FacultyAdmin
from apps.rbac.models.role_models import Role, UserRole
from apps.users.models import User
from apps.users.serializers.user_serializers import UserSerializer


class FacultyAdminSerializer(serializers.ModelSerializer):
    """
    Serializer for the FacultyAdmin model.

    This serializer is used to serialize/deserialize FacultyAdmin objects.
    It includes the user information and the faculty where the faculty admin is assigned to.
    """

    user = serializers.JSONField(write_only=True)

    class Meta:
        model = FacultyAdmin
        fields = ["user", "faculty"]

    def validate(self, attrs):
        faculty = attrs.get("faculty")
        if FacultyAdmin.objects.filter(faculty=faculty).exists():
            raise serializers.ValidationError("A faculty admin already exists for this faculty.")

        user_data = attrs.get("user")
        if isinstance(user_data, dict):
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            attrs["user"] = user_serializer.validated_data
        elif isinstance(user_data, int):
            try:
                attrs["user"] = User.objects.get(pk=user_data)
            except User.DoesNotExist:
                raise serializers.ValidationError({"user": "No such user exists."})
        else:
            raise serializers.ValidationError({"user": "Invalid user data."})

        if FacultyAdmin.objects.filter(faculty=attrs["faculty"]).exists():
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
        faculty_admin = FacultyAdmin.objects.create(**validated_data)
        role = Role.objects.get(name="Faculty Admin")
        UserRole.objects.create(user=faculty_admin.user, role=role)

        return faculty_admin
