from rest_framework import viewsets, permissions
from apps.entities.serializers.faculty_serializers import FacultySerializer
from apps.entities.models.faculty_models import Faculty


class FacultyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = (permissions.IsAuthenticated,)
