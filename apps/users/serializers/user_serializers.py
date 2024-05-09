from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    role_name = serializers.SerializerMethodField()
    email = serializers.EmailField(max_length=254, required=False)
    phone_number = PhoneNumberField()
    faculty = serializers.SerializerMethodField(read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "middle_name",
            "role_name",
            "is_first_time_login",
            "email",
            "phone_number",
            "bio",
            "avatar",
            "faculty",
        )

    def get_role_name(self, obj) -> str:
        return obj.user_role.role.name

    def get_faculty(self, obj) -> str:
        if getattr(obj, "faculty_admin", None):
            return obj.faculty_admin.faculty.name
        return ""
