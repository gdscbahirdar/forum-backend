from rest_framework import serializers

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
            "student_id",
            "first_name",
            "middle_name",
            "last_name",
            "year_in_school",
            "admission_date",
            "graduation_date",
        ]

    def validate(self, attrs):
        request_user = self.context["request"].user

        if hasattr(request_user, "user_role") and request_user.user_role.role.name != "Super Admin":
            faculty_admin = request_user.faculty_admin.faculty
            if attrs["faculty"] != faculty_admin:
                raise serializers.ValidationError({"faculty": "You can only create students within your faculty."})

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
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student = Student.objects.create(user=user, **validated_data)
        role = Role.objects.get(name="Student")
        UserRole.objects.create(user=user, role=role)
        return student
