from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.entities.models.admin_models import FacultyAdmin
from apps.entities.models.student_models import Student
from apps.entities.models.teacher_models import Teacher
from apps.entities.serializers.student_serializers import StudentSerializer
from apps.entities.serializers.teacher_serializers import TeacherSerializer
from apps.entities.serializers.faculty_admin_serializers import FacultyAdminSerializer
from apps.rbac.permissions import IsUserSuperAdminOrFacultyAdmin, IsUserSuperAdmin


class EntityViewSet(viewsets.ViewSet):
    """
    A viewset for managing entities of different types.

    This viewset provides the following actions:
    - list: List entities based on entity_type.
    - create: Create an entity based on entity_type.

    The supported entity types are `student`, `teacher`, and `faculty_admin`.

    Permissions:
    - Only authenticated users can access this viewset.
    - For the `create` action, the user must be a super admin or a faculty admin.
    - For other actions, the user must be a super admin or a faculty admin.

    """

    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            if self.kwargs.get("entity_type") == "faculty_admin":
                permission_classes = [IsAuthenticated, IsUserSuperAdmin]
            else:
                permission_classes = [IsAuthenticated, IsUserSuperAdminOrFacultyAdmin]
        else:
            permission_classes = [IsAuthenticated, IsUserSuperAdminOrFacultyAdmin]
        return [permission() for permission in permission_classes]

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

    def destroy(self, request, entity_type=None, pk=None):
        """
        Delete an entity based on entity_type and pk.

        Parameters:
        - entity_type (str): The type of entity to delete. Choices are `student`, `teacher`, and `faculty_admin`.
        - pk (int): The primary key of the entity to delete.

        Returns:
        - Response: A response indicating the success or failure of the delete operation.
        """
        models = {
            "student": Student,
            "teacher": Teacher,
            "faculty_admin": FacultyAdmin,
        }

        model = models.get(entity_type)

        if not model:
            return Response(
                {"error": "Invalid entity type. Choices are `student`, `teacher`, and `faculty_admin`"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response(
                {"error": f"{entity_type.capitalize()} with id {pk} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
