from rest_framework import permissions, viewsets

from apps.entities.models.faculty_models import Faculty
from apps.entities.serializers.faculty_serializers import FacultySerializer


class FacultyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = (permissions.AllowAny,)
