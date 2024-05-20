from typing import Any, Dict

from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.badges.models.badge_models import UserBadge
from apps.badges.serializers.badge_serializer import BadgeSerializer

User = get_user_model()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    role_name = serializers.SerializerMethodField()
    email = serializers.EmailField(max_length=254, required=False)
    phone_number = PhoneNumberField(required=False)
    faculty = serializers.SerializerMethodField(read_only=True)
    badge = serializers.SerializerMethodField(read_only=True)

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
            "gender",
            "reputation",
            "badge",
        )
        read_only_fields = UserDetailsSerializer.Meta.read_only_fields + ("reputation", "badge")

    def get_role_name(self, obj) -> str:
        return obj.user_role.role.name

    def get_faculty(self, obj) -> str:
        if getattr(obj, "faculty_admin", None):
            return obj.faculty_admin.faculty.name
        return ""

    def get_badge(self, obj) -> Dict[str, Any]:
        recent_badge = UserBadge.objects.filter(user=obj).order_by("-created_at").first()
        return BadgeSerializer(recent_badge.badge).data if recent_badge else {}


class PublicUserProfileSerializer(CustomUserDetailsSerializer):
    class Meta(CustomUserDetailsSerializer.Meta):
        fields = (
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "bio",
            "avatar",
            "faculty",
            "reputation",
        )
