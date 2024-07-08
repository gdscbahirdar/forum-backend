from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from apps.entities.models.faculty_models import Faculty
from apps.entities.serializers.faculty_serializers import FacultySerializer


class FacultyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ("name",)
