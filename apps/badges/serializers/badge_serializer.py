from rest_framework import serializers

from apps.badges.models.badge_models import Badge


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ("pk", "name", "description", "points", "level", "created_at")
