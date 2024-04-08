from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.entities.models.admin_models import FacultyAdmin
from apps.entities.models.student_models import Student
from apps.entities.models.teacher_models import Teacher
from apps.entities.serializers.faculty_admin_serializers import FacultyAdminSerializer
from apps.entities.serializers.student_serializers import StudentSerializer
from apps.entities.serializers.teacher_serializers import TeacherSerializer
from apps.entities.utils import is_valid_uuid
from apps.rbac.permissions import IsUserSuperAdmin, IsUserSuperAdminOrFacultyAdmin


class EntityViewSet(viewsets.ViewSet):
    """
    A viewset for managing entities of different types.

    This viewset provides the following actions:
        - list: List entities based on entity_type.
        - create: Create an entity based on entity_type.

    The supported entity types are `student`, `teacher`, and `faculty_admin`.

    Permissions:
        - Only authenticated users with role `Super Admin` or `Faculty Admin` can access this viewset.
    """

    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            if self.kwargs.get("entity_type") == "faculty_admin":
                self.permission_classes += (IsUserSuperAdmin,)
            else:
                self.permission_classes += (IsUserSuperAdminOrFacultyAdmin,)
        else:
            self.permission_classes += (IsUserSuperAdminOrFacultyAdmin,)

        return super().get_permissions()

    def list(self, request, entity_type=None):
        """
        List entities based on entity_type.

        Parameters:
        - entity_type (str): The type of entity to list. Choices are `student`, `teacher`, and `faculty_admin`.

        Returns:
        - Response: A response containing the serialized data of the entities.
        """
        if entity_type == "student":
            queryset = Student.objects.all()
            serializer = StudentSerializer(queryset, many=True)
        elif entity_type == "teacher":
            queryset = Teacher.objects.all()
            serializer = TeacherSerializer(queryset, many=True)
        elif entity_type == "faculty_admin":
            queryset = FacultyAdmin.objects.all()
            serializer = FacultyAdminSerializer(queryset, many=True)
        else:
            return Response(
                {"error": "Invalid entity type. Choices are `student`, `teacher`, and `faculty_admin`"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if hasattr(request.user, "user_role") and request.user.user_role.role.name != "Super Admin":
            faculty = request.user.faculty_admin.faculty
            queryset = queryset.filter(faculty=faculty)

        return Response(serializer.data)

    def retrieve(self, request, entity_type=None, pk=None):
        """
        Retrieve an entity based on entity_type and pk.

        Parameters:
        - entity_type (str): The type of entity to retrieve. Choices are `student`, `teacher`, and `faculty_admin`.
        - pk (int): The primary key of the entity to retrieve.

        Returns:
        - Response: A response containing the serialized data of the entities.
        """
        if not is_valid_uuid(pk):
            return Response(
                {"error": "Invalid ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        model_classes = {
            "student": Student,
            "teacher": Teacher,
            "faculty_admin": FacultyAdmin,
        }
        serializer_classes = {
            "student": StudentSerializer,
            "teacher": TeacherSerializer,
            "faculty_admin": FacultyAdminSerializer,
        }
        model_class = model_classes.get(entity_type)
        serializer_class = serializer_classes.get(entity_type)

        if not model_class or not serializer_class:
            return Response(
                {"error": "Invalid entity type. Choices are `student`, `teacher`, and `faculty_admin`"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            entity = model_class.objects.get(pk=pk)
        except model_class.DoesNotExist:
            return Response(
                {"error": f"{entity_type.title()} with the provided ID does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if hasattr(request.user, "user_role") and request.user.user_role.role.name != "Super Admin":
            faculty = request.user.faculty_admin.faculty
            if entity.faculty != faculty:
                return Response(
                    {"error": "You do not have permission to view this entity."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = serializer_class(entity)
        return Response(serializer.data)

    def create(self, request, entity_type=None):
        """
        Create an entity based on entity_type.

        Parameters:
        - entity_type (str): The type of entity to create. Choices are `student`, `teacher`, and `faculty_admin`.

        Returns:
        - Response: A response containing the serialized data of the created entity.
        """
        serializers = {
            "student": StudentSerializer,
            "teacher": TeacherSerializer,
            "faculty_admin": FacultyAdminSerializer,
        }

        serializer_class = serializers.get(entity_type)

        if not serializer_class:
            return Response(
                {"error": "Invalid entity type. Choices are `student`, `teacher`, and `faculty_admin`"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
