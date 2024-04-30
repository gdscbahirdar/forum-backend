from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    role_name = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ("middle_name", "role_name", "is_first_time_login")

    def get_role_name(self, obj) -> str:
        return obj.user_role.role.name
