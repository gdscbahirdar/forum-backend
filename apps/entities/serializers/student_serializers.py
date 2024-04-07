import re

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.entities.models.student_models import Student
from apps.rbac.models.role_models import Role, UserRole
from apps.users.serializers.user_serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.

    This serializer is used to serialize/deserialize Student objects.
    It includes the user information and other fields specific to the Student model.
    """

    user = UserSerializer()

    class Meta:
        model = Student
        fields = [
            "user",
            "faculty",
            "department",
            "first_name",
            "middle_name",
            "last_name",
            "year_in_school",
            "admission_date",
            "graduation_date",
        ]
        read_only_fields = ["first_name", "middle_name", "last_name"]

    def validate(self, attrs):
        request_user = CurrentUserDefault()

        if hasattr(request_user, "user_role") and request_user.user_role.role.name != "Super Admin":
            faculty_admin = request_user.faculty_admin.faculty
            if attrs["faculty"] != faculty_admin:
                raise serializers.ValidationError({"faculty": "You can only create students within your faculty."})

        username = attrs.get("user").get("username")
        username_regex = r"^(bdu)?\d{7}$"

        if not re.match(username_regex, username):
            raise serializers.ValidationError(
                {"username": "Username must be in the format 'bdu1234567' or '1234567'."}
            )

        if not username.startswith("bdu"):
            attrs["user"]["username"] = f"bdu{username}"

        return attrs

    def create(self, validated_data):
        """
        Create a new student instance.

        Args:
            validated_data (dict): The validated data for creating the student.

        Returns:
            student (Student): The created student instance.
        """
        user_data = validated_data.pop("user")
        validated_data["first_name"] = user_data.get("first_name")
        validated_data["middle_name"] = user_data.get("middle_name")
        validated_data["last_name"] = user_data.get("last_name")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student = Student.objects.create(user=user, **validated_data)
        role = Role.objects.get(name="Student")
        UserRole.objects.create(user=user, role=role)
        return student
