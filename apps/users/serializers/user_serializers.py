from typing import Dict

from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.badges.models.badge_models import Badge, UserBadge

User = get_user_model()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    role_name = serializers.SerializerMethodField()
    email = serializers.EmailField(max_length=254, required=False)
    phone_number = PhoneNumberField(required=False)
    faculty = serializers.SerializerMethodField(read_only=True)
    badges = serializers.SerializerMethodField(read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = (
            *UserDetailsSerializer.Meta.fields,
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
            "badges",
        )
        read_only_fields = (*UserDetailsSerializer.Meta.read_only_fields, "reputation", "badge")

    def get_role_name(self, obj) -> str:
        return obj.user_role.role.name

    def get_faculty(self, obj) -> str:
        if getattr(obj, "faculty_admin", None):
            return obj.faculty_admin.faculty.name
        return ""

    def get_badges(self, obj) -> Dict[str, int]:
        badges = UserBadge.objects.filter(user=obj).aggregate(
            gold_badges=Count("id", filter=Q(badge__level=Badge.BadgeLevel.GOLD)),
            silver_badges=Count("id", filter=Q(badge__level=Badge.BadgeLevel.SILVER)),
            bronze_badges=Count("id", filter=Q(badge__level=Badge.BadgeLevel.BRONZE)),
        )
        return {
            "gold_badges": badges.get("gold_badges", 0),
            "silver_badges": badges.get("silver_badges", 0),
            "bronze_badges": badges.get("bronze_badges", 0),
        }


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
