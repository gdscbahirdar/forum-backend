from drf_spectacular.utils import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.entities.models.faculty_models import Department
from apps.entities.models.faculty_models import Faculty


@extend_schema_field(OpenApiTypes.STR)
class FacultyRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            return Faculty.objects.get(name=data)
        except Faculty.DoesNotExist:
            raise serializers.ValidationError(f"Faculty with name '{data}' does not exist.")


@extend_schema_field(OpenApiTypes.STR)
class DepartmentRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            return Department.objects.get(name=data)
        except Department.DoesNotExist:
            raise serializers.ValidationError(f"Department with name '{data}' does not exist.")
