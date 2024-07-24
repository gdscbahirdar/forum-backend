from datetime import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.db import transaction
from django_filters import rest_framework as django_filters
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.entities.models.faculty_models import Department, Faculty
from apps.entities.models.student_models import Student
from apps.entities.serializers.entity_serializers import EntitySerializer
from apps.entities.utils import generate_password
from apps.rbac.models.role_models import Role, UserRole
from apps.rbac.permissions import IsUserSuperAdmin, IsUserSuperAdminOrFacultyAdmin

User = get_user_model()


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="entity_type",
            description="Type of entity. Options are `student`, `teacher`, `faculty_admin`",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
        )
    ]
)
class EntityViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing entities.

    This viewset provides CRUD operations for entities and applies permissions based on the entity type.

    Attributes:
        permission_classes (tuple): A tuple of permission classes to apply for the viewset.
        serializer_class (Serializer): The serializer class to use for serializing and deserializing entities.

    Methods:
        get_permissions(): Returns the permission classes based on the action and entity type.
        get_queryset(): Returns the queryset of entities based on the entity type and user role.
        get_serializer_context(): Overrides the default method to add the 'entity_type' to the serializer context.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = EntitySerializer
    filter_backends = (
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = (
        "student__faculty",
        "student__department",
        "student__department__name",
        "student__year_in_school",
        "teacher__faculty",
        "teacher__departments",
    )
    search_fields = ("username", "first_name", "middle_name", "last_name")
    ordering_fields = ("username",)
    ordering = ("username",)

    def get_permissions(self):
        """
        Returns the permission classes based on the action and entity type.

        If the action is 'create' and the entity type is 'faculty_admin', adds 'IsUserSuperAdmin' permission class.
        Otherwise, adds 'IsUserSuperAdminOrFacultyAdmin' permission class.

        Returns:
            tuple: A tuple of permission classes.
        """
        if self.action == "create":
            if self.kwargs.get("entity_type") == "faculty_admin":
                self.permission_classes += (IsUserSuperAdmin,)
            else:
                self.permission_classes += (IsUserSuperAdminOrFacultyAdmin,)
        else:
            self.permission_classes += (IsUserSuperAdminOrFacultyAdmin,)

        return super().get_permissions()

    def get_queryset(self):
        """
        Returns the queryset of entities based on the entity type and user role.

        Filters the queryset based on the entity type.
        If the user has a 'user_role' attribute and it's not 'Super Admin', filters by faculty.

        Returns:
            QuerySet: The filtered queryset of entities.
        """
        entity_type = self.kwargs.get("entity_type")
        if entity_type is None:
            return User.objects.none()

        filter = {f"{entity_type}__isnull": False}
        queryset = User.objects.filter(**filter)

        if hasattr(self.request.user, "user_role") and self.request.user.user_role.role.name != "Super Admin":
            faculty = self.request.user.faculty_admin.faculty
            filter = {f"{entity_type}__faculty": faculty}
            queryset = queryset.filter(**filter)

        return queryset

    def get_serializer_context(self):
        """
        Overrides the default method to add the 'entity_type' to the serializer context.

        Returns:
            dict: The serializer context with the 'entity_type' added.
        """
        context = super().get_serializer_context()
        entity_type = self.kwargs.get("entity_type")
        context.update({"entity_type": entity_type})
        return context


class UploadStudents(APIView):
    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            return None

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")

        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_extension = file_obj.name.split(".")[-1].lower()
        if file_extension not in ["xlsx", "xls", "csv"]:
            return Response(
                {"error": "Unsupported file type. Only Excel and CSV files are accepted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if file_extension in ["xlsx", "xls"]:
                df = pd.read_excel(file_obj)
            elif file_extension == "csv":
                df = pd.read_csv(file_obj)

            required_columns = {
                "username",
                "first_name",
                "middle_name",
                "last_name",
                "gender",
                "faculty",
                "department",
                "year_in_school",
                "admission_date",
                "graduation_date",
            }
            if not required_columns.issubset(df.columns):
                print(df.columns)
                return Response(
                    {"error": "All fields are required in the file."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            errors = []
            success_count = 0

            # TODO This should be a background task (Use Celery)
            for index, entry in df.iterrows():
                error = {}
                if not all([entry[col] for col in required_columns]):
                    error["row"] = index + 1
                    error["message"] = "Missing required fields"
                    errors.append(error)
                    continue

                if User.objects.filter(username=entry["username"]).exists():
                    error["row"] = index + 1
                    error["message"] = "Username already exists"
                    errors.append(error)
                    continue

                admission_date = self.parse_date(entry["admission_date"])
                graduation_date = self.parse_date(entry["graduation_date"])

                if not admission_date or not graduation_date:
                    error["row"] = index + 1
                    error["message"] = "Invalid date format"
                    errors.append(error)
                    continue

                first_name = entry["first_name"]
                middle_name = entry["middle_name"]
                last_name = entry["last_name"]

                password = generate_password(last_name)

                with transaction.atomic():
                    try:
                        user = User.objects.create_user(
                            first_name=first_name,
                            middle_name=middle_name,
                            last_name=last_name,
                            gender=entry["gender"],
                            username=entry["username"],
                            password=password,
                            is_first_time_login=True,
                        )
                        faculty = Faculty.objects.get(name=entry["faculty"])
                        department = Department.objects.get(name=entry["department"])
                        Student.objects.create(
                            user=user,
                            faculty=faculty,
                            department=department,
                            year_in_school=entry["year_in_school"],
                            admission_date=admission_date,
                            graduation_date=graduation_date,
                        )
                        role = Role.objects.get(name="Student")
                        UserRole.objects.create(user=user, role=role)
                        success_count += 1
                    except Exception:
                        error["row"] = index + 1
                        error["message"] = "Something went wrong."
                        errors.append(error)

            # TODO Allow users to download error log

            return Response(
                {
                    "message": f"{success_count} students created successfully. {len(errors)} entries failed.",
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception:
            return Response(
                {"error": "Something went wrong. Please try again later."},
                status=status.HTTP_400_BAD_REQUEST,
            )
