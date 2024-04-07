from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.entities.serializers.student_serializers import StudentSerializer
from apps.entities.serializers.teacher_serializers import TeacherSerializer
from apps.rbac.permissions import IsUserSuperAdminOrFacultyAdmin


class CreateEntityAPIView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsUserSuperAdminOrFacultyAdmin,
    )

    def post(self, request, entity_type):
        if entity_type == "student":
            serializer = StudentSerializer(data=request.data)
        elif entity_type == "teacher":
            serializer = TeacherSerializer(data=request.data)
        else:
            return Response(
                {"error": "Invalid entity type. Choices are `student` and `teacher`"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
