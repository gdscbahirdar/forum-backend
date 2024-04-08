from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.entities.utils import generate_password

User = get_user_model()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    role_name = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ("middle_name", "role_name", "is_first_time_login")

    def get_role_name(self, obj):
        return obj.user_role.role.name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "middle_name", "last_name", "is_first_time_login")
        read_only_fields = ("is_first_time_login",)

    def create(self, validated_data):
        username = validated_data.pop("username")
        first_name = validated_data.pop("first_name")
        middle_name = validated_data.pop("middle_name")
        last_name = validated_data.pop("last_name")
        password = generate_password(first_name, middle_name, last_name)
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            password=password,
            is_first_time_login=True,
        )
        return user
