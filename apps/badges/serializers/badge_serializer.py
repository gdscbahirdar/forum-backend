from rest_framework import serializers

from apps.badges.models.badge_models import Badge


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ("name", "description", "level")


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = Badge
        fields = ("badge", "created_at")
