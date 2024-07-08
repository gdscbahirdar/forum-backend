import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from apps.entities.models.admin_models import FacultyAdmin
from apps.entities.models.student_models import Student
from apps.entities.models.teacher_models import Teacher
from apps.entities.serializers.faculty_serializers import FacultyAdminSerializer
from apps.entities.serializers.student_serializers import StudentSerializer
from apps.entities.serializers.teacher_serializers import TeacherSerializer
from apps.entities.utils import generate_password
from apps.rbac.models.role_models import Role
from apps.rbac.models.role_models import UserRole

User = get_user_model()


class EntitySerializer(serializers.ModelSerializer):
    """
    Serializer for the Entity model.
    """

    class Meta:
        model = User
        fields = ("pk", "username", "first_name", "middle_name", "last_name", "gender", "is_first_time_login")
        read_only_fields = ("is_first_time_login",)

    def __init__(self, *args, **kwargs):
        context = kwargs.pop("context", {})
        super().__init__(*args, **kwargs)

        entity_type = context.get("entity_type", None)

        # Create a copy of Meta.fields
        self.fields_to_include = list(self.Meta.fields)

        if entity_type == "student":
            self.fields["student"] = StudentSerializer()
            self.fields_to_include.append("student")
        elif entity_type == "teacher":
            self.fields["teacher"] = TeacherSerializer()
            self.fields_to_include.append("teacher")
        elif entity_type == "faculty_admin":
            self.fields["faculty_admin"] = FacultyAdminSerializer()
            self.fields_to_include.append("faculty_admin")

        # Use the copy of Meta.fields for this instance
        for field in self.fields.keys():
            if field not in self.fields_to_include:
                self.fields.pop(field)

    def validate(self, attrs):
        request_user = CurrentUserDefault()

        if hasattr(request_user, "user_role") and request_user.user_role.role.name != "Super Admin":
            faculty = request_user.faculty_admin.faculty
            if attrs["faculty"] != faculty:
                raise serializers.ValidationError(
                    {"faculty": "You can only create students and teachers within your faculty."}
                )

        # Validate username for students
        if "student" in attrs:
            username = attrs.get("username")
            username_regex = r"^(bdu)?\d{7}$"

            if not re.match(username_regex, username):
                raise serializers.ValidationError(
                    {"username": "Username must be in the format 'bdu1234567' or '1234567'."}
                )

            if not username.startswith("bdu"):
                attrs["username"] = f"bdu{username}"

        return attrs

    def create(self, validated_data):
        student_data = validated_data.pop("student", None)
        teacher_data = validated_data.pop("teacher", None)
        faculty_admin_data = validated_data.pop("faculty_admin", None)

        username = validated_data.pop("username")
        first_name = validated_data.pop("first_name")
        middle_name = validated_data.pop("middle_name")
        last_name = validated_data.pop("last_name")
        gender = validated_data.pop("gender")
        password = generate_password(last_name)
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gender=gender,
            password=password,
            is_first_time_login=True,
        )

        if student_data:
            Student.objects.create(user=user, **student_data)
            role = Role.objects.get(name="Student")
            UserRole.objects.create(user=user, role=role)
        elif teacher_data:
            departments = teacher_data.pop("departments", [])
            teacher = Teacher.objects.create(user=user, **teacher_data)
            teacher.departments.set(departments)
            role = Role.objects.get(name="Teacher")
            UserRole.objects.create(user=user, role=role)
        elif faculty_admin_data:
            FacultyAdmin.objects.filter(faculty=faculty_admin_data.get("faculty")).delete()
            FacultyAdmin.objects.create(user=user, **faculty_admin_data)
            role = Role.objects.get(name="Faculty Admin")
            UserRole.objects.create(user=user, role=role)

        return user

    def update(self, instance, validated_data):
        student_data = validated_data.pop("student", None)
        teacher_data = validated_data.pop("teacher", None)
        faculty_admin_data = validated_data.pop("faculty_admin", None)

        instance = super().update(instance, validated_data)

        if student_data:
            student = instance.student
            for attr, value in student_data.items():
                setattr(student, attr, value)
            student.save()
        elif teacher_data:
            teacher = instance.teacher
            departments = teacher_data.pop("departments", [])
            for attr, value in teacher_data.items():
                setattr(teacher, attr, value)
            teacher.departments.set(departments)
            teacher.save()
        elif faculty_admin_data:
            faculty_admin = instance.faculty_admin
            for attr, value in faculty_admin_data.items():
                setattr(faculty_admin, attr, value)
            faculty_admin.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        optional_fields = ("student", "teacher", "faculty_admin")
        for field in optional_fields:
            if field in representation and representation.get(field) is None:
                representation.pop(field)
        return representation
