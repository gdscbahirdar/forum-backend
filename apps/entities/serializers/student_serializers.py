from rest_framework import serializers

from apps.entities.models.faculty_models import Department
from apps.entities.models.faculty_models import Faculty
from apps.entities.models.student_models import Student
from apps.entities.serializers.related_fields import DepartmentRelatedField
from apps.entities.serializers.related_fields import FacultyRelatedField


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.
    """

    MAX_YEAR_IN_SCHOOL = 5

    faculty = FacultyRelatedField(queryset=Faculty.objects.all())
    department = DepartmentRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Student
        fields = (
            "pk",
            "faculty",
            "department",
            "year_in_school",
            "admission_date",
            "graduation_date",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        if attrs.get("admission_date") >= attrs.get("graduation_date"):
            raise serializers.ValidationError({"admission_date": "Admission date must be before graduation date."})

        if attrs.get("year_in_school") > self.MAX_YEAR_IN_SCHOOL:
            raise serializers.ValidationError({"year_in_school": "Year in school must not be greater than 5."})

        return attrs
