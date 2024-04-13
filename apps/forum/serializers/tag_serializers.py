from rest_framework import serializers

from apps.forum.models.tag_models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Tag model.

    Serializes the Tag model fields: pk, name, description, created_at, updated_at.
    """

    class Meta:
        model = Tag
        fields = ("pk", "name", "description", "created_at", "updated_at")
