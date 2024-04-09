import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.entities.models.faculty_models import Department, Faculty
from apps.entities.models.student_models import Student
from apps.entities.serializers.related_fields import DepartmentRelatedField, FacultyRelatedField
from apps.rbac.models.role_models import Role, UserRole
from apps.users.serializers.user_serializers import UserSerializer

User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.

    This serializer is used to serialize/deserialize Student objects.
    It includes the user information and other fields specific to the Student model.
    """

    user = UserSerializer()
    faculty = FacultyRelatedField(queryset=Faculty.objects.all())
    department = DepartmentRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Student
        fields = [
            "pk",
            "user",
            "faculty",
            "department",
            "year_in_school",
            "admission_date",
            "graduation_date",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request_user = CurrentUserDefault()

        if hasattr(request_user, "user_role") and request_user.user_role.role.name != "Super Admin":
            faculty = request_user.faculty_admin.faculty
            if attrs["faculty"] != faculty:
                raise serializers.ValidationError({"faculty": "You can only create students within your faculty."})

        username = attrs.get("user").get("username")
        username_regex = r"^(bdu)?\d{7}$"

        if not re.match(username_regex, username):
            raise serializers.ValidationError(
                {"username": "Username must be in the format 'bdu1234567' or '1234567'."}
            )

        if not username.startswith("bdu"):
            attrs["user"]["username"] = f"bdu{username}"

        if Student.objects.filter(user__username=attrs["user"]["username"]).exists():
            raise serializers.ValidationError({"username": "Student is already registered."})

        if User.objects.filter(username=attrs["user"]["username"]).exists():
            raise serializers.ValidationError({"username": "Username is already taken."})

        if attrs.get("admission_date") >= attrs.get("graduation_date"):
            raise serializers.ValidationError({"admission_date": "Admission date must be before graduation date."})

        if attrs.get("year_in_school") > 5:
            raise serializers.ValidationError({"year_in_school": "Year in school must not be greater than 5."})

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
