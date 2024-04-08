from rest_framework import serializers

from apps.entities.models.faculty_models import Department, Faculty


class FacultyRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return Faculty.objects.get(name=data)


class DepartmentRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return Department.objects.get(name=data)
